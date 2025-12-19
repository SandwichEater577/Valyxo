//! Process management
//! 
//! Spawn and manage child processes with output streaming.

use napi::bindgen_prelude::*;
use std::process::{Command, Child, Stdio};
use std::io::{BufRead, BufReader};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::collections::HashMap;
use parking_lot::Mutex;
use dashmap::DashMap;
use uuid::Uuid;
use serde::{Deserialize, Serialize};
use crate::error::ValyxoError;

/// Process info
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct ProcessInfo {
    pub id: String,
    pub command: String,
    pub args: Vec<String>,
    pub cwd: String,
    pub running: bool,
    pub exit_code: Option<i32>,
    pub pid: Option<u32>,
}

/// Process output
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct ProcessOutput {
    pub stdout: String,
    pub stderr: String,
    pub exit_code: i32,
    pub success: bool,
}

// Global process storage
lazy_static::lazy_static! {
    static ref PROCESSES: DashMap<String, ManagedProcess> = DashMap::new();
}

struct ManagedProcess {
    id: String,
    command: String,
    args: Vec<String>,
    cwd: String,
    running: Arc<AtomicBool>,
    child: Arc<Mutex<Option<Child>>>,
    stdout_buffer: Arc<Mutex<Vec<String>>>,
    stderr_buffer: Arc<Mutex<Vec<String>>>,
}

/// Spawn a process
#[napi]
pub fn spawn_process(
    command: String,
    args: Option<Vec<String>>,
    cwd: Option<String>,
    env: Option<HashMap<String, String>>,
) -> Result<String> {
    let args = args.unwrap_or_default();
    let working_dir = cwd.unwrap_or_else(|| {
        std::env::current_dir()
            .map(|p| p.to_string_lossy().to_string())
            .unwrap_or_else(|_| ".".to_string())
    });
    
    let mut cmd = Command::new(&command);
    cmd.args(&args);
    cmd.current_dir(&working_dir);
    cmd.stdout(Stdio::piped());
    cmd.stderr(Stdio::piped());
    cmd.stdin(Stdio::piped());
    
    if let Some(env_vars) = env {
        for (key, value) in env_vars {
            cmd.env(key, value);
        }
    }
    
    let child = cmd.spawn()
        .map_err(|e| ValyxoError::Process(e.to_string()))?;
    
    let id = Uuid::new_v4().to_string();
    
    let process = ManagedProcess {
        id: id.clone(),
        command: command.clone(),
        args: args.clone(),
        cwd: working_dir,
        running: Arc::new(AtomicBool::new(true)),
        child: Arc::new(Mutex::new(Some(child))),
        stdout_buffer: Arc::new(Mutex::new(Vec::new())),
        stderr_buffer: Arc::new(Mutex::new(Vec::new())),
    };
    
    PROCESSES.insert(id.clone(), process);
    
    tracing::info!("Spawned process: {} (id: {})", command, id);
    
    Ok(id)
}

/// Run a command and wait for completion
#[napi]
pub fn run_command(
    command: String,
    args: Option<Vec<String>>,
    cwd: Option<String>,
    env: Option<HashMap<String, String>>,
    timeout_ms: Option<u32>,
) -> Result<ProcessOutput> {
    let args = args.unwrap_or_default();
    let working_dir = cwd.unwrap_or_else(|| ".".to_string());
    
    let mut cmd = Command::new(&command);
    cmd.args(&args);
    cmd.current_dir(&working_dir);
    cmd.stdout(Stdio::piped());
    cmd.stderr(Stdio::piped());
    
    if let Some(env_vars) = env {
        for (key, value) in env_vars {
            cmd.env(key, value);
        }
    }
    
    let output = if let Some(timeout) = timeout_ms {
        // With timeout - spawn and wait with timeout
        let mut child = cmd.spawn()
            .map_err(|e| ValyxoError::Process(e.to_string()))?;
        
        let start = std::time::Instant::now();
        let timeout_duration = std::time::Duration::from_millis(timeout as u64);
        
        loop {
            match child.try_wait() {
                Ok(Some(status)) => {
                    let mut stdout = String::new();
                    let mut stderr = String::new();
                    
                    if let Some(ref mut out) = child.stdout {
                        std::io::Read::read_to_string(out, &mut stdout).ok();
                    }
                    if let Some(ref mut err) = child.stderr {
                        std::io::Read::read_to_string(err, &mut stderr).ok();
                    }
                    
                    let exit_code = status.code().unwrap_or(-1);
                    
                    return Ok(ProcessOutput {
                        stdout,
                        stderr,
                        exit_code,
                        success: status.success(),
                    });
                }
                Ok(None) => {
                    if start.elapsed() > timeout_duration {
                        child.kill().ok();
                        return Err(ValyxoError::Process("Process timeout".to_string()).into());
                    }
                    std::thread::sleep(std::time::Duration::from_millis(10));
                }
                Err(e) => {
                    return Err(ValyxoError::Process(e.to_string()).into());
                }
            }
        }
    } else {
        // Without timeout - simple wait
        cmd.output()
            .map_err(|e| ValyxoError::Process(e.to_string()))?
    };
    
    let exit_code = output.status.code().unwrap_or(-1);
    
    Ok(ProcessOutput {
        stdout: String::from_utf8_lossy(&output.stdout).to_string(),
        stderr: String::from_utf8_lossy(&output.stderr).to_string(),
        exit_code,
        success: output.status.success(),
    })
}

