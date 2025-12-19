//! Text buffer with rope data structure for O(log n) operations

use ropey::Rope;
use std::collections::HashMap;
use std::path::PathBuf;
use anyhow::Result;

/// Unique buffer identifier
pub type BufferId = u64;

/// A text buffer backed by a rope data structure
pub struct Buffer {
    /// Unique ID
    pub id: BufferId,
    
    /// File path (None for unsaved buffers)
    pub path: Option<PathBuf>,
    
    /// The text content as a rope
    pub rope: Rope,
    
    /// Whether the buffer has unsaved changes
    pub modified: bool,
    
    /// Current cursor position (line)
    pub cursor_line: usize,
    
    /// Current cursor position (column)
    pub cursor_col: usize,
    
    /// Selection start (line, col)
    pub selection_start: Option<(usize, usize)>,
    
    /// Selection end (line, col)
    pub selection_end: Option<(usize, usize)>,
    
    /// Scroll offset (vertical)
    pub scroll_y: f32,
    
    /// Scroll offset (horizontal)
    pub scroll_x: f32,
    
    /// Detected language
    pub language: String,
    
    /// Undo stack
    undo_stack: Vec<UndoEntry>,
    
    /// Redo stack
    redo_stack: Vec<UndoEntry>,
    
    /// Cached line count
    pub line_count: usize,
}

#[derive(Clone)]
struct UndoEntry {
    /// Position where edit occurred
    position: usize,
    /// Text that was removed (for undo)
    removed: String,
    /// Text that was inserted (for undo)
    inserted: String,
}

impl Buffer {
    /// Create a new empty buffer
    pub fn new(id: BufferId) -> Self {
        Self {
            id,
            path: None,
            rope: Rope::new(),
            modified: false,
            cursor_line: 0,
            cursor_col: 0,
            selection_start: None,
            selection_end: None,
            scroll_y: 0.0,
            scroll_x: 0.0,
            language: "Plain Text".to_string(),
            undo_stack: Vec::new(),
            redo_stack: Vec::new(),
            line_count: 1,
        }
    }
    
    /// Create a buffer from file
    pub fn from_file(id: BufferId, path: &PathBuf) -> Result<Self> {
        let content = std::fs::read_to_string(path)?;
        let rope = Rope::from_str(&content);
        let line_count = rope.len_lines();
        
        // Detect language from extension
        let language = path.extension()
            .and_then(|e| e.to_str())
            .map(detect_language)
            .unwrap_or_else(|| "Plain Text".to_string());
        
        Ok(Self {
            id,
            path: Some(path.clone()),
            rope,
            modified: false,
            cursor_line: 0,
            cursor_col: 0,
            selection_start: None,
            selection_end: None,
            scroll_y: 0.0,
            scroll_x: 0.0,
            language,
            undo_stack: Vec::new(),
            redo_stack: Vec::new(),
            line_count,
        })
    }
    
    /// Save buffer to file
    pub fn save(&mut self) -> Result<()> {
        if let Some(ref path) = self.path {
            let content = self.rope.to_string();
            std::fs::write(path, content)?;
            self.modified = false;
            Ok(())
        } else {
            anyhow::bail!("No file path set")
        }
    }
    
    /// Get the text content
    pub fn text(&self) -> String {
        self.rope.to_string()
    }
    
    /// Get a specific line
    pub fn line(&self, idx: usize) -> Option<String> {
        if idx < self.rope.len_lines() {
            Some(self.rope.line(idx).to_string())
        } else {
            None
        }
    }
    
    /// Insert text at cursor position
    pub fn insert(&mut self, text: &str) {
        let char_idx = self.cursor_to_char_idx();
        
        // Save for undo
        self.undo_stack.push(UndoEntry {
            position: char_idx,
            removed: String::new(),
            inserted: text.to_string(),
        });
        self.redo_stack.clear();
        
        self.rope.insert(char_idx, text);
        self.modified = true;
        self.line_count = self.rope.len_lines();
        
        // Move cursor
        for c in text.chars() {
            if c == '\n' {
                self.cursor_line += 1;
                self.cursor_col = 0;
            } else {
                self.cursor_col += 1;
            }
        }
    }
    
