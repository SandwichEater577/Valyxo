/**
 * Valyxo Native Backend - Node.js Bindings
 *
 * This module provides TypeScript bindings for the Rust native backend.
 * Import and use in Electron main process.
 */

// Try to load the native module
let native;
try {
  native = require("./valyxo-native.node");
} catch (e) {
  console.warn(
    "Native backend not available, falling back to JS implementation"
  );
  native = null;
}

// ============================================================================
// Core Functions
// ============================================================================

/**
 * Initialize the native backend
 */
export function initNativeBackend() {
  if (!native) return "Native backend not available";
  return native.initNativeBackend();
}

/**
 * Get version info
 */
export function getVersion() {
  if (!native) return "Valyxo Native (JS Fallback)";
  return native.getVersion();
}

/**
 * Health check
 */
export function healthCheck() {
  if (!native) return false;
  return native.healthCheck();
}

// ============================================================================
// File Operations
// ============================================================================

export const fileOps = {
  /**
   * Read file contents (fast, uses mmap for large files)
   */
  readFile(path) {
    if (!native) return require("fs").readFileSync(path, "utf8");
    return native.readFileFast(path);
  },

  /**
   * Read file as bytes
   */
  readFileBytes(path) {
    if (!native) return require("fs").readFileSync(path);
    return native.readFileBytes(path);
  },

  /**
   * Write file (atomic operation)
   */
  writeFile(path, content) {
    if (!native) return require("fs").writeFileSync(path, content);
    return native.writeFileFast(path, content);
  },

  /**
   * Write bytes to file
   */
  writeFileBytes(path, content) {
    if (!native) return require("fs").writeFileSync(path, content);
    return native.writeFileBytes(path, content);
  },

  /**
   * Get file info
   */
  getFileInfo(path) {
    if (!native) {
      const fs = require("fs");
      const stats = fs.statSync(path);
      const parsed = require("path").parse(path);
      return {
        path,
        name: parsed.base,
        size: stats.size,
        isDir: stats.isDirectory(),
        isFile: stats.isFile(),
        isSymlink: stats.isSymbolicLink(),
        modified: Math.floor(stats.mtimeMs / 1000),
        created: Math.floor(stats.ctimeMs / 1000),
        extension: parsed.ext ? parsed.ext.slice(1) : null,
      };
    }
    return native.getFileInfo(path);
  },

  /**
   * List directory contents
   */
  listDirectory(path, recursive = false) {
    if (!native) {
      const fs = require("fs");
      const entries = fs.readdirSync(path, { withFileTypes: true });
      return entries.map((e) => ({
        path: require("path").join(path, e.name),
        name: e.name,
        isDir: e.isDirectory(),
        isFile: e.isFile(),
      }));
    }
    return native.listDirectory(path, recursive);
  },

  /**
   * Search for text in files
   */
  searchInFiles(directory, pattern, filePattern = null, maxResults = 1000) {
    if (!native) throw new Error("Native backend required for file search");
    return native.searchInFiles(directory, pattern, filePattern, maxResults);
  },

  /**
   * Create directory
   */
  createDirectory(path) {
    if (!native) return require("fs").mkdirSync(path, { recursive: true });
    return native.createDirectory(path);
  },

  /**
   * Delete file or directory
   */
  deletePath(path, recursive = false) {
    if (!native) {
      const fs = require("fs");
      if (fs.statSync(path).isDirectory()) {
        fs.rmSync(path, { recursive });
      } else {
        fs.unlinkSync(path);
      }
      return;
    }
    return native.deletePath(path, recursive);
  },

  /**
   * Copy file or directory
   */
  copyPath(source, destination) {
    if (!native) throw new Error("Native backend required for copy");
    return native.copyPath(source, destination);
  },

  /**
   * Move/rename file or directory
   */
  movePath(source, destination) {
    if (!native) return require("fs").renameSync(source, destination);
    return native.movePath(source, destination);
  },

  /**
   * Check if path exists
   */
  pathExists(path) {
    if (!native) return require("fs").existsSync(path);
    return native.pathExists(path);
  },

  /**
   * Get file hash
   */
  getFileHash(path) {
    if (!native) throw new Error("Native backend required for hashing");
    return native.getFileHash(path);
  },
};

