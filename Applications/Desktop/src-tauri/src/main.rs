#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[tauri::command]
fn get_app_version() -> String {
    "0.6.0".to_string()
}

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let window = app.get_window("main").unwrap();
            
            // Open dev tools in debug mode
            #[cfg(debug_assertions)]
            window.open_devtools();
            
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![greet, get_app_version])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
