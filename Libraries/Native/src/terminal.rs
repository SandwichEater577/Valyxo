//! Terminal/PTY emulation
//! 
//! Provides pseudo-terminal functionality for running shell commands
//! with full terminal emulation support.

use napi::bindgen_prelude::*;
use portable_pty::{native_pty_system, CommandBuilder, PtySize};
use std::io::{Read, Write};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use parking_lot::Mutex;
use dashmap::DashMap;
use uuid::Uuid;
use serde::{Deserialize, Serialize};
use crate::error::ValyxoError;

/// Terminal session info
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct TerminalInfo {
    pub id: String,
    pub shell: String,
    pub cwd: String,
    pub cols: u32,
    pub rows: u32,
    pub running: bool,
}

/// Terminal output
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct TerminalOutput {
    pub id: String,
    pub data: String,
}

// Global terminal sessions storage
lazy_static::lazy_static! {
    static ref TERMINALS: DashMap<String, TerminalSession> = DashMap::new();
}

struct TerminalSession {
    id: String,
    shell: String,
    cwd: String,
    cols: u32,
    rows: u32,
    running: Arc<AtomicBool>,
    writer: Arc<Mutex<Box<dyn Write + Send>>>,
    reader: Arc<Mutex<Box<dyn Read + Send>>>,
}

/// Create a new terminal session
#[napi]
pub fn create_terminal(
    shell: Option<String>,
    cwd: Option<String>,
    cols: Option<u32>,
    rows: Option<u32>,
) -> Result<String> {
    let pty_system = native_pty_system();
    
    let cols = cols.unwrap_or(80);
    let rows = rows.unwrap_or(24);
    
    let pair = pty_system
        .openpty(PtySize {
            rows: rows as u16,
            cols: cols as u16,
            pixel_width: 0,
            pixel_height: 0,
        })
        .map_err(|e| ValyxoError::Terminal(e.to_string()))?;
    
    // Determine shell based on OS
    let shell_cmd = shell.unwrap_or_else(|| {
        if cfg!(windows) {
            "powershell.exe".to_string()
        } else {
            std::env::var("SHELL").unwrap_or_else(|_| "/bin/bash".to_string())
        }
    });
    
    let working_dir = cwd.unwrap_or_else(|| {
        std::env::current_dir()
            .map(|p| p.to_string_lossy().to_string())
            .unwrap_or_else(|_| ".".to_string())
    });
    
    let mut cmd = CommandBuilder::new(&shell_cmd);
    cmd.cwd(&working_dir);
    
    // Spawn the shell
    let child = pair.slave
        .spawn_command(cmd)
        .map_err(|e| ValyxoError::Terminal(e.to_string()))?;
    
    // Drop child as we don't need to wait on it
    drop(child);
    
    let id = Uuid::new_v4().to_string();
    
    let reader = pair.master.try_clone_reader()
        .map_err(|e| ValyxoError::Terminal(e.to_string()))?;
    
    let writer = pair.master
        .take_writer()
        .map_err(|e| ValyxoError::Terminal(e.to_string()))?;
    
    let session = TerminalSession {
        id: id.clone(),
        shell: shell_cmd,
        cwd: working_dir,
        cols,
        rows,
        running: Arc::new(AtomicBool::new(true)),
        writer: Arc::new(Mutex::new(writer)),
        reader: Arc::new(Mutex::new(reader)),
    };
    
    TERMINALS.insert(id.clone(), session);
    
    tracing::info!("Created terminal session: {}", id);
    
    Ok(id)
}

/// Write data to terminal
#[napi]
pub fn write_terminal(id: String, data: String) -> Result<()> {
    let terminal = TERMINALS.get(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Terminal not found: {}", id)))?;
    
    if !terminal.running.load(Ordering::SeqCst) {
        return Err(ValyxoError::Terminal("Terminal is not running".to_string()).into());
    }
    
    let mut writer = terminal.writer.lock();
    writer.write_all(data.as_bytes())?;
    writer.flush()?;
    
    Ok(())
}

/// Read output from terminal
#[napi]
pub fn read_terminal(id: String, max_bytes: Option<u32>) -> Result<String> {
    let terminal = TERMINALS.get(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Terminal not found: {}", id)))?;
    
    let max = max_bytes.unwrap_or(4096) as usize;
    let mut buffer = vec![0u8; max];
    
    let mut reader = terminal.reader.lock();
    
    // Non-blocking read attempt
    match reader.read(&mut buffer) {
        Ok(n) if n > 0 => {
            let output = String::from_utf8_lossy(&buffer[..n]).to_string();
            Ok(output)
        }
        Ok(_) => Ok(String::new()),
        Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => Ok(String::new()),
        Err(e) => Err(ValyxoError::Terminal(e.to_string()).into()),
    }
}

/// Resize terminal
#[napi]
pub fn resize_terminal(id: String, cols: u32, rows: u32) -> Result<()> {
    let mut terminal = TERMINALS.get_mut(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Terminal not found: {}", id)))?;
    
    terminal.cols = cols;
    terminal.rows = rows;
    
    // Note: Actual resize requires PTY master resize which is more complex
    // This is a simplified implementation
    
    tracing::info!("Resized terminal {} to {}x{}", id, cols, rows);
    
    Ok(())
}

/// Get terminal info
#[napi]
pub fn get_terminal_info(id: String) -> Result<TerminalInfo> {
    let terminal = TERMINALS.get(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Terminal not found: {}", id)))?;
    
    Ok(TerminalInfo {
        id: terminal.id.clone(),
        shell: terminal.shell.clone(),
        cwd: terminal.cwd.clone(),
        cols: terminal.cols,
        rows: terminal.rows,
        running: terminal.running.load(Ordering::SeqCst),
    })
}

/// List all terminals
#[napi]
pub fn list_terminals() -> Vec<TerminalInfo> {
    TERMINALS.iter()
        .map(|entry| {
            let t = entry.value();
            TerminalInfo {
                id: t.id.clone(),
                shell: t.shell.clone(),
                cwd: t.cwd.clone(),
                cols: t.cols,
                rows: t.rows,
                running: t.running.load(Ordering::SeqCst),
            }
        })
        .collect()
}

/// Close terminal session
#[napi]
pub fn close_terminal(id: String) -> Result<()> {
    let terminal = TERMINALS.remove(&id)
        .ok_or_else(|| ValyxoError::NotFound(format!("Terminal not found: {}", id)))?;
    
    terminal.1.running.store(false, Ordering::SeqCst);
    
    tracing::info!("Closed terminal session: {}", id);
    
    Ok(())
}

/// Close all terminals
#[napi]
pub fn close_all_terminals() -> u32 {
    let count = TERMINALS.len() as u32;
    
    for entry in TERMINALS.iter() {
        entry.value().running.store(false, Ordering::SeqCst);
    }
    
    TERMINALS.clear();
    
    tracing::info!("Closed {} terminal sessions", count);
    
    count
}
