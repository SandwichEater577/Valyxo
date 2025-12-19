//! File indexer for fast search
//! 
//! Builds an in-memory index of files for fast symbol/text search
//! with support for gitignore patterns.

use napi::bindgen_prelude::*;
use std::path::{Path, PathBuf};
use std::fs;
use ignore::WalkBuilder;
use serde::{Deserialize, Serialize};
use dashmap::DashMap;
use parking_lot::RwLock;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use rayon::prelude::*;
use crate::error::ValyxoError;

/// Index entry for a file
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct IndexEntry {
    pub path: String,
    pub name: String,
    pub extension: Option<String>,
    pub size: i64,
    pub modified: i64,
    pub symbols: Vec<String>,
}

/// Index statistics
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct IndexStats {
    pub total_files: u32,
    pub total_size: i64,
    pub indexed_at: i64,
    pub root_path: String,
    pub is_indexing: bool,
}

/// File match result
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct FileMatch {
    pub path: String,
    pub name: String,
    pub score: f64,
    pub extension: Option<String>,
}

// Global index storage
lazy_static::lazy_static! {
    static ref INDEX: Arc<RwLock<FileIndex>> = Arc::new(RwLock::new(FileIndex::default()));
}

#[derive(Default)]
struct FileIndex {
    root: Option<PathBuf>,
    entries: DashMap<String, IndexEntry>,
    is_indexing: Arc<AtomicBool>,
    total_size: Arc<AtomicU64>,
    indexed_at: i64,
}

/// Start indexing a directory
#[napi]
pub fn start_indexing(root_path: String, respect_gitignore: bool) -> Result<()> {
    let root = PathBuf::from(&root_path);
    
    if !root.exists() {
        return Err(ValyxoError::NotFound(format!("Directory not found: {:?}", root)).into());
    }
    
    {
        let mut index = INDEX.write();
        index.root = Some(root.clone());
        index.entries.clear();
        index.is_indexing.store(true, Ordering::SeqCst);
        index.total_size.store(0, Ordering::SeqCst);
    }
    
    // Build walker with gitignore support
    let walker = WalkBuilder::new(&root)
        .git_ignore(respect_gitignore)
        .git_global(respect_gitignore)
        .git_exclude(respect_gitignore)
        .hidden(false)
        .build();
    
    // Collect all file paths first
    let entries: Vec<PathBuf> = walker
        .filter_map(|e| e.ok())
        .filter(|e| e.file_type().map(|ft| ft.is_file()).unwrap_or(false))
        .map(|e| e.path().to_path_buf())
        .collect();
    
    // Index files in parallel
    let index_ref = INDEX.read();
    
    entries.par_iter().for_each(|path| {
        if let Ok(entry) = create_index_entry(path) {
            index_ref.total_size.fetch_add(entry.size as u64, Ordering::SeqCst);
            index_ref.entries.insert(path.to_string_lossy().to_string(), entry);
        }
    });
    
    drop(index_ref);
    
    // Update indexing state
    {
        let mut index = INDEX.write();
        index.is_indexing.store(false, Ordering::SeqCst);
        index.indexed_at = chrono::Utc::now().timestamp();
    }
    
    let index = INDEX.read();
    tracing::info!("Indexed {} files in {:?}", index.entries.len(), root);
    
    Ok(())
}

fn create_index_entry(path: &Path) -> std::result::Result<IndexEntry, ValyxoError> {
    let metadata = fs::metadata(path)?;
    
    let modified = metadata.modified()
        .map(|t| t.duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs() as i64)
        .unwrap_or(0);
    
    // Extract basic symbols from file (simplified)
    let symbols = extract_symbols(path);
    
    Ok(IndexEntry {
        path: path.to_string_lossy().to_string(),
        name: path.file_name()
            .map(|n| n.to_string_lossy().to_string())
            .unwrap_or_default(),
        extension: path.extension().map(|e| e.to_string_lossy().to_string()),
        size: metadata.len() as i64,
        modified,
        symbols,
    })
}

fn extract_symbols(path: &Path) -> Vec<String> {
    let mut symbols = Vec::new();
    
    // Only extract symbols from code files
    let ext = path.extension()
        .map(|e| e.to_string_lossy().to_lowercase())
        .unwrap_or_default();
    
    let code_extensions = ["js", "ts", "py", "rs", "go", "java", "c", "cpp", "h", "hpp", "rb", "php"];
    
    if !code_extensions.contains(&ext.as_str()) {
        return symbols;
    }
    
    // Read file and extract function/class names
    if let Ok(content) = fs::read_to_string(path) {
        let patterns = [
            (regex::Regex::new(r"(?m)^(?:export\s+)?(?:async\s+)?function\s+(\w+)").ok(), "fn"),
            (regex::Regex::new(r"(?m)^(?:export\s+)?class\s+(\w+)").ok(), "class"),
            (regex::Regex::new(r"(?m)^def\s+(\w+)").ok(), "fn"),
            (regex::Regex::new(r"(?m)^class\s+(\w+)").ok(), "class"),
            (regex::Regex::new(r"(?m)^fn\s+(\w+)").ok(), "fn"),
            (regex::Regex::new(r"(?m)^struct\s+(\w+)").ok(), "struct"),
            (regex::Regex::new(r"(?m)^impl\s+(\w+)").ok(), "impl"),
        ];
        
        for (pattern, _kind) in patterns {
            if let Some(re) = pattern {
                for cap in re.captures_iter(&content) {
                    if let Some(name) = cap.get(1) {
                        symbols.push(name.as_str().to_string());
                    }
                }
            }
        }
    }
    
    symbols
}