    /// Insert a single character
    pub fn insert_char(&mut self, c: char) {
        self.insert(&c.to_string());
    }
    
    /// Delete character before cursor (backspace)
    pub fn backspace(&mut self) {
        if self.cursor_col > 0 {
            self.cursor_col -= 1;
            let char_idx = self.cursor_to_char_idx();
            let removed = self.rope.char(char_idx).to_string();
            
            self.undo_stack.push(UndoEntry {
                position: char_idx,
                removed,
                inserted: String::new(),
            });
            self.redo_stack.clear();
            
            self.rope.remove(char_idx..char_idx + 1);
            self.modified = true;
            self.line_count = self.rope.len_lines();
        } else if self.cursor_line > 0 {
            // Join with previous line
            self.cursor_line -= 1;
            let prev_line_len = self.rope.line(self.cursor_line).len_chars();
            self.cursor_col = prev_line_len.saturating_sub(1);
            
            let char_idx = self.cursor_to_char_idx();
            self.undo_stack.push(UndoEntry {
                position: char_idx,
                removed: "\n".to_string(),
                inserted: String::new(),
            });
            self.redo_stack.clear();
            
            self.rope.remove(char_idx..char_idx + 1);
            self.modified = true;
            self.line_count = self.rope.len_lines();
        }
    }
    
    /// Delete character at cursor (delete key)
    pub fn delete(&mut self) {
        let char_idx = self.cursor_to_char_idx();
        if char_idx < self.rope.len_chars() {
            let removed = self.rope.char(char_idx).to_string();
            
            self.undo_stack.push(UndoEntry {
                position: char_idx,
                removed,
                inserted: String::new(),
            });
            self.redo_stack.clear();
            
            self.rope.remove(char_idx..char_idx + 1);
            self.modified = true;
            self.line_count = self.rope.len_lines();
        }
    }
    
    /// Move cursor up
    pub fn move_up(&mut self) {
        if self.cursor_line > 0 {
            self.cursor_line -= 1;
            let line_len = self.rope.line(self.cursor_line).len_chars().saturating_sub(1);
            self.cursor_col = self.cursor_col.min(line_len);
        }
    }
    
    /// Move cursor down
    pub fn move_down(&mut self) {
        if self.cursor_line < self.line_count.saturating_sub(1) {
            self.cursor_line += 1;
            let line_len = self.rope.line(self.cursor_line).len_chars().saturating_sub(1);
            self.cursor_col = self.cursor_col.min(line_len);
        }
    }
    
    /// Move cursor left
    pub fn move_left(&mut self) {
        if self.cursor_col > 0 {
            self.cursor_col -= 1;
        } else if self.cursor_line > 0 {
            self.cursor_line -= 1;
            self.cursor_col = self.rope.line(self.cursor_line).len_chars().saturating_sub(1);
        }
    }
    
    /// Move cursor right
    pub fn move_right(&mut self) {
        let line_len = self.rope.line(self.cursor_line).len_chars();
        if self.cursor_col < line_len.saturating_sub(1) {
            self.cursor_col += 1;
        } else if self.cursor_line < self.line_count.saturating_sub(1) {
            self.cursor_line += 1;
            self.cursor_col = 0;
        }
    }
    
    /// Move to start of line
    pub fn move_home(&mut self) {
        self.cursor_col = 0;
    }
    
    /// Move to end of line
    pub fn move_end(&mut self) {
        self.cursor_col = self.rope.line(self.cursor_line).len_chars().saturating_sub(1);
    }
    
