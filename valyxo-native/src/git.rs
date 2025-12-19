//! Git integration

use git2::Repository;
use std::path::Path;
use anyhow::Result;

/// Git status for a repository
pub struct GitStatus {
    pub branch: String,
    pub changed_files: usize,
    pub staged_files: usize,
    pub untracked_files: usize,
}

impl GitStatus {
    /// Get git status from a path
    pub fn from_path(path: &Path) -> Result<Self> {
        let repo = Repository::discover(path)?;
        
        let head = repo.head()?;
        let branch = head.shorthand()
            .map(|s| s.to_string())
            .unwrap_or_else(|| "HEAD".to_string());
        
        let mut opts = git2::StatusOptions::new();
        opts.include_untracked(true);
        opts.recurse_untracked_dirs(true);
        
        let statuses = repo.statuses(Some(&mut opts))?;
        
        let mut changed_files = 0;
        let mut staged_files = 0;
        let mut untracked_files = 0;
        
        for entry in statuses.iter() {
            let status = entry.status();
            
            if status.is_index_new() || status.is_index_modified() || status.is_index_deleted() {
                staged_files += 1;
            }
            
            if status.is_wt_modified() || status.is_wt_deleted() {
                changed_files += 1;
            }
            
            if status.is_wt_new() {
                untracked_files += 1;
            }
        }
        
        Ok(GitStatus {
            branch,
            changed_files,
            staged_files,
            untracked_files,
        })
    }
}
