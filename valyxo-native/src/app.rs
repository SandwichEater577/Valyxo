//! Main application state and UI

use crate::buffer::BufferManager;
use crate::command_palette::CommandPalette;
use crate::config::Config;
use crate::editor::Editor;
use crate::file_tree::FileTree;
use crate::git::GitStatus;
use crate::keybindings::Keybindings;
use crate::syntax::SyntaxHighlighter;
use crate::tabs::TabBar;
use crate::theme::{Theme, available_themes};
use eframe::egui::{self, Context, Key, FontFamily, FontId};
use std::path::PathBuf;
use std::sync::Arc;
use std::time::Instant;

/// Main application state
pub struct ValyxoApp {
    /// Current theme
    theme: Theme,
    
    /// Current theme index
    theme_index: usize,
    
    /// Application configuration
    config: Config,
    
    /// File tree panel
    file_tree: FileTree,
    
    /// Tab bar for open files
    tab_bar: TabBar,
    
    /// Buffer manager for all open files
    buffers: BufferManager,
    
    /// Syntax highlighter
    syntax: Arc<SyntaxHighlighter>,
    
    /// Command palette
    command_palette: CommandPalette,
    
    /// Key bindings
    keybindings: Keybindings,
    
    /// Git status for current workspace
    git_status: Option<GitStatus>,
    
    /// Current workspace path
    workspace: Option<PathBuf>,
    
    /// Show file tree panel
    show_file_tree: bool,
    
    /// Show command palette
    show_command_palette: bool,
    
    /// Status bar message
    status_message: String,
    
    /// Line wrap toggle
    line_wrap: bool,
    
    /// Font size
    font_size: f32,
    
    /// Start time for animations
    start_time: Instant,
    
    /// Show minimap
    show_minimap: bool,
}

impl ValyxoApp {
    pub fn new(cc: &eframe::CreationContext<'_>) -> Self {
        // Configure custom fonts
        let mut fonts = egui::FontDefinitions::default();
        
        // Add JetBrains Mono for code editing
        fonts.font_data.insert(
            "JetBrains Mono".to_owned(),
            egui::FontData::from_static(include_bytes!("../assets/fonts/JetBrainsMono-Regular.ttf")),
        );
        
        // Set as default monospace font
        fonts.families
            .get_mut(&FontFamily::Monospace)
            .unwrap()
            .insert(0, "JetBrains Mono".to_owned());
        
        // Also use for proportional for consistency
        fonts.families
            .get_mut(&FontFamily::Proportional)
            .unwrap()
            .insert(0, "JetBrains Mono".to_owned());
        
        cc.egui_ctx.set_fonts(fonts);
        
        // Load theme
        let theme = Theme::dark();
        theme.apply(&cc.egui_ctx);
        
        // Configure style for better UI
        let mut style = (*cc.egui_ctx.style()).clone();
        style.spacing.item_spacing = egui::vec2(8.0, 6.0);
        style.spacing.button_padding = egui::vec2(8.0, 4.0);
        style.spacing.window_margin = egui::Margin::same(12.0);
        style.visuals.window_rounding = egui::Rounding::same(8.0);
        style.visuals.menu_rounding = egui::Rounding::same(6.0);
        style.visuals.widgets.noninteractive.rounding = egui::Rounding::same(4.0);
        style.visuals.widgets.inactive.rounding = egui::Rounding::same(4.0);
        style.visuals.widgets.hovered.rounding = egui::Rounding::same(4.0);
        style.visuals.widgets.active.rounding = egui::Rounding::same(4.0);
        style.animation_time = 0.15; // Smooth animations
        cc.egui_ctx.set_style(style);
        
        // Load config
        let config = Config::load().unwrap_or_default();
        
        // Initialize syntax highlighter
        let syntax = Arc::new(SyntaxHighlighter::new());
        
        Self {
            theme,
            theme_index: 0,
            config,
            file_tree: FileTree::new(),
            tab_bar: TabBar::new(),
            buffers: BufferManager::new(),
            syntax,
            command_palette: CommandPalette::new(),
            keybindings: Keybindings::default(),
            git_status: None,
            workspace: None,
            show_file_tree: true,
            show_command_palette: false,
            status_message: "Ready".to_string(),
            line_wrap: false,
            font_size: 14.0,
            start_time: Instant::now(),
            show_minimap: false,
        }
    }
    
    /// Cycle to next theme
    fn next_theme(&mut self, ctx: &Context) {
        let themes = available_themes();
        self.theme_index = (self.theme_index + 1) % themes.len();
        self.theme = themes[self.theme_index].clone();
        self.theme.apply(ctx);
        self.status_message = format!("Theme: {}", self.theme.name);
    }
    
