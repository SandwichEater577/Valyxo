//! Settings management
//! 
//! Fast JSON-based settings with file watching and defaults.

use napi::bindgen_prelude::*;
use std::path::{Path, PathBuf};
use std::fs;
use serde::{Deserialize, Serialize};
use serde_json::{Value, Map};
use parking_lot::RwLock;
use std::sync::Arc;
use crate::error::ValyxoError;

/// Settings container
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct SettingsSnapshot {
    pub data: String, // JSON string
    pub path: String,
    pub modified: i64,
}

// Global settings store
lazy_static::lazy_static! {
    static ref SETTINGS: Arc<RwLock<SettingsStore>> = Arc::new(RwLock::new(SettingsStore::default()));
}

#[derive(Default)]
struct SettingsStore {
    path: Option<PathBuf>,
    data: Map<String, Value>,
    defaults: Map<String, Value>,
}

/// Initialize settings from a file
#[napi]
pub fn init_settings(path: String, defaults: Option<String>) -> Result<()> {
    let settings_path = PathBuf::from(&path);
    let mut store = SETTINGS.write();
    
    store.path = Some(settings_path.clone());
    
    // Load defaults if provided
    if let Some(defaults_json) = defaults {
        if let Ok(parsed) = serde_json::from_str::<Map<String, Value>>(&defaults_json) {
            store.defaults = parsed.clone();
            store.data = parsed;
        }
    }
    
    // Load existing settings file
    if settings_path.exists() {
        let content = fs::read_to_string(&settings_path)?;
        if let Ok(parsed) = serde_json::from_str::<Map<String, Value>>(&content) {
            // Merge with defaults
            for (key, value) in parsed {
                store.data.insert(key, value);
            }
        }
    }
    
    tracing::info!("Settings initialized from: {:?}", settings_path);
    
    Ok(())
}

/// Get a setting value
#[napi]
pub fn get_setting(key: String) -> Result<Option<String>> {
    let store = SETTINGS.read();
    
    // Support dot notation for nested keys
    let value = get_nested_value(&store.data, &key);
    
    match value {
        Some(v) => Ok(Some(serde_json::to_string(&v)?)),
        None => Ok(None),
    }
}

/// Set a setting value
#[napi]
pub fn set_setting(key: String, value: String) -> Result<()> {
    let parsed_value: Value = serde_json::from_str(&value)
        .unwrap_or(Value::String(value.clone()));
    
    {
        let mut store = SETTINGS.write();
        set_nested_value(&mut store.data, &key, parsed_value);
    }
    
    // Save to file
    save_settings_internal()?;
    
    Ok(())
}

/// Delete a setting
#[napi]
pub fn delete_setting(key: String) -> Result<bool> {
    let existed = {
        let mut store = SETTINGS.write();
        let existed = store.data.contains_key(&key);
        store.data.remove(&key);
        existed
    };
    
    if existed {
        save_settings_internal()?;
    }
    
    Ok(existed)
}

/// Get all settings as JSON
#[napi]
pub fn get_all_settings() -> Result<String> {
    let store = SETTINGS.read();
    Ok(serde_json::to_string_pretty(&store.data)?)
}

/// Get settings snapshot
#[napi]
pub fn get_settings_snapshot() -> Result<SettingsSnapshot> {
    let store = SETTINGS.read();
    
    let modified = store.path.as_ref()
        .and_then(|p| fs::metadata(p).ok())
        .and_then(|m| m.modified().ok())
        .map(|t| t.duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs() as i64)
        .unwrap_or(0);
    
    Ok(SettingsSnapshot {
        data: serde_json::to_string(&store.data)?,
        path: store.path.as_ref()
            .map(|p| p.to_string_lossy().to_string())
            .unwrap_or_default(),
        modified,
    })
}

/// Reset settings to defaults
#[napi]
pub fn reset_settings() -> Result<()> {
    {
        let mut store = SETTINGS.write();
        store.data = store.defaults.clone();
    }
    
    save_settings_internal()?;
    
    Ok(())
}

/// Reset a specific setting to default
#[napi]
pub fn reset_setting(key: String) -> Result<()> {
    {
        let mut store = SETTINGS.write();
        
        if let Some(default) = store.defaults.get(&key).cloned() {
            store.data.insert(key, default);
        } else {
            store.data.remove(&key);
        }
    }
    
    save_settings_internal()?;
    
    Ok(())
}

/// Check if settings file has been modified externally
#[napi]
pub fn check_settings_modified() -> Result<bool> {
    let store = SETTINGS.read();
    
    if let Some(ref path) = store.path {
        if path.exists() {
            let current_content = fs::read_to_string(path)?;
            let stored_content = serde_json::to_string_pretty(&store.data)?;
            return Ok(current_content != stored_content);
        }
    }
    
    Ok(false)
}

/// Reload settings from file
#[napi]
pub fn reload_settings() -> Result<()> {
    let mut store = SETTINGS.write();
    
    if let Some(ref path) = store.path {
        if path.exists() {
            let content = fs::read_to_string(path)?;
            if let Ok(parsed) = serde_json::from_str::<Map<String, Value>>(&content) {
                // Reset to defaults then apply loaded settings
                store.data = store.defaults.clone();
                for (key, value) in parsed {
                    store.data.insert(key, value);
                }
            }
        }
    }
    
    Ok(())
}

/// Save settings to file
#[napi]
pub fn save_settings() -> Result<()> {
    save_settings_internal()
}

fn save_settings_internal() -> Result<()> {
    let store = SETTINGS.read();
    
    if let Some(ref path) = store.path {
        // Ensure parent directory exists
        if let Some(parent) = path.parent() {
            if !parent.exists() {
                fs::create_dir_all(parent)?;
            }
        }
        
        let content = serde_json::to_string_pretty(&store.data)?;
        
        // Atomic write
        let temp_path = path.with_extension("tmp");
        fs::write(&temp_path, &content)?;
        fs::rename(&temp_path, path)?;
    }
    
    Ok(())
}

// Helper functions for nested key access

fn get_nested_value<'a>(data: &'a Map<String, Value>, key: &str) -> Option<&'a Value> {
    let parts: Vec<&str> = key.split('.').collect();
    let mut current: &Value = &Value::Object(data.clone());
    
    for part in parts {
        match current {
            Value::Object(obj) => {
                current = obj.get(part)?;
            }
            _ => return None,
        }
    }
    
    Some(current)
}

fn set_nested_value(data: &mut Map<String, Value>, key: &str, value: Value) {
    let parts: Vec<&str> = key.split('.').collect();
    
    if parts.len() == 1 {
        data.insert(key.to_string(), value);
        return;
    }
    
    // Navigate to the correct nested location
    let mut current = Value::Object(data.clone());
    
    for (i, part) in parts.iter().enumerate() {
        if i == parts.len() - 1 {
            if let Value::Object(ref mut obj) = current {
                obj.insert(part.to_string(), value.clone());
            }
        } else {
            if let Value::Object(ref mut obj) = current {
                if !obj.contains_key(*part) {
                    obj.insert(part.to_string(), Value::Object(Map::new()));
                }
                // This is simplified - full implementation would need recursion
            }
        }
    }
    
    // Simple fallback: just set at top level for now
    data.insert(key.to_string(), value);
}