/// Get index statistics
#[napi]
pub fn get_index_stats() -> IndexStats {
    let index = INDEX.read();
    
    IndexStats {
        total_files: index.entries.len() as u32,
        total_size: index.total_size.load(Ordering::SeqCst) as i64,
        indexed_at: index.indexed_at,
        root_path: index.root.as_ref()
            .map(|p| p.to_string_lossy().to_string())
            .unwrap_or_default(),
        is_indexing: index.is_indexing.load(Ordering::SeqCst),
    }
}

/// Search for files by name (fuzzy match)
#[napi]
pub fn search_files(query: String, max_results: Option<u32>) -> Vec<FileMatch> {
    let index = INDEX.read();
    let max = max_results.unwrap_or(50) as usize;
    let query_lower = query.to_lowercase();
    
    let mut matches: Vec<FileMatch> = index.entries.iter()
        .filter_map(|entry| {
            let e = entry.value();
            let name_lower = e.name.to_lowercase();
            
            // Calculate match score
            let score = if name_lower == query_lower {
                1.0
            } else if name_lower.starts_with(&query_lower) {
                0.9
            } else if name_lower.contains(&query_lower) {
                0.7
            } else if fuzzy_match(&name_lower, &query_lower) {
                0.5
            } else {
                return None;
            };
            
            Some(FileMatch {
                path: e.path.clone(),
                name: e.name.clone(),
                score,
                extension: e.extension.clone(),
            })
        })
        .collect();
    
    // Sort by score descending
    matches.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap_or(std::cmp::Ordering::Equal));
    matches.truncate(max);
    
    matches
}

fn fuzzy_match(text: &str, pattern: &str) -> bool {
    let mut pattern_chars = pattern.chars().peekable();
    
    for c in text.chars() {
        if let Some(&pc) = pattern_chars.peek() {
            if c == pc {
                pattern_chars.next();
            }
        } else {
            break;
        }
    }
    
    pattern_chars.peek().is_none()
}

/// Search for symbols in indexed files
#[napi]
pub fn search_symbols(query: String, max_results: Option<u32>) -> Vec<FileMatch> {
    let index = INDEX.read();
    let max = max_results.unwrap_or(50) as usize;
    let query_lower = query.to_lowercase();
    
    let mut matches: Vec<FileMatch> = index.entries.iter()
        .filter_map(|entry| {
            let e = entry.value();
            
            // Check if any symbol matches
            let matching_symbol = e.symbols.iter()
                .find(|s| s.to_lowercase().contains(&query_lower));
            
            if let Some(symbol) = matching_symbol {
                Some(FileMatch {
                    path: e.path.clone(),
                    name: symbol.clone(),
                    score: if symbol.to_lowercase() == query_lower { 1.0 } else { 0.7 },
                    extension: e.extension.clone(),
                })
            } else {
                None
            }
        })
        .collect();
    
    matches.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap_or(std::cmp::Ordering::Equal));
    matches.truncate(max);
    
    matches
}

/// Get all indexed files
#[napi]
pub fn get_all_indexed_files() -> Vec<IndexEntry> {
    let index = INDEX.read();
    
    index.entries.iter()
        .map(|e| e.value().clone())
        .collect()
}

/// Get files by extension
#[napi]
pub fn get_files_by_extension(extension: String) -> Vec<IndexEntry> {
    let index = INDEX.read();
    let ext_lower = extension.to_lowercase();
    
    index.entries.iter()
        .filter(|e| {
            e.value().extension.as_ref()
                .map(|e| e.to_lowercase() == ext_lower)
                .unwrap_or(false)
        })
        .map(|e| e.value().clone())
        .collect()
}

/// Clear the index
#[napi]
pub fn clear_index() -> Result<()> {
    let mut index = INDEX.write();
    index.entries.clear();
    index.root = None;
    index.total_size.store(0, Ordering::SeqCst);
    index.indexed_at = 0;
    
    tracing::info!("Index cleared");
    
    Ok(())
}

/// Refresh index (re-index changed files)
#[napi]
pub fn refresh_index() -> Result<u32> {
    let index = INDEX.read();
    
    let root = index.root.as_ref()
        .ok_or_else(|| ValyxoError::Config("No index root set".to_string()))?
        .clone();
    
    drop(index);
    
    // Re-index
    start_indexing(root.to_string_lossy().to_string(), true)?;
    
    let index = INDEX.read();
    Ok(index.entries.len() as u32)
}
