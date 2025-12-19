//! Valyxo - The Fastest Code Editor
//!
//! A high-performance code editor built in Rust with GPU-accelerated rendering.

// Hide console window on Windows
#![windows_subsystem = "windows"]

mod app;
mod editor;
mod buffer;
mod syntax;
mod file_tree;
mod tabs;
mod command_palette;
mod theme;
mod config;
mod git;
mod keybindings;

use app::ValyxoApp;
use eframe::egui;

fn main() -> eframe::Result<()> {
    // Configure native options for best performance
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_title("Valyxo")
            .with_inner_size([1400.0, 900.0])
            .with_min_inner_size([800.0, 600.0])
            .with_icon(load_icon()),
        
        // Use wgpu for GPU-accelerated rendering
        renderer: eframe::Renderer::Wgpu,
        
        // VSync for smooth rendering
        vsync: true,
        
        // Hardware acceleration
        hardware_acceleration: eframe::HardwareAcceleration::Required,
        
        // Multisampling for smoother text
        multisampling: 4,
        
        // Persist window state
        persist_window: true,
        
        ..Default::default()
    };

    eframe::run_native(
        "Valyxo",
        options,
        Box::new(|cc| Ok(Box::new(ValyxoApp::new(cc)))),
    )
}

fn load_icon() -> egui::IconData {
    // Load icon from embedded bytes
    let icon_bytes = include_bytes!("../assets/icon.png");
    
    if let Ok(image) = image::load_from_memory(icon_bytes) {
        let rgba = image.to_rgba8();
        let (width, height) = rgba.dimensions();
        egui::IconData {
            rgba: rgba.into_raw(),
            width,
            height,
        }
    } else {
        egui::IconData::default()
    }
}