    /// Open a folder as workspace
    pub fn open_folder(&mut self, path: PathBuf) {
        self.workspace = Some(path.clone());
        self.file_tree.set_root(path.clone());
        self.git_status = GitStatus::from_path(&path).ok();
        self.status_message = format!("📂 Opened: {}", path.display());
    }
    
    /// Open a file
    pub fn open_file(&mut self, path: PathBuf) {
        if let Ok(buffer_id) = self.buffers.open_file(&path) {
            self.tab_bar.add_tab(path.clone(), buffer_id);
            self.status_message = format!("📄 {}", path.file_name().unwrap_or_default().to_string_lossy());
        }
    }
    
    /// Save current file
    pub fn save_current(&mut self) {
        if let Some(buffer_id) = self.tab_bar.current_buffer_id() {
            if let Err(e) = self.buffers.save(buffer_id) {
                self.status_message = format!("❌ Error: {}", e);
            } else {
                self.status_message = "✓ Saved".to_string();
            }
        }
    }
    
    /// Zoom in
    fn zoom_in(&mut self, ctx: &Context) {
        self.font_size = (self.font_size + 1.0).min(32.0);
        ctx.set_pixels_per_point(ctx.pixels_per_point() * 1.1);
        self.status_message = format!("Zoom: {}%", (ctx.pixels_per_point() * 100.0) as i32);
    }
    
    /// Zoom out
    fn zoom_out(&mut self, ctx: &Context) {
        self.font_size = (self.font_size - 1.0).max(8.0);
        ctx.set_pixels_per_point((ctx.pixels_per_point() / 1.1).max(0.5));
        self.status_message = format!("Zoom: {}%", (ctx.pixels_per_point() * 100.0) as i32);
    }
    
    /// Handle keyboard shortcuts
    fn handle_shortcuts(&mut self, ctx: &Context) {
        let input = ctx.input(|i| i.clone());
        
        // Ctrl+Shift+P - Command Palette
        if input.modifiers.ctrl && input.modifiers.shift && input.key_pressed(Key::P) {
            self.show_command_palette = !self.show_command_palette;
        }
        
        // Ctrl+P - Quick Open
        if input.modifiers.ctrl && !input.modifiers.shift && input.key_pressed(Key::P) {
            self.show_command_palette = true;
            self.command_palette.set_mode_quick_open();
        }
        
        // Ctrl+S - Save
        if input.modifiers.ctrl && input.key_pressed(Key::S) {
            self.save_current();
        }
        
        // Ctrl+K T - Cycle Theme
        if input.modifiers.ctrl && input.key_pressed(Key::T) {
            self.next_theme(ctx);
        }
        
        // Ctrl++ / Ctrl+= - Zoom In
        if input.modifiers.ctrl && (input.key_pressed(Key::Equals) || input.key_pressed(Key::Plus)) {
            self.zoom_in(ctx);
        }
        
        // Ctrl+- - Zoom Out
        if input.modifiers.ctrl && input.key_pressed(Key::Minus) {
            self.zoom_out(ctx);
        }
        
        // Ctrl+O - Open File
        if input.modifiers.ctrl && input.key_pressed(Key::O) {
            if let Some(path) = rfd::FileDialog::new().pick_file() {
                self.open_file(path);
            }
        }
        
        // Ctrl+Shift+O - Open Folder
        if input.modifiers.ctrl && input.modifiers.shift && input.key_pressed(Key::O) {
            if let Some(path) = rfd::FileDialog::new().pick_folder() {
                self.open_folder(path);
            }
        }
        
        // Ctrl+W - Close Tab
        if input.modifiers.ctrl && input.key_pressed(Key::W) {
            self.tab_bar.close_current();
        }
        
        // Ctrl+B - Toggle Sidebar
        if input.modifiers.ctrl && input.key_pressed(Key::B) {
            self.show_file_tree = !self.show_file_tree;
        }
        
        // Escape - Close command palette
        if input.key_pressed(Key::Escape) {
            self.show_command_palette = false;
        }
        
        // Ctrl+Tab - Next Tab
        if input.modifiers.ctrl && input.key_pressed(Key::Tab) {
            self.tab_bar.next_tab();
        }
    }
}

