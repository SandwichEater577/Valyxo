//! Custom error types for the native backend

use napi::bindgen_prelude::*;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ValyxoError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("Git error: {0}")]
    Git(#[from] git2::Error),
    
    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),
    
    #[error("Path error: {0}")]
    Path(String),
    
    #[error("Terminal error: {0}")]
    Terminal(String),
    
    #[error("Process error: {0}")]
    Process(String),
    
    #[error("Config error: {0}")]
    Config(String),
    
    #[error("Not found: {0}")]
    NotFound(String),
    
    #[error("Permission denied: {0}")]
    PermissionDenied(String),
    
    #[error("Invalid operation: {0}")]
    InvalidOperation(String),
}

impl From<ValyxoError> for napi::Error {
    fn from(err: ValyxoError) -> Self {
        napi::Error::from_reason(err.to_string())
    }
}

pub type ValyxoResult<T> = std::result::Result<T, ValyxoError>;
