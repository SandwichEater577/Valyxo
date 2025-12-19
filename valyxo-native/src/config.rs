//! Configuration management

use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use anyhow::Result;

/// Application configuration
#[derive(Clone, Serialize, Deserialize)]
pub struct Config {
    /// Font size for editor
    pub font_size: f32,
    
    /// Font family
    pub font_family: String,
    
    /// Tab size in spaces
    pub tab_size: usize,
    
    /// Use spaces instead of tabs
    pub use_spaces: bool,
    
    /// Show line numbers
    pub show_line_numbers: bool,
    
    /// Show minimap
    pub show_minimap: bool,
    
    /// Word wrap
    pub word_wrap: bool,
    
    /// Current theme name
    pub theme: String,
    
    /// Auto save delay in seconds (0 = disabled)
    pub auto_save_delay: u32,
    
    /// Recent files
    pub recent_files: Vec<PathBuf>,
    
    /// Recent folders
    pub recent_folders: Vec<PathBuf>,
    
    /// Window width
    pub window_width: f32,
    
    /// Window height
    pub window_height: f32,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            font_size: 14.0,
            font_family: "JetBrains Mono".to_string(),
            tab_size: 4,
            use_spaces: true,
            show_line_numbers: true,
            show_minimap: false,
            word_wrap: false,
            theme: "Dark".to_string(),
            auto_save_delay: 0,
            recent_files: Vec::new(),
            recent_folders: Vec::new(),
            window_width: 1400.0,
            window_height: 900.0,
        }
    }
}

impl Config {
    /// Get config file path
    fn config_path() -> Option<PathBuf> {
        dirs::config_dir().map(|p| p.join("valyxo").join("config.json"))
    }
    
    /// Load configuration from file
    pub fn load() -> Result<Self> {
        let path = Self::config_path()
            .ok_or_else(|| anyhow::anyhow!("Could not find config directory"))?;
        
        if path.exists() {
            let content = std::fs::read_to_string(&path)?;
            let config: Config = serde_json::from_str(&content)?;
            Ok(config)
        } else {
            Ok(Self::default())
        }
    }
    
    /// Save configuration to file
    pub fn save(&self) -> Result<()> {
        let path = Self::config_path()
            .ok_or_else(|| anyhow::anyhow!("Could not find config directory"))?;
        
        // Create directory if it doesn't exist
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        
        let content = serde_json::to_string_pretty(self)?;
        std::fs::write(&path, content)?;
        
        Ok(())
    }
    
    /// Add a recent file
    pub fn add_recent_file(&mut self, path: PathBuf) {
        // Remove if already exists
        self.recent_files.retain(|p| p != &path);
        
        // Add to front
        self.recent_files.insert(0, path);
        
        // Keep only last 10
        self.recent_files.truncate(10);
    }
    
    /// Add a recent folder
    pub fn add_recent_folder(&mut self, path: PathBuf) {
        self.recent_folders.retain(|p| p != &path);
        self.recent_folders.insert(0, path);
        self.recent_folders.truncate(10);
    }
}
