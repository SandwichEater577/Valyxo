//! Tab bar for open files

use crate::buffer::BufferId;
use eframe::egui::{self, Color32, Ui};
use std::path::PathBuf;

/// Tab action
pub enum TabAction {
    Select,
    Close,
}

/// A single tab
#[derive(Clone)]
pub struct Tab {
    pub path: PathBuf,
    pub buffer_id: BufferId,
    pub name: String,
    pub modified: bool,
}

impl Tab {
    pub fn new(path: PathBuf, buffer_id: BufferId) -> Self {
        let name = path.file_name()
            .map(|n| n.to_string_lossy().to_string())
            .unwrap_or_else(|| "Untitled".to_string());
        
        Self {
            path,
            buffer_id,
            name,
            modified: false,
        }
    }
}

/// Tab bar
pub struct TabBar {
    tabs: Vec<Tab>,
    current_index: Option<usize>,
}

impl TabBar {
    pub fn new() -> Self {
        Self {
            tabs: Vec::new(),
            current_index: None,
        }
    }
    
    /// Add a new tab
    pub fn add_tab(&mut self, path: PathBuf, buffer_id: BufferId) {
        // Check if already open
        for (i, tab) in self.tabs.iter().enumerate() {
            if tab.path == path {
                self.current_index = Some(i);
                return;
            }
        }
        
        let tab = Tab::new(path, buffer_id);
        self.tabs.push(tab);
        self.current_index = Some(self.tabs.len() - 1);
    }
    
    /// Get current buffer ID
    pub fn current_buffer_id(&self) -> Option<BufferId> {
        self.current_index.and_then(|i| self.tabs.get(i).map(|t| t.buffer_id))
    }
    
    /// Close current tab
    pub fn close_current(&mut self) {
        if let Some(index) = self.current_index {
            self.tabs.remove(index);
            if self.tabs.is_empty() {
                self.current_index = None;
            } else if index >= self.tabs.len() {
                self.current_index = Some(self.tabs.len() - 1);
            }
        }
    }
    
    /// Close a specific tab
    pub fn close_tab(&mut self, index: usize) {
        if index < self.tabs.len() {
            self.tabs.remove(index);
            if self.tabs.is_empty() {
                self.current_index = None;
            } else if let Some(current) = self.current_index {
                if current >= self.tabs.len() {
                    self.current_index = Some(self.tabs.len() - 1);
                } else if index < current {
                    self.current_index = Some(current - 1);
                }
            }
        }
    }
    
    /// Next tab
    pub fn next_tab(&mut self) {
        if let Some(index) = self.current_index {
            if !self.tabs.is_empty() {
                self.current_index = Some((index + 1) % self.tabs.len());
            }
        }
    }
    
    /// Previous tab
    pub fn prev_tab(&mut self) {
        if let Some(index) = self.current_index {
            if !self.tabs.is_empty() {
                if index == 0 {
                    self.current_index = Some(self.tabs.len() - 1);
                } else {
                    self.current_index = Some(index - 1);
                }
            }
        }
    }
    
    /// Mark a tab as modified
    pub fn set_modified(&mut self, buffer_id: BufferId, modified: bool) {
        for tab in &mut self.tabs {
            if tab.buffer_id == buffer_id {
                tab.modified = modified;
                break;
            }
        }
    }
    
    /// Show the tab bar
    pub fn show(&mut self, ui: &mut Ui) -> Option<(TabAction, BufferId)> {
        let mut result = None;
        
        if self.tabs.is_empty() {
            return None;
        }
        
        ui.horizontal(|ui| {
            let mut close_index = None;
            
            for (i, tab) in self.tabs.iter().enumerate() {
                let is_selected = self.current_index == Some(i);
                
                let bg_color = if is_selected {
                    Color32::from_rgb(45, 45, 45)
                } else {
                    Color32::from_rgb(30, 30, 30)
                };
                
                let text_color = if is_selected {
                    Color32::from_rgb(255, 255, 255)
                } else {
                    Color32::from_rgb(180, 180, 180)
                };
                
                egui::Frame::none()
                    .fill(bg_color)
                    .inner_margin(egui::Margin::symmetric(8.0, 4.0))
                    .show(ui, |ui| {
                        ui.horizontal(|ui| {
                            // Modified indicator
                            let label = if tab.modified {
                                format!("● {}", tab.name)
                            } else {
                                tab.name.clone()
                            };
                            
                            // Tab name button
                            if ui.selectable_label(is_selected, egui::RichText::new(&label).color(text_color)).clicked() {
                                self.current_index = Some(i);
                                result = Some((TabAction::Select, tab.buffer_id));
                            }
                            
                            // Close button
                            if ui.small_button("×").clicked() {
                                close_index = Some(i);
                                result = Some((TabAction::Close, tab.buffer_id));
                            }
                        });
                    });
            }
            
            if let Some(index) = close_index {
                self.close_tab(index);
            }
        });
        
        ui.separator();
        
        result
    }
}
