//! Code editor widget with syntax highlighting

use crate::buffer::Buffer;
use crate::syntax::SyntaxHighlighter;
use eframe::egui::{self, Color32, FontId, Key, Rect, Response, Sense, TextStyle, Ui, Vec2};
use std::sync::Arc;

/// Editor widget
pub struct Editor;

impl Editor {
    /// Show the editor for a buffer
    pub fn show(ui: &mut Ui, buffer: &mut Buffer, syntax: Arc<SyntaxHighlighter>) {
        let font_id = FontId::monospace(14.0);
        let line_height = 20.0;
        let char_width = 8.4; // Approximate monospace character width
        let gutter_width = 60.0;
        
        let available_size = ui.available_size();
        let visible_lines = (available_size.y / line_height) as usize + 2;
        let first_visible_line = (buffer.scroll_y / line_height) as usize;
        
        // Create scrollable area
        let (response, painter) = ui.allocate_painter(available_size, Sense::click_and_drag());
        let rect = response.rect;
        
        // Background
        painter.rect_filled(rect, 0.0, Color32::from_rgb(30, 30, 30));
        
        // Handle scrolling
        if response.hovered() {
            let scroll = ui.input(|i| i.raw_scroll_delta);
            buffer.scroll_y = (buffer.scroll_y - scroll.y).max(0.0);
            buffer.scroll_x = (buffer.scroll_x - scroll.x).max(0.0);
        }
        
        // Draw gutter (line numbers)
        let gutter_rect = Rect::from_min_size(rect.min, Vec2::new(gutter_width, rect.height()));
        painter.rect_filled(gutter_rect, 0.0, Color32::from_rgb(35, 35, 35));
        
        // Get highlighted lines
        let text = buffer.text();
        let highlights = syntax.highlight(&text, &buffer.language);
        
        // Draw lines
        for i in 0..visible_lines {
            let line_idx = first_visible_line + i;
            if line_idx >= buffer.line_count {
                break;
            }
            
            let y = rect.min.y + (i as f32 * line_height) - (buffer.scroll_y % line_height);
            
            // Line number
            let line_num_text = format!("{:>4}", line_idx + 1);
            painter.text(
                egui::pos2(rect.min.x + 8.0, y + 2.0),
                egui::Align2::LEFT_TOP,
                &line_num_text,
                font_id.clone(),
                Color32::from_rgb(100, 100, 100),
            );
            
            // Line content
            if let Some(line_content) = buffer.line(line_idx) {
                let x_start = rect.min.x + gutter_width + 8.0 - buffer.scroll_x;
                
                // Get syntax highlights for this line
                if let Some(line_highlights) = highlights.get(line_idx) {
                    let mut x_offset = 0.0;
                    for (text_span, color) in line_highlights {
                        painter.text(
                            egui::pos2(x_start + x_offset, y + 2.0),
                            egui::Align2::LEFT_TOP,
                            text_span,
                            font_id.clone(),
                            *color,
                        );
                        x_offset += text_span.chars().count() as f32 * char_width;
                    }
                } else {
                    // No highlighting, draw plain text
                    let display_text = line_content.trim_end_matches('\n');
                    painter.text(
                        egui::pos2(x_start, y + 2.0),
                        egui::Align2::LEFT_TOP,
                        display_text,
                        font_id.clone(),
                        Color32::from_rgb(212, 212, 212),
                    );
                }
            }
            
            // Draw cursor
            if line_idx == buffer.cursor_line {
                let cursor_x = rect.min.x + gutter_width + 8.0 + (buffer.cursor_col as f32 * char_width) - buffer.scroll_x;
                let cursor_y = y;
                
                // Blinking cursor (simple implementation)
                let show_cursor = (ui.input(|i| i.time) * 2.0) as i32 % 2 == 0;
                if show_cursor {
                    painter.rect_filled(
                        Rect::from_min_size(
                            egui::pos2(cursor_x, cursor_y + 2.0),
                            Vec2::new(2.0, line_height - 4.0),
                        ),
                        0.0,
                        Color32::from_rgb(255, 255, 255),
                    );
                }
                
                // Highlight current line
                painter.rect_filled(
                    Rect::from_min_size(
                        egui::pos2(rect.min.x + gutter_width, y),
                        Vec2::new(rect.width() - gutter_width, line_height),
                    ),
                    0.0,
                    Color32::from_rgba_unmultiplied(255, 255, 255, 10),
                );
            }
        }
        
        // Separator between gutter and editor
        painter.line_segment(
            [
                egui::pos2(rect.min.x + gutter_width, rect.min.y),
                egui::pos2(rect.min.x + gutter_width, rect.max.y),
            ],
            egui::Stroke::new(1.0, Color32::from_rgb(50, 50, 50)),
        );
        
        // Handle keyboard input
        if response.has_focus() || response.clicked() {
            response.request_focus();
            
            ui.input(|input| {
                // Text input
                for event in &input.events {
                    match event {
                        egui::Event::Text(text) => {
                            buffer.insert(text);
                        }
                        egui::Event::Key { key, pressed: true, modifiers, .. } => {
                            match key {
                                Key::Enter => buffer.insert("\n"),
                                Key::Backspace => buffer.backspace(),
                                Key::Delete => buffer.delete(),
                                Key::ArrowUp => buffer.move_up(),
                                Key::ArrowDown => buffer.move_down(),
                                Key::ArrowLeft => buffer.move_left(),
                                Key::ArrowRight => buffer.move_right(),
                                Key::Home => buffer.move_home(),
                                Key::End => buffer.move_end(),
                                Key::Tab => buffer.insert("    "), // 4 spaces
                                Key::Z if modifiers.ctrl => {
                                    if modifiers.shift {
                                        buffer.redo();
                                    } else {
                                        buffer.undo();
                                    }
                                }
                                Key::Y if modifiers.ctrl => buffer.redo(),
                                _ => {}
                            }
                        }
                        _ => {}
                    }
                }
            });
        }
        
        // Click to position cursor
        if response.clicked() {
            if let Some(pos) = response.interact_pointer_pos() {
                let rel_x = pos.x - rect.min.x - gutter_width - 8.0 + buffer.scroll_x;
                let rel_y = pos.y - rect.min.y + buffer.scroll_y;
                
                buffer.cursor_line = ((rel_y / line_height) as usize).min(buffer.line_count.saturating_sub(1));
                
                if let Some(line) = buffer.line(buffer.cursor_line) {
                    let line_len = line.trim_end_matches('\n').chars().count();
                    buffer.cursor_col = ((rel_x / char_width) as usize).min(line_len);
                }
            }
        }
        
        // Ensure cursor is visible
        let cursor_y = buffer.cursor_line as f32 * line_height;
        if cursor_y < buffer.scroll_y {
            buffer.scroll_y = cursor_y;
        } else if cursor_y > buffer.scroll_y + available_size.y - line_height * 2.0 {
            buffer.scroll_y = cursor_y - available_size.y + line_height * 2.0;
        }
    }
}