// ============================================================================
// Terminal Operations
// ============================================================================

export const terminal = {
  /**
   * Create a new terminal session
   */
  create(shell = null, cwd = null, cols = 80, rows = 24) {
    if (!native) throw new Error("Native backend required for terminal");
    return native.createTerminal(shell, cwd, cols, rows);
  },

  /**
   * Write to terminal
   */
  write(id, data) {
    if (!native) throw new Error("Native backend required for terminal");
    return native.writeTerminal(id, data);
  },

  /**
   * Read from terminal
   */
  read(id, maxBytes = 4096) {
    if (!native) throw new Error("Native backend required for terminal");
    return native.readTerminal(id, maxBytes);
  },

  /**
   * Resize terminal
   */
  resize(id, cols, rows) {
    if (!native) throw new Error("Native backend required for terminal");
    return native.resizeTerminal(id, cols, rows);
  },

  /**
   * Get terminal info
   */
  getInfo(id) {
    if (!native) throw new Error("Native backend required for terminal");
    return native.getTerminalInfo(id);
  },

  /**
   * List all terminals
   */
  list() {
    if (!native) return [];
    return native.listTerminals();
  },

  /**
   * Close terminal
   */
  close(id) {
    if (!native) throw new Error("Native backend required for terminal");
    return native.closeTerminal(id);
  },

  /**
   * Close all terminals
   */
  closeAll() {
    if (!native) return 0;
    return native.closeAllTerminals();
  },
};

// ============================================================================
// Settings
// ============================================================================

export const settings = {
  /**
   * Initialize settings from file
   */
  init(path, defaults = null) {
    if (!native) throw new Error("Native backend required for settings");
    return native.initSettings(
      path,
      defaults ? JSON.stringify(defaults) : null
    );
  },

  /**
   * Get a setting
   */
  get(key) {
    if (!native) throw new Error("Native backend required for settings");
    const value = native.getSetting(key);
    return value ? JSON.parse(value) : null;
  },

  /**
   * Set a setting
   */
  set(key, value) {
    if (!native) throw new Error("Native backend required for settings");
    return native.setSetting(key, JSON.stringify(value));
  },

  /**
   * Delete a setting
   */
  delete(key) {
    if (!native) throw new Error("Native backend required for settings");
    return native.deleteSetting(key);
  },

  /**
   * Get all settings
   */
  getAll() {
    if (!native) return {};
    return JSON.parse(native.getAllSettings());
  },

  /**
   * Reset all settings
   */
  reset() {
    if (!native) throw new Error("Native backend required for settings");
    return native.resetSettings();
  },

  /**
   * Save settings
   */
  save() {
    if (!native) throw new Error("Native backend required for settings");
    return native.saveSettings();
  },

  /**
   * Reload settings from file
   */
  reload() {
    if (!native) throw new Error("Native backend required for settings");
    return native.reloadSettings();
  },
};

// ============================================================================
// File Indexer
// ============================================================================

export const indexer = {
  /**
   * Start indexing a directory
   */
  start(rootPath, respectGitignore = true) {
    if (!native) throw new Error("Native backend required for indexer");
    return native.startIndexing(rootPath, respectGitignore);
  },

  /**
   * Get index statistics
   */
  getStats() {
    if (!native) return { totalFiles: 0, totalSize: 0, isIndexing: false };
    return native.getIndexStats();
  },

  /**
   * Search for files by name
   */
  searchFiles(query, maxResults = 50) {
    if (!native) return [];
    return native.searchFiles(query, maxResults);
  },

  /**
   * Search for symbols
   */
  searchSymbols(query, maxResults = 50) {
    if (!native) return [];
    return native.searchSymbols(query, maxResults);
  },

  /**
   * Get files by extension
   */
  getByExtension(extension) {
    if (!native) return [];
    return native.getFilesByExtension(extension);
  },

  /**
   * Clear the index
   */
  clear() {
    if (!native) return;
    return native.clearIndex();
  },

  /**
   * Refresh the index
   */
  refresh() {
    if (!native) return 0;
    return native.refreshIndex();
  },
};