/// Write to process stdin
#[napi]
pub fn write_to_process(id: String, data: String) -> Result<()> {
    let process = PROCESSES.get(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Process not found: {}", id)))?;
    
    if !process.running.load(Ordering::SeqCst) {
        return Err(ValyxoError::Process("Process is not running".to_string()).into());
    }
    
    let mut child_guard = process.child.lock();
    if let Some(ref mut child) = *child_guard {
        if let Some(ref mut stdin) = child.stdin {
            use std::io::Write;
            stdin.write_all(data.as_bytes())?;
            stdin.flush()?;
        }
    }
    
    Ok(())
}

/// Read stdout from process
#[napi]
pub fn read_process_stdout(id: String) -> Result<Vec<String>> {
    let process = PROCESSES.get(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Process not found: {}", id)))?;
    
    let mut buffer = process.stdout_buffer.lock();
    let lines = buffer.clone();
    buffer.clear();
    
    Ok(lines)
}

/// Read stderr from process
#[napi]
pub fn read_process_stderr(id: String) -> Result<Vec<String>> {
    let process = PROCESSES.get(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Process not found: {}", id)))?;
    
    let mut buffer = process.stderr_buffer.lock();
    let lines = buffer.clone();
    buffer.clear();
    
    Ok(lines)
}

/// Get process info
#[napi]
pub fn get_process_info(id: String) -> Result<ProcessInfo> {
    let process = PROCESSES.get(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Process not found: {}", id)))?;
    
    let mut child_guard = process.child.lock();
    let (running, exit_code, pid) = if let Some(ref mut child) = *child_guard {
        match child.try_wait() {
            Ok(Some(status)) => {
                process.running.store(false, Ordering::SeqCst);
                (false, status.code(), Some(child.id()))
            }
            Ok(None) => (true, None, Some(child.id())),
            Err(_) => (false, None, None),
        }
    } else {
        (false, None, None)
    };
    
    Ok(ProcessInfo {
        id: process.id.clone(),
        command: process.command.clone(),
        args: process.args.clone(),
        cwd: process.cwd.clone(),
        running,
        exit_code,
        pid,
    })
}

/// List all managed processes
#[napi]
pub fn list_processes() -> Vec<ProcessInfo> {
    PROCESSES.iter()
        .filter_map(|entry| {
            get_process_info(entry.key().clone()).ok()
        })
        .collect()
}

/// Kill a process
#[napi]
pub fn kill_process(id: String) -> Result<bool> {
    let process = PROCESSES.get(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Process not found: {}", id)))?;
    
    let mut child_guard = process.child.lock();
    if let Some(ref mut child) = *child_guard {
        child.kill()
            .map_err(|e| ValyxoError::Process(e.to_string()))?;
        process.running.store(false, Ordering::SeqCst);
        return Ok(true);
    }
    
    Ok(false)
}

/// Wait for process to complete
#[napi]
pub fn wait_for_process(id: String) -> Result<i32> {
    let process = PROCESSES.get(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Process not found: {}", id)))?;
    
    let mut child_guard = process.child.lock();
    if let Some(ref mut child) = *child_guard {
        let status = child.wait()
            .map_err(|e| ValyxoError::Process(e.to_string()))?;
        
        process.running.store(false, Ordering::SeqCst);
        
        return Ok(status.code().unwrap_or(-1));
    }
    
    Err(ValyxoError::Process("No child process".to_string()).into())
}

/// Remove a process from management
#[napi]
pub fn remove_process(id: String) -> Result<bool> {
    // First kill if running
    if let Some(process) = PROCESSES.get(&id) {
        if process.running.load(Ordering::SeqCst) {
            kill_process(id.clone()).ok();
        }
    }
    
    Ok(PROCESSES.remove(&id).is_some())
}

/// Kill all processes
#[napi]
pub fn kill_all_processes() -> u32 {
    let mut count = 0;
    
    for entry in PROCESSES.iter() {
        let id = entry.key().clone();
        if kill_process(id).unwrap_or(false) {
            count += 1;
        }
    }
    
    PROCESSES.clear();
    
    tracing::info!("Killed {} processes", count);
    
    count
}

/// Run shell command (convenience function)
#[napi]
pub fn run_shell(command: String, cwd: Option<String>) -> Result<ProcessOutput> {
    let (shell, flag) = if cfg!(windows) {
        ("cmd", "/C")
    } else {
        ("sh", "-c")
    };
    
    run_command(shell.to_string(), Some(vec![flag.to_string(), command]), cwd, None, None)
}