impl eframe::App for ValyxoApp {
    fn update(&mut self, ctx: &Context, _frame: &mut eframe::Frame) {
        // Handle keyboard shortcuts
        self.handle_shortcuts(ctx);
        
        // Top panel - Menu bar with improved styling
        egui::TopBottomPanel::top("menu_bar")
            .exact_height(28.0)
            .show(ctx, |ui| {
            egui::menu::bar(ui, |ui| {
                ui.menu_button("📁 File", |ui| {
                    if ui.button("📄 Open File          Ctrl+O").clicked() {
                        if let Some(path) = rfd::FileDialog::new().pick_file() {
                            self.open_file(path);
                        }
                        ui.close_menu();
                    }
                    if ui.button("📂 Open Folder    Ctrl+Shift+O").clicked() {
                        if let Some(path) = rfd::FileDialog::new().pick_folder() {
                            self.open_folder(path);
                        }
                        ui.close_menu();
                    }
                    ui.separator();
                    if ui.button("💾 Save                  Ctrl+S").clicked() {
                        self.save_current();
                        ui.close_menu();
                    }
                    ui.separator();
                    if ui.button("🚪 Exit").clicked() {
                        ctx.send_viewport_cmd(egui::ViewportCommand::Close);
                    }
                });
                
                ui.menu_button("✏️ Edit", |ui| {
                    if ui.button("↩️ Undo      Ctrl+Z").clicked() {
                        // TODO: Implement undo
                        ui.close_menu();
                    }
                    if ui.button("↪️ Redo      Ctrl+Y").clicked() {
                        // TODO: Implement redo
                        ui.close_menu();
                    }
                });
                
                ui.menu_button("👁️ View", |ui| {
                    if ui.checkbox(&mut self.show_file_tree, "📂 File Explorer (Ctrl+B)").clicked() {
                        ui.close_menu();
                    }
                    if ui.checkbox(&mut self.line_wrap, "↩️ Word Wrap").clicked() {
                        self.status_message = if self.line_wrap { "Word wrap: ON" } else { "Word wrap: OFF" }.to_string();
                        ui.close_menu();
                    }
                    if ui.checkbox(&mut self.show_minimap, "🗺️ Minimap").clicked() {
                        ui.close_menu();
                    }
                    ui.separator();
                    if ui.button("🎨 Switch Theme (Ctrl+T)").clicked() {
                        self.next_theme(ctx);
                        ui.close_menu();
                    }
                    ui.separator();
                    if ui.button("🔍 Zoom In       Ctrl++").clicked() {
                        self.zoom_in(ctx);
                        ui.close_menu();
                    }
                    if ui.button("🔍 Zoom Out     Ctrl+-").clicked() {
                        self.zoom_out(ctx);
                        ui.close_menu();
                    }
                    ui.separator();
                    if ui.button("⌘ Command Palette (Ctrl+Shift+P)").clicked() {
                        self.show_command_palette = true;
                        ui.close_menu();
                    }
                });
                
                ui.menu_button("❓ Help", |ui| {
                    if ui.button("ℹ️ About Valyxo").clicked() {
                        self.status_message = format!("Valyxo v{} - The Fastest Code Editor 🚀", env!("CARGO_PKG_VERSION"));
                        ui.close_menu();
                    }
                    if ui.button("⌨️ Keyboard Shortcuts").clicked() {
                        self.status_message = "Ctrl+O: Open | Ctrl+S: Save | Ctrl+P: Quick Open | Ctrl+T: Theme".to_string();
                        ui.close_menu();
                    }
                });
                
                // Right-aligned indicators with theme name
                ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                    ui.label(format!("🎨 {}", self.theme.name));
                    ui.separator();
                    if let Some(ref git) = self.git_status {
                        ui.label(format!("⎇ {}", git.branch));
                    }
                });
            });
        });
        
        // Bottom panel - Status bar with improved styling
        let elapsed = self.start_time.elapsed().as_secs();
        egui::TopBottomPanel::bottom("status_bar")
            .exact_height(26.0)
            .show(ctx, |ui| {
                ui.horizontal(|ui| {
                    // Status message with icon
                    ui.label(&self.status_message);
                    
                    ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                        // Session time
                        ui.label(format!("⏱️ {}:{:02}", elapsed / 60, elapsed % 60));
                        ui.separator();
                        
                        // Line/column indicator
                        if let Some(buffer_id) = self.tab_bar.current_buffer_id() {
                            if let Some(buffer) = self.buffers.get(buffer_id) {
                                ui.label(format!("📍 Ln {}, Col {}", buffer.cursor_line + 1, buffer.cursor_col + 1));
                                ui.separator();
                                ui.label(format!("📝 {}", &buffer.language));
                                ui.separator();
                            }
                        }
                        
                        // Encoding and line ending
                        ui.label("UTF-8 | LF");
                    });
                });
            });
        
        // Left panel - File tree with improved styling
        if self.show_file_tree {
            egui::SidePanel::left("file_tree")
                .default_width(260.0)
                .min_width(180.0)
                .max_width(400.0)
                .resizable(true)
                .show(ctx, |ui| {
                    ui.add_space(4.0);
                    ui.horizontal(|ui| {
                        ui.heading("📂 Explorer");
                    });
                    ui.separator();
                    ui.add_space(4.0);
                    
                    if let Some(file_path) = self.file_tree.show(ui) {
                        self.open_file(file_path);
                    }
                });
        }
        
        // Central panel - Editor
        egui::CentralPanel::default().show(ctx, |ui| {
            // Tab bar
            if let Some((action, buffer_id)) = self.tab_bar.show(ui) {
                match action {
                    crate::tabs::TabAction::Select => {
                        // Tab selected, buffer is now active
                    }
                    crate::tabs::TabAction::Close => {
                        self.buffers.close(buffer_id);
                    }
                }
            }
            
            // Editor area
            if let Some(buffer_id) = self.tab_bar.current_buffer_id() {
                if let Some(buffer) = self.buffers.get_mut(buffer_id) {
                    let syntax = Arc::clone(&self.syntax);
                    Editor::show(ui, buffer, syntax);
                }
            } else {
                // Welcome screen with better styling
                ui.centered_and_justified(|ui| {
                    ui.vertical_centered(|ui| {
                        ui.add_space(80.0);
                        
                        // Logo/title with larger font
                        ui.label(egui::RichText::new("⚡").size(64.0));
                        ui.add_space(10.0);
                        ui.label(egui::RichText::new("Valyxo").size(48.0).strong());
                        ui.add_space(8.0);
                        ui.label(egui::RichText::new("The Fastest Code Editor").size(18.0).weak());
                        
                        ui.add_space(40.0);
                        
                        // Action buttons with icons
                        ui.horizontal(|ui| {
                            ui.add_space(ui.available_width() / 2.0 - 120.0);
                            if ui.add_sized([100.0, 36.0], egui::Button::new("📄 Open File")).clicked() {
                                if let Some(path) = rfd::FileDialog::new().pick_file() {
                                    self.open_file(path);
                                }
                            }
                            ui.add_space(10.0);
                            if ui.add_sized([100.0, 36.0], egui::Button::new("📂 Open Folder")).clicked() {
                                if let Some(path) = rfd::FileDialog::new().pick_folder() {
                                    self.open_folder(path);
                                }
                            }
                        });
                        
                        ui.add_space(40.0);
                        
                        // Keyboard shortcuts hint
                        ui.label(egui::RichText::new("Quick Actions").size(14.0).strong());
                        ui.add_space(8.0);
                        ui.horizontal(|ui| {
                            ui.add_space(ui.available_width() / 2.0 - 150.0);
                            ui.label("Ctrl+O  Open File");
                        });
                        ui.horizontal(|ui| {
                            ui.add_space(ui.available_width() / 2.0 - 150.0);
                            ui.label("Ctrl+P  Quick Open");
                        });
                        ui.horizontal(|ui| {
                            ui.add_space(ui.available_width() / 2.0 - 150.0);
                            ui.label("Ctrl+T  Change Theme");
                        });
                    });
                });
            }
        });
        
        // Command palette overlay with improved styling
        if self.show_command_palette {
            egui::Window::new("⌘ Command Palette")
                .collapsible(false)
                .resizable(false)
                .anchor(egui::Align2::CENTER_TOP, [0.0, 80.0])
                .fixed_size([550.0, 420.0])
                .show(ctx, |ui| {
                    if let Some(command) = self.command_palette.show(ui, &self.workspace) {
                        self.execute_command(command);
                        self.show_command_palette = false;
                    }
                });
        }
        
        // Request repaint for smooth animations
        ctx.request_repaint();
    }
    
    fn save(&mut self, _storage: &mut dyn eframe::Storage) {
        // Save window state
    }
}

impl ValyxoApp {
    fn execute_command(&mut self, command: String) {
        match command.as_str() {
            "file.open" => {
                if let Some(path) = rfd::FileDialog::new().pick_file() {
                    self.open_file(path);
                }
            }
            "file.save" => self.save_current(),
            "view.toggle_sidebar" => self.show_file_tree = !self.show_file_tree,
            _ => {
                // Check if it's a file path
                let path = std::path::PathBuf::from(&command);
                if path.exists() && path.is_file() {
                    self.open_file(path);
                }
            }
        }
    }
}