// ============================================================================
// Git Operations
// ============================================================================

export const git = {
  /**
   * Check if path is a git repository
   */
  isRepo(path) {
    if (!native) return false;
    return native.isGitRepo(path);
  },

  /**
   * Get repository info
   */
  getRepoInfo(path) {
    if (!native) throw new Error("Native backend required for git");
    return native.getRepoInfo(path);
  },

  /**
   * Get status
   */
  status(path) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitStatus(path);
  },

  /**
   * Stage files
   */
  add(repoPath, files) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitAdd(repoPath, Array.isArray(files) ? files : [files]);
  },

  /**
   * Unstage files
   */
  unstage(repoPath, files) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitUnstage(repoPath, Array.isArray(files) ? files : [files]);
  },

  /**
   * Commit changes
   */
  commit(repoPath, message, authorName = null, authorEmail = null) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitCommit(repoPath, message, authorName, authorEmail);
  },

  /**
   * Get commit log
   */
  log(repoPath, maxCount = 50) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitLog(repoPath, maxCount);
  },

  /**
   * Get branches
   */
  branches(repoPath, includeRemote = false) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitBranches(repoPath, includeRemote);
  },

  /**
   * Create branch
   */
  createBranch(repoPath, name, checkout = true) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitCreateBranch(repoPath, name, checkout);
  },

  /**
   * Checkout branch
   */
  checkout(repoPath, branchName) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitCheckout(repoPath, branchName);
  },

  /**
   * Get diff
   */
  diff(repoPath, staged = false) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitDiff(repoPath, staged);
  },

  /**
   * Initialize repository
   */
  init(path) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitInit(path);
  },

  /**
   * Clone repository
   */
  clone(url, path) {
    if (!native) throw new Error("Native backend required for git");
    return native.gitClone(url, path);
  },

  /**
   * Get current branch
   */
  currentBranch(repoPath) {
    if (!native) return null;
    return native.gitCurrentBranch(repoPath);
  },
};

// ============================================================================
// Process Management
// ============================================================================

export const process = {
  /**
   * Spawn a new process
   */
  spawn(command, args = [], cwd = null, env = null) {
    if (!native) throw new Error("Native backend required for process");
    return native.spawnProcess(command, args, cwd, env);
  },

  /**
   * Run command and wait for completion
   */
  run(command, args = [], cwd = null, env = null, timeout = null) {
    if (!native) throw new Error("Native backend required for process");
    return native.runCommand(command, args, cwd, env, timeout);
  },

  /**
   * Run shell command
   */
  shell(command, cwd = null) {
    if (!native) throw new Error("Native backend required for process");
    return native.runShell(command, cwd);
  },

  /**
   * Write to process stdin
   */
  write(id, data) {
    if (!native) throw new Error("Native backend required for process");
    return native.writeToProcess(id, data);
  },

  /**
   * Get process info
   */
  getInfo(id) {
    if (!native) throw new Error("Native backend required for process");
    return native.getProcessInfo(id);
  },

  /**
   * List all processes
   */
  list() {
    if (!native) return [];
    return native.listProcesses();
  },

  /**
   * Kill process
   */
  kill(id) {
    if (!native) throw new Error("Native backend required for process");
    return native.killProcess(id);
  },

  /**
   * Wait for process
   */
  wait(id) {
    if (!native) throw new Error("Native backend required for process");
    return native.waitForProcess(id);
  },

  /**
   * Kill all processes
   */
  killAll() {
    if (!native) return 0;
    return native.killAllProcesses();
  },
};

// ============================================================================
// Check if native backend is available
// ============================================================================

export function isNativeAvailable() {
  return native !== null;
}

// Default export
export default {
  init: initNativeBackend,
  getVersion,
  healthCheck,
  isNativeAvailable,
  fileOps,
  terminal,
  settings,
  indexer,
  git,
  process,
};
