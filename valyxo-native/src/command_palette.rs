//! Command palette for quick actions

use eframe::egui::{self, Key, TextEdit, Ui};
use fuzzy_matcher::skim::SkimMatcherV2;
use fuzzy_matcher::FuzzyMatcher;
use std::path::PathBuf;
use walkdir::WalkDir;

/// Command palette mode
#[derive(Clone, PartialEq)]
pub enum PaletteMode {
    /// Commands (>)
    Commands,
    /// Quick file open
    QuickOpen,
}

/// A command in the palette
#[derive(Clone)]
pub struct Command {
    pub id: String,
    pub label: String,
    pub shortcut: Option<String>,
}

/// Command palette
pub struct CommandPalette {
    mode: PaletteMode,
    query: String,
    selected_index: usize,
    commands: Vec<Command>,
    files: Vec<PathBuf>,
    matcher: SkimMatcherV2,
}

impl CommandPalette {
    pub fn new() -> Self {
        let commands = vec![
            Command { id: "file.open".into(), label: "Open File".into(), shortcut: Some("Ctrl+O".into()) },
            Command { id: "file.save".into(), label: "Save File".into(), shortcut: Some("Ctrl+S".into()) },
            Command { id: "file.saveAs".into(), label: "Save As...".into(), shortcut: None },
            Command { id: "file.close".into(), label: "Close File".into(), shortcut: Some("Ctrl+W".into()) },
            Command { id: "view.toggle_sidebar".into(), label: "Toggle Sidebar".into(), shortcut: Some("Ctrl+B".into()) },
            Command { id: "view.command_palette".into(), label: "Command Palette".into(), shortcut: Some("Ctrl+Shift+P".into()) },
            Command { id: "edit.undo".into(), label: "Undo".into(), shortcut: Some("Ctrl+Z".into()) },
            Command { id: "edit.redo".into(), label: "Redo".into(), shortcut: Some("Ctrl+Y".into()) },
            Command { id: "edit.cut".into(), label: "Cut".into(), shortcut: Some("Ctrl+X".into()) },
            Command { id: "edit.copy".into(), label: "Copy".into(), shortcut: Some("Ctrl+C".into()) },
            Command { id: "edit.paste".into(), label: "Paste".into(), shortcut: Some("Ctrl+V".into()) },
            Command { id: "edit.selectAll".into(), label: "Select All".into(), shortcut: Some("Ctrl+A".into()) },
            Command { id: "edit.find".into(), label: "Find".into(), shortcut: Some("Ctrl+F".into()) },
            Command { id: "edit.replace".into(), label: "Replace".into(), shortcut: Some("Ctrl+H".into()) },
            Command { id: "theme.dark".into(), label: "Theme: Dark".into(), shortcut: None },
            Command { id: "theme.light".into(), label: "Theme: Light".into(), shortcut: None },
        ];
        
        Self {
            mode: PaletteMode::QuickOpen,
            query: String::new(),
            selected_index: 0,
            commands,
            files: Vec::new(),
            matcher: SkimMatcherV2::default(),
        }
    }
    
    /// Set mode to quick open
    pub fn set_mode_quick_open(&mut self) {
        self.mode = PaletteMode::QuickOpen;
        self.query.clear();
        self.selected_index = 0;
    }
    
    /// Set mode to commands
    pub fn set_mode_commands(&mut self) {
        self.mode = PaletteMode::Commands;
        self.query.clear();
        self.selected_index = 0;
    }
    
