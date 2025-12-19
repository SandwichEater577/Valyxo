//! Syntax highlighting using syntect

use eframe::egui::Color32;
use std::collections::HashMap;
use syntect::easy::HighlightLines;
use syntect::highlighting::{Style, ThemeSet};
use syntect::parsing::SyntaxSet;
use syntect::util::LinesWithEndings;

/// Syntax highlighter
pub struct SyntaxHighlighter {
    syntax_set: SyntaxSet,
    theme_set: ThemeSet,
}

impl SyntaxHighlighter {
    pub fn new() -> Self {
        Self {
            syntax_set: SyntaxSet::load_defaults_newlines(),
            theme_set: ThemeSet::load_defaults(),
        }
    }
    
    /// Highlight text and return colored spans per line
    pub fn highlight(&self, text: &str, language: &str) -> Vec<Vec<(String, Color32)>> {
        let syntax = self.syntax_set
            .find_syntax_by_name(language)
            .or_else(|| self.syntax_set.find_syntax_by_extension(language.to_lowercase().as_str()))
            .unwrap_or_else(|| self.syntax_set.find_syntax_plain_text());
        
        let theme = &self.theme_set.themes["base16-ocean.dark"];
        let mut highlighter = HighlightLines::new(syntax, theme);
        
        let mut result = Vec::new();
        
        for line in LinesWithEndings::from(text) {
            let mut line_spans = Vec::new();
            
            match highlighter.highlight_line(line, &self.syntax_set) {
                Ok(ranges) => {
                    for (style, text_span) in ranges {
                        let color = style_to_color32(&style);
                        // Remove trailing newline for display
                        let display_text = text_span.trim_end_matches('\n').to_string();
                        if !display_text.is_empty() {
                            line_spans.push((display_text, color));
                        }
                    }
                }
                Err(_) => {
                    // Fallback to plain text
                    line_spans.push((line.trim_end_matches('\n').to_string(), Color32::from_rgb(212, 212, 212)));
                }
            }
            
            result.push(line_spans);
        }
        
        result
    }
    
    /// Get list of available themes
    pub fn available_themes(&self) -> Vec<&str> {
        self.theme_set.themes.keys().map(|s| s.as_str()).collect()
    }
    
    /// Get list of supported languages
    pub fn available_languages(&self) -> Vec<&str> {
        self.syntax_set.syntaxes().iter().map(|s| s.name.as_str()).collect()
    }
}

/// Convert syntect style to egui Color32
fn style_to_color32(style: &Style) -> Color32 {
    Color32::from_rgb(
        style.foreground.r,
        style.foreground.g,
        style.foreground.b,
    )
}