    /// Undo last action
    pub fn undo(&mut self) {
        if let Some(entry) = self.undo_stack.pop() {
            if !entry.inserted.is_empty() {
                // Remove inserted text
                let len = entry.inserted.chars().count();
                self.rope.remove(entry.position..entry.position + len);
            }
            if !entry.removed.is_empty() {
                // Restore removed text
                self.rope.insert(entry.position, &entry.removed);
            }
            self.redo_stack.push(entry);
            self.modified = true;
            self.line_count = self.rope.len_lines();
        }
    }
    
    /// Redo last undone action
    pub fn redo(&mut self) {
        if let Some(entry) = self.redo_stack.pop() {
            if !entry.removed.is_empty() {
                // Remove the restored text
                let len = entry.removed.chars().count();
                self.rope.remove(entry.position..entry.position + len);
            }
            if !entry.inserted.is_empty() {
                // Re-insert the text
                self.rope.insert(entry.position, &entry.inserted);
            }
            self.undo_stack.push(entry);
            self.modified = true;
            self.line_count = self.rope.len_lines();
        }
    }
    
    /// Convert cursor position to character index
    fn cursor_to_char_idx(&self) -> usize {
        if self.cursor_line >= self.rope.len_lines() {
            return self.rope.len_chars();
        }
        let line_start = self.rope.line_to_char(self.cursor_line);
        let line_len = self.rope.line(self.cursor_line).len_chars();
        line_start + self.cursor_col.min(line_len)
    }
}

/// Buffer manager
pub struct BufferManager {
    buffers: HashMap<BufferId, Buffer>,
    next_id: BufferId,
}

impl BufferManager {
    pub fn new() -> Self {
        Self {
            buffers: HashMap::new(),
            next_id: 1,
        }
    }
    
    /// Create a new empty buffer
    pub fn create(&mut self) -> BufferId {
        let id = self.next_id;
        self.next_id += 1;
        self.buffers.insert(id, Buffer::new(id));
        id
    }
    
    /// Open a file into a buffer
    pub fn open_file(&mut self, path: &PathBuf) -> Result<BufferId> {
        // Check if already open
        for (id, buffer) in &self.buffers {
            if buffer.path.as_ref() == Some(path) {
                return Ok(*id);
            }
        }
        
        let id = self.next_id;
        self.next_id += 1;
        let buffer = Buffer::from_file(id, path)?;
        self.buffers.insert(id, buffer);
        Ok(id)
    }
    
    /// Get a buffer by ID
    pub fn get(&self, id: BufferId) -> Option<&Buffer> {
        self.buffers.get(&id)
    }
    
    /// Get a mutable buffer by ID
    pub fn get_mut(&mut self, id: BufferId) -> Option<&mut Buffer> {
        self.buffers.get_mut(&id)
    }
    
    /// Save a buffer
    pub fn save(&mut self, id: BufferId) -> Result<()> {
        if let Some(buffer) = self.buffers.get_mut(&id) {
            buffer.save()
        } else {
            anyhow::bail!("Buffer not found")
        }
    }
    
    /// Close a buffer
    pub fn close(&mut self, id: BufferId) {
        self.buffers.remove(&id);
    }
}

/// Detect language from file extension
fn detect_language(ext: &str) -> String {
    match ext.to_lowercase().as_str() {
        "rs" => "Rust",
        "py" => "Python",
        "js" => "JavaScript",
        "ts" => "TypeScript",
        "jsx" => "JavaScript React",
        "tsx" => "TypeScript React",
        "html" | "htm" => "HTML",
        "css" => "CSS",
        "scss" | "sass" => "SCSS",
        "json" => "JSON",
        "md" => "Markdown",
        "yaml" | "yml" => "YAML",
        "toml" => "TOML",
        "xml" => "XML",
        "c" | "h" => "C",
        "cpp" | "cc" | "cxx" | "hpp" => "C++",
        "java" => "Java",
        "go" => "Go",
        "rb" => "Ruby",
        "php" => "PHP",
        "sh" | "bash" => "Shell",
        "ps1" => "PowerShell",
        "sql" => "SQL",
        "swift" => "Swift",
        "kt" => "Kotlin",
        _ => "Plain Text",
    }.to_string()
}