    /// Load files from workspace
    pub fn load_files(&mut self, workspace: &PathBuf) {
        self.files.clear();
        
        for entry in WalkDir::new(workspace)
            .max_depth(10)
            .into_iter()
            .filter_map(|e| e.ok())
        {
            let path = entry.path();
            if path.is_file() {
                let name = path.file_name()
                    .map(|n| n.to_string_lossy().to_string())
                    .unwrap_or_default();
                
                // Skip hidden and ignored
                if name.starts_with('.') {
                    continue;
                }
                
                // Skip common ignored directories
                let path_str = path.to_string_lossy();
                if path_str.contains("node_modules") || 
                   path_str.contains("target") || 
                   path_str.contains("__pycache__") ||
                   path_str.contains(".git") {
                    continue;
                }
                
                self.files.push(path.to_path_buf());
            }
        }
    }
    
    /// Show the command palette and return selected command/file
    pub fn show(&mut self, ui: &mut Ui, workspace: &Option<PathBuf>) -> Option<String> {
        let mut result = None;
        
        // Load files if needed
        if self.mode == PaletteMode::QuickOpen && self.files.is_empty() {
            if let Some(ref ws) = workspace {
                self.load_files(ws);
            }
        }
        
        // Input field
        let placeholder = match self.mode {
            PaletteMode::Commands => "Type a command...",
            PaletteMode::QuickOpen => "Search files...",
        };
        
        let response = ui.add(
            TextEdit::singleline(&mut self.query)
                .hint_text(placeholder)
                .desired_width(480.0)
        );
        
        // Focus the input
        response.request_focus();
        
        // Check for mode switch
        if self.query.starts_with('>') && self.mode != PaletteMode::Commands {
            self.mode = PaletteMode::Commands;
            self.query = self.query[1..].to_string();
        }
        
        ui.separator();
        
        // Get filtered results
        let results: Vec<(usize, String, String)> = match self.mode {
            PaletteMode::Commands => {
                self.commands.iter()
                    .enumerate()
                    .filter_map(|(i, cmd)| {
                        if self.query.is_empty() {
                            Some((i, cmd.label.clone(), cmd.id.clone()))
                        } else {
                            self.matcher.fuzzy_match(&cmd.label, &self.query)
                                .map(|_| (i, cmd.label.clone(), cmd.id.clone()))
                        }
                    })
                    .take(15)
                    .collect()
            }
            PaletteMode::QuickOpen => {
                self.files.iter()
                    .enumerate()
                    .filter_map(|(i, path)| {
                        let name = path.file_name()?.to_string_lossy().to_string();
                        let display = path.to_string_lossy().to_string();
                        
                        if self.query.is_empty() {
                            Some((i, name, display))
                        } else {
                            self.matcher.fuzzy_match(&name, &self.query)
                                .map(|_| (i, name, display))
                        }
                    })
                    .take(15)
                    .collect()
            }
        };
        
        // Clamp selected index
        if !results.is_empty() {
            self.selected_index = self.selected_index.min(results.len() - 1);
        } else {
            self.selected_index = 0;
        }
        
        // Handle keyboard navigation
        ui.input(|input| {
            if input.key_pressed(Key::ArrowDown) {
                if !results.is_empty() {
                    self.selected_index = (self.selected_index + 1) % results.len();
                }
            }
            if input.key_pressed(Key::ArrowUp) {
                if !results.is_empty() {
                    if self.selected_index == 0 {
                        self.selected_index = results.len() - 1;
                    } else {
                        self.selected_index -= 1;
                    }
                }
            }
            if input.key_pressed(Key::Enter) {
                if let Some((_, _, ref value)) = results.get(self.selected_index) {
                    result = Some(value.clone());
                }
            }
        });
        
        // Show results
        egui::ScrollArea::vertical()
            .max_height(300.0)
            .show(ui, |ui| {
                for (i, (_, label, value)) in results.iter().enumerate() {
                    let is_selected = i == self.selected_index;
                    
                    let response = ui.selectable_label(is_selected, label);
                    
                    if response.clicked() {
                        result = Some(value.clone());
                    }
                    
                    if response.hovered() {
                        self.selected_index = i;
                    }
                }
                
                if results.is_empty() {
                    ui.label("No results found");
                }
            });
        
        result
    }
}
