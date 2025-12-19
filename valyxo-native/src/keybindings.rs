//! Keyboard shortcuts

use eframe::egui::{Key, Modifiers};
use std::collections::HashMap;

/// A keybinding
#[derive(Clone, Hash, PartialEq, Eq)]
pub struct Keybinding {
    pub key: Key,
    pub modifiers: Modifiers,
}

impl Keybinding {
    pub fn new(key: Key, ctrl: bool, shift: bool, alt: bool) -> Self {
        Self {
            key,
            modifiers: Modifiers {
                ctrl,
                shift,
                alt,
                command: false,
                mac_cmd: false,
            },
        }
    }
}

/// Keybindings manager
pub struct Keybindings {
    bindings: HashMap<Keybinding, String>,
}

impl Default for Keybindings {
    fn default() -> Self {
        let mut bindings = HashMap::new();
        
        // File operations
        bindings.insert(Keybinding::new(Key::O, true, false, false), "file.open".to_string());
        bindings.insert(Keybinding::new(Key::O, true, true, false), "file.openFolder".to_string());
        bindings.insert(Keybinding::new(Key::S, true, false, false), "file.save".to_string());
        bindings.insert(Keybinding::new(Key::S, true, true, false), "file.saveAs".to_string());
        bindings.insert(Keybinding::new(Key::W, true, false, false), "file.close".to_string());
        bindings.insert(Keybinding::new(Key::N, true, false, false), "file.new".to_string());
        
        // Edit operations
        bindings.insert(Keybinding::new(Key::Z, true, false, false), "edit.undo".to_string());
        bindings.insert(Keybinding::new(Key::Y, true, false, false), "edit.redo".to_string());
        bindings.insert(Keybinding::new(Key::Z, true, true, false), "edit.redo".to_string());
        bindings.insert(Keybinding::new(Key::X, true, false, false), "edit.cut".to_string());
        bindings.insert(Keybinding::new(Key::C, true, false, false), "edit.copy".to_string());
        bindings.insert(Keybinding::new(Key::V, true, false, false), "edit.paste".to_string());
        bindings.insert(Keybinding::new(Key::A, true, false, false), "edit.selectAll".to_string());
        bindings.insert(Keybinding::new(Key::F, true, false, false), "edit.find".to_string());
        bindings.insert(Keybinding::new(Key::H, true, false, false), "edit.replace".to_string());
        bindings.insert(Keybinding::new(Key::G, true, false, false), "edit.goToLine".to_string());
        
        // View operations
        bindings.insert(Keybinding::new(Key::B, true, false, false), "view.toggleSidebar".to_string());
        bindings.insert(Keybinding::new(Key::P, true, true, false), "view.commandPalette".to_string());
        bindings.insert(Keybinding::new(Key::P, true, false, false), "view.quickOpen".to_string());
        
        // Navigation
        bindings.insert(Keybinding::new(Key::Tab, true, false, false), "navigate.nextTab".to_string());
        bindings.insert(Keybinding::new(Key::Tab, true, true, false), "navigate.prevTab".to_string());
        
        Self { bindings }
    }
}

impl Keybindings {
    /// Get command for a keybinding
    pub fn get_command(&self, key: Key, modifiers: Modifiers) -> Option<&str> {
        let binding = Keybinding { key, modifiers };
        self.bindings.get(&binding).map(|s| s.as_str())
    }
    
    /// Set a keybinding
    pub fn set(&mut self, key: Key, modifiers: Modifiers, command: String) {
        let binding = Keybinding { key, modifiers };
        self.bindings.insert(binding, command);
    }
    
    /// Remove a keybinding
    pub fn remove(&mut self, key: Key, modifiers: Modifiers) {
        let binding = Keybinding { key, modifiers };
        self.bindings.remove(&binding);
    }
}
