//! Git operations using git2-rs
//! 
//! Provides native Git functionality for repository operations.

use napi::bindgen_prelude::*;
use git2::{Repository, StatusOptions, Signature, DiffOptions, DiffFormat};
use std::path::Path;
use serde::{Deserialize, Serialize};
use crate::error::ValyxoError;

/// Git status entry
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct GitStatusEntry {
    pub path: String,
    pub status: String,
    pub staged: bool,
}

/// Git commit info
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct GitCommitInfo {
    pub id: String,
    pub message: String,
    pub author: String,
    pub email: String,
    pub time: i64,
}

/// Git branch info
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct GitBranchInfo {
    pub name: String,
    pub is_head: bool,
    pub is_remote: bool,
    pub commit_id: String,
}

/// Git diff info
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct GitDiffInfo {
    pub files_changed: u32,
    pub insertions: u32,
    pub deletions: u32,
    pub diff_text: String,
}

/// Git repository info
#[napi(object)]
#[derive(Clone, Serialize, Deserialize)]
pub struct GitRepoInfo {
    pub path: String,
    pub is_bare: bool,
    pub is_empty: bool,
    pub head_branch: Option<String>,
    pub head_commit: Option<String>,
}

/// Check if path is a git repository
#[napi]
pub fn is_git_repo(path: String) -> bool {
    Repository::discover(&path).is_ok()
}

