//! File tree panel

use eframe::egui::{self, Color32, Ui};
use std::collections::HashMap;
use std::path::PathBuf;
use walkdir::WalkDir;

/// File tree node
#[derive(Clone)]
pub struct FileNode {
    pub path: PathBuf,
    pub name: String,
    pub is_dir: bool,
    pub is_expanded: bool,
    pub children: Vec<FileNode>,
}

impl FileNode {
    fn from_path(path: PathBuf) -> Self {
        let name = path.file_name()
            .map(|n| n.to_string_lossy().to_string())
            .unwrap_or_else(|| path.to_string_lossy().to_string());
        
        let is_dir = path.is_dir();
        
        Self {
            path,
            name,
            is_dir,
            is_expanded: false,
            children: Vec::new(),
        }
    }
    
    fn load_children(&mut self) {
        if !self.is_dir || !self.children.is_empty() {
            return;
        }
        
        let mut dirs = Vec::new();
        let mut files = Vec::new();
        
        if let Ok(entries) = std::fs::read_dir(&self.path) {
            for entry in entries.filter_map(|e| e.ok()) {
                let path = entry.path();
                let name = path.file_name()
                    .map(|n| n.to_string_lossy().to_string())
                    .unwrap_or_default();
                
                // Skip hidden files and common ignored directories
                if name.starts_with('.') || name == "node_modules" || name == "target" || name == "__pycache__" {
                    continue;
                }
                
                let node = FileNode::from_path(path);
                if node.is_dir {
                    dirs.push(node);
                } else {
                    files.push(node);
                }
            }
        }
        
        // Sort: directories first, then files, alphabetically
        dirs.sort_by(|a, b| a.name.to_lowercase().cmp(&b.name.to_lowercase()));
        files.sort_by(|a, b| a.name.to_lowercase().cmp(&b.name.to_lowercase()));
        
        self.children = dirs;
        self.children.extend(files);
    }
}

/// File tree panel
pub struct FileTree {
    root: Option<FileNode>,
    expanded_paths: HashMap<PathBuf, bool>,
}

impl FileTree {
    pub fn new() -> Self {
        Self {
            root: None,
            expanded_paths: HashMap::new(),
        }
    }
    
    /// Set the root directory
    pub fn set_root(&mut self, path: PathBuf) {
        let mut root = FileNode::from_path(path);
        root.is_expanded = true;
        root.load_children();
        self.root = Some(root);
    }
    
    /// Show the file tree and return selected file path
    pub fn show(&mut self, ui: &mut Ui) -> Option<PathBuf> {
        let mut selected = None;
        
        if let Some(root) = self.root.take() {
            let mut root = root;
            egui::ScrollArea::vertical()
                .auto_shrink([false; 2])
                .show(ui, |ui| {
                    selected = Self::show_node_static(ui, &mut root, 0);
                });
            self.root = Some(root);
        } else {
            ui.vertical_centered(|ui| {
                ui.label("No folder open");
                ui.add_space(10.0);
                if ui.button("Open Folder").clicked() {
                    if let Some(path) = rfd::FileDialog::new().pick_folder() {
                        self.set_root(path);
                    }
                }
            });
        }
        
        selected
    }
    
    fn show_node_static(ui: &mut Ui, node: &mut FileNode, depth: usize) -> Option<PathBuf> {
        let mut selected = None;
        let indent = depth as f32 * 16.0;
        
        ui.horizontal(|ui| {
            ui.add_space(indent);
            
            if node.is_dir {
                // Directory
                let icon = if node.is_expanded { "▼" } else { "▶" };
                let folder_icon = if node.is_expanded { "📂" } else { "📁" };
                
                if ui.small_button(icon).clicked() {
                    node.is_expanded = !node.is_expanded;
                    if node.is_expanded {
                        node.load_children();
                    }
                }
                
                ui.label(folder_icon);
                ui.label(&node.name);
            } else {
                // File
                ui.add_space(18.0); // Align with folder expand button
                
                let icon = get_file_icon(&node.name);
                ui.label(icon);
                
                if ui.selectable_label(false, &node.name).clicked() {
                    selected = Some(node.path.clone());
                }
            }
        });
        
        // Show children if expanded
        if node.is_dir && node.is_expanded {
            for child in &mut node.children {
                if let Some(path) = Self::show_node_static(ui, child, depth + 1) {
                    selected = Some(path);
                }
            }
        }
        
        selected
    }
}

/// Get icon for file based on extension
fn get_file_icon(name: &str) -> &'static str {
    let ext = name.rsplit('.').next().unwrap_or("");
    
    match ext.to_lowercase().as_str() {
        "rs" => "🦀",
        "py" => "🐍",
        "js" | "mjs" => "📜",
        "ts" => "📘",
        "jsx" | "tsx" => "⚛️",
        "html" | "htm" => "🌐",
        "css" | "scss" | "sass" => "🎨",
        "json" => "📋",
        "md" => "📝",
        "txt" => "📄",
        "yaml" | "yml" => "⚙️",
        "toml" => "⚙️",
        "xml" => "📰",
        "png" | "jpg" | "jpeg" | "gif" | "svg" | "ico" => "🖼️",
        "mp3" | "wav" | "ogg" => "🎵",
        "mp4" | "webm" | "avi" => "🎬",
        "zip" | "tar" | "gz" | "rar" => "📦",
        "pdf" => "📕",
        "doc" | "docx" => "📘",
        "xls" | "xlsx" => "📗",
        "ppt" | "pptx" => "📙",
        "exe" | "msi" => "⚡",
        "dll" | "so" | "dylib" => "🔧",
        "sh" | "bash" => "🖥️",
        "ps1" => "💠",
        "bat" | "cmd" => "🖥️",
        "gitignore" | "gitattributes" => "📌",
        "lock" => "🔒",
        "env" => "🔐",
        _ => "📄",
    }
}
