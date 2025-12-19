//! Valyxo Native Backend
//! 
//! High-performance Rust modules exposed to Electron via NAPI-RS.
//! Provides fast file operations, terminal emulation, git integration,
//! and more for the Valyxo desktop application.

#[macro_use]
extern crate napi_derive;

pub mod file_ops;
pub mod terminal;
pub mod settings;
pub mod indexer;
pub mod git;
pub mod process;
pub mod error;

use napi::bindgen_prelude::*;
use tracing_subscriber;

/// Initialize the native backend
#[napi]
pub fn init_native_backend() -> Result<String> {
    // Initialize tracing for logging
    let _ = tracing_subscriber::fmt()
        .with_env_filter("valyxo_native=info")
        .try_init();
    
    tracing::info!("Valyxo Native Backend initialized");
    
    Ok("Valyxo Native Backend v0.5.2 ready".to_string())
}

/// Get version info
#[napi]
pub fn get_version() -> String {
    format!(
        "Valyxo Native v{} (Rust {})",
        env!("CARGO_PKG_VERSION"),
        rustc_version()
    )
}

fn rustc_version() -> &'static str {
    "1.75+"
}

/// Health check
#[napi]
pub fn health_check() -> Result<bool> {
    Ok(true)
}