/// Get repository info
#[napi]
pub fn get_repo_info(path: String) -> Result<GitRepoInfo> {
    let repo = Repository::discover(&path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let head_branch = repo.head()
        .ok()
        .and_then(|h| h.shorthand().map(|s| s.to_string()));
    
    let head_commit = repo.head()
        .ok()
        .and_then(|h| h.target().map(|oid| oid.to_string()));
    
    Ok(GitRepoInfo {
        path: repo.path().to_string_lossy().to_string(),
        is_bare: repo.is_bare(),
        is_empty: repo.is_empty().unwrap_or(true),
        head_branch,
        head_commit,
    })
}

/// Get repository status
#[napi]
pub fn git_status(path: String) -> Result<Vec<GitStatusEntry>> {
    let repo = Repository::discover(&path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let mut opts = StatusOptions::new();
    opts.include_untracked(true);
    opts.include_ignored(false);
    opts.recurse_untracked_dirs(true);
    
    let statuses = repo.statuses(Some(&mut opts))
        .map_err(|e| ValyxoError::Git(e))?;
    
    let entries: Vec<GitStatusEntry> = statuses.iter()
        .filter_map(|entry| {
            let path = entry.path()?.to_string();
            let status = entry.status();
            
            let status_str = if status.is_index_new() {
                "added"
            } else if status.is_index_modified() {
                "modified"
            } else if status.is_index_deleted() {
                "deleted"
            } else if status.is_wt_new() {
                "untracked"
            } else if status.is_wt_modified() {
                "modified"
            } else if status.is_wt_deleted() {
                "deleted"
            } else if status.is_conflicted() {
                "conflicted"
            } else {
                return None;
            };
            
            let staged = status.is_index_new() || 
                        status.is_index_modified() || 
                        status.is_index_deleted();
            
            Some(GitStatusEntry {
                path,
                status: status_str.to_string(),
                staged,
            })
        })
        .collect();
    
    Ok(entries)
}

/// Stage files
#[napi]
pub fn git_add(repo_path: String, files: Vec<String>) -> Result<u32> {
    let repo = Repository::discover(&repo_path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let mut index = repo.index()
        .map_err(|e| ValyxoError::Git(e))?;
    
    let mut count = 0;
    for file in &files {
        if file == "." {
            // Add all
            index.add_all(["."].iter(), git2::IndexAddOption::DEFAULT, None)
                .map_err(|e| ValyxoError::Git(e))?;
            count = 999; // Indicate all
            break;
        } else {
            let path = Path::new(file);
            index.add_path(path)
                .map_err(|e| ValyxoError::Git(e))?;
            count += 1;
        }
    }
    
    index.write()
        .map_err(|e| ValyxoError::Git(e))?;
    
    Ok(count)
}

/// Unstage files
#[napi]
pub fn git_unstage(repo_path: String, files: Vec<String>) -> Result<u32> {
    let repo = Repository::discover(&repo_path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let head = repo.head()
        .map_err(|e| ValyxoError::Git(e))?
        .peel_to_tree()
        .map_err(|e| ValyxoError::Git(e))?;
    
    let mut count = 0;
    for file in &files {
        repo.reset_default(Some(head.as_object()), [file.as_str()])
            .map_err(|e| ValyxoError::Git(e))?;
        count += 1;
    }
    
    Ok(count)
}

/// Create a commit
#[napi]
pub fn git_commit(
    repo_path: String,
    message: String,
    author_name: Option<String>,
    author_email: Option<String>,
) -> Result<String> {
    let repo = Repository::discover(&repo_path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let mut index = repo.index()
        .map_err(|e| ValyxoError::Git(e))?;
    
    let tree_id = index.write_tree()
        .map_err(|e| ValyxoError::Git(e))?;
    
    let tree = repo.find_tree(tree_id)
        .map_err(|e| ValyxoError::Git(e))?;
    
    // Get signature
    let name = author_name.unwrap_or_else(|| "Valyxo User".to_string());
    let email = author_email.unwrap_or_else(|| "user@valyxo.app".to_string());
    
    let signature = Signature::now(&name, &email)
        .map_err(|e| ValyxoError::Git(e))?;
    
    // Get parent commit if exists
    let parent = repo.head()
        .ok()
        .and_then(|h| h.target())
        .and_then(|oid| repo.find_commit(oid).ok());
    
    let parents: Vec<&git2::Commit> = parent.as_ref().map(|p| vec![p]).unwrap_or_default();
    
    let commit_id = repo.commit(
        Some("HEAD"),
        &signature,
        &signature,
        &message,
        &tree,
        &parents,
    ).map_err(|e| ValyxoError::Git(e))?;
    
    Ok(commit_id.to_string())
}

/// Get commit log
#[napi]
pub fn git_log(repo_path: String, max_count: Option<u32>) -> Result<Vec<GitCommitInfo>> {
    let repo = Repository::discover(&repo_path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let max = max_count.unwrap_or(50) as usize;
    
    let mut revwalk = repo.revwalk()
        .map_err(|e| ValyxoError::Git(e))?;
    
    revwalk.push_head()
        .map_err(|e| ValyxoError::Git(e))?;
    
    let commits: Vec<GitCommitInfo> = revwalk
        .take(max)
        .filter_map(|oid| oid.ok())
        .filter_map(|oid| repo.find_commit(oid).ok())
        .map(|commit| {
            GitCommitInfo {
                id: commit.id().to_string(),
                message: commit.message().unwrap_or("").to_string(),
                author: commit.author().name().unwrap_or("").to_string(),
                email: commit.author().email().unwrap_or("").to_string(),
                time: commit.time().seconds(),
            }
        })
        .collect();
    
    Ok(commits)
}

/// Get branches
#[napi]
pub fn git_branches(repo_path: String, include_remote: bool) -> Result<Vec<GitBranchInfo>> {
    let repo = Repository::discover(&repo_path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let filter = if include_remote {
        git2::BranchType::Local // We'll add remote separately
    } else {
        git2::BranchType::Local
    };
    
    let mut branches_list = Vec::new();
    
    // Local branches
    let branches = repo.branches(Some(filter))
        .map_err(|e| ValyxoError::Git(e))?;
    
    for branch_result in branches {
        if let Ok((branch, _branch_type)) = branch_result {
            let name = branch.name()
                .ok()
                .flatten()
                .map(|s| s.to_string())
                .unwrap_or_default();
            
            let is_head = branch.is_head();
            let commit_id = branch.get()
                .target()
                .map(|oid| oid.to_string())
                .unwrap_or_default();
            
            branches_list.push(GitBranchInfo {
                name,
                is_head,
                is_remote: false,
                commit_id,
            });
        }
    }
    
    // Remote branches
    if include_remote {
        if let Ok(remote_branches) = repo.branches(Some(git2::BranchType::Remote)) {
            for branch_result in remote_branches {
                if let Ok((branch, _)) = branch_result {
                    let name = branch.name()
                        .ok()
                        .flatten()
                        .map(|s| s.to_string())
                        .unwrap_or_default();
                    
                    let commit_id = branch.get()
                        .target()
                        .map(|oid| oid.to_string())
                        .unwrap_or_default();
                    
                    branches_list.push(GitBranchInfo {
                        name,
                        is_head: false,
                        is_remote: true,
                        commit_id,
                    });
                }
            }
        }
    }
    
    Ok(branches_list)
}

/// Create a new branch
#[napi]
pub fn git_create_branch(repo_path: String, name: String, checkout: bool) -> Result<()> {
    let repo = Repository::discover(&repo_path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let head = repo.head()
        .map_err(|e| ValyxoError::Git(e))?
        .peel_to_commit()
        .map_err(|e| ValyxoError::Git(e))?;
    
    let branch = repo.branch(&name, &head, false)
        .map_err(|e| ValyxoError::Git(e))?;
    
    if checkout {
        let refname = branch.get().name()
            .ok_or_else(|| ValyxoError::Git(git2::Error::from_str("Invalid branch name")))?;
        
        repo.set_head(refname)
            .map_err(|e| ValyxoError::Git(e))?;
        
        repo.checkout_head(Some(git2::build::CheckoutBuilder::new().force()))
            .map_err(|e| ValyxoError::Git(e))?;
    }
    
    Ok(())
}

/// Checkout a branch
#[napi]
pub fn git_checkout(repo_path: String, branch_name: String) -> Result<()> {
    let repo = Repository::discover(&repo_path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let refname = format!("refs/heads/{}", branch_name);
    
    repo.set_head(&refname)
        .map_err(|e| ValyxoError::Git(e))?;
    
    repo.checkout_head(Some(git2::build::CheckoutBuilder::new().force()))
        .map_err(|e| ValyxoError::Git(e))?;
    
    Ok(())
}

/// Get diff
#[napi]
pub fn git_diff(repo_path: String, staged: bool) -> Result<GitDiffInfo> {
    let repo = Repository::discover(&repo_path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let mut opts = DiffOptions::new();
    opts.include_untracked(true);
    
    let diff = if staged {
        let tree = repo.head()
            .ok()
            .and_then(|h| h.peel_to_tree().ok());
        
        repo.diff_tree_to_index(tree.as_ref(), None, Some(&mut opts))
            .map_err(|e| ValyxoError::Git(e))?
    } else {
        repo.diff_index_to_workdir(None, Some(&mut opts))
            .map_err(|e| ValyxoError::Git(e))?
    };
    
    let stats = diff.stats()
        .map_err(|e| ValyxoError::Git(e))?;
    
    let mut diff_text = String::new();
    diff.print(DiffFormat::Patch, |_delta, _hunk, line| {
        let prefix = match line.origin() {
            '+' => "+",
            '-' => "-",
            ' ' => " ",
            _ => "",
        };
        diff_text.push_str(prefix);
        diff_text.push_str(std::str::from_utf8(line.content()).unwrap_or(""));
        true
    }).map_err(|e| ValyxoError::Git(e))?;
    
    Ok(GitDiffInfo {
        files_changed: stats.files_changed() as u32,
        insertions: stats.insertions() as u32,
        deletions: stats.deletions() as u32,
        diff_text,
    })
}

/// Initialize a new repository
#[napi]
pub fn git_init(path: String) -> Result<String> {
    let repo = Repository::init(&path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    Ok(repo.path().to_string_lossy().to_string())
}

/// Clone a repository
#[napi]
pub fn git_clone(url: String, path: String) -> Result<String> {
    let repo = Repository::clone(&url, &path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    Ok(repo.path().to_string_lossy().to_string())
}

/// Get current branch name
#[napi]
pub fn git_current_branch(repo_path: String) -> Result<Option<String>> {
    let repo = Repository::discover(&repo_path)
        .map_err(|e| ValyxoError::Git(e))?;
    
    let head = repo.head().ok();
    
    Ok(head.and_then(|h| h.shorthand().map(|s| s.to_string())))
}
