//! Theme system

use eframe::egui::{self, Color32, Context, Visuals};
use serde::{Deserialize, Serialize};

/// Theme colors
#[derive(Clone, Serialize, Deserialize)]
pub struct Theme {
    pub name: String,
    pub background: [u8; 3],
    pub foreground: [u8; 3],
    pub accent: [u8; 3],
    pub selection: [u8; 3],
    pub gutter: [u8; 3],
    pub line_highlight: [u8; 3],
    pub border: [u8; 3],
    pub sidebar: [u8; 3],
    pub tab_active: [u8; 3],
    pub tab_inactive: [u8; 3],
    pub status_bar: [u8; 3],
}

impl Default for Theme {
    fn default() -> Self {
        Self::dark()
    }
}

impl Theme {
    /// Dark theme (default)
    pub fn dark() -> Self {
        Self {
            name: "Dark".to_string(),
            background: [30, 30, 30],
            foreground: [212, 212, 212],
            accent: [0, 122, 204],
            selection: [38, 79, 120],
            gutter: [35, 35, 35],
            line_highlight: [40, 40, 40],
            border: [50, 50, 50],
            sidebar: [33, 33, 33],
            tab_active: [45, 45, 45],
            tab_inactive: [30, 30, 30],
            status_bar: [0, 122, 204],
        }
    }
    
    /// Light theme
    pub fn light() -> Self {
        Self {
            name: "Light".to_string(),
            background: [255, 255, 255],
            foreground: [0, 0, 0],
            accent: [0, 122, 204],
            selection: [173, 214, 255],
            gutter: [240, 240, 240],
            line_highlight: [248, 248, 248],
            border: [220, 220, 220],
            sidebar: [245, 245, 245],
            tab_active: [255, 255, 255],
            tab_inactive: [240, 240, 240],
            status_bar: [0, 122, 204],
        }
    }
    
    /// Monokai theme
    pub fn monokai() -> Self {
        Self {
            name: "Monokai".to_string(),
            background: [39, 40, 34],
            foreground: [248, 248, 242],
            accent: [166, 226, 46],
            selection: [73, 72, 62],
            gutter: [45, 46, 40],
            line_highlight: [50, 51, 45],
            border: [60, 61, 55],
            sidebar: [35, 36, 30],
            tab_active: [50, 51, 45],
            tab_inactive: [39, 40, 34],
            status_bar: [166, 226, 46],
        }
    }
    
    /// Dracula theme
    pub fn dracula() -> Self {
        Self {
            name: "Dracula".to_string(),
            background: [40, 42, 54],
            foreground: [248, 248, 242],
            accent: [189, 147, 249],
            selection: [68, 71, 90],
            gutter: [45, 47, 59],
            line_highlight: [55, 57, 69],
            border: [68, 71, 90],
            sidebar: [35, 37, 49],
            tab_active: [55, 57, 69],
            tab_inactive: [40, 42, 54],
            status_bar: [189, 147, 249],
        }
    }
    
    /// Nord theme
    pub fn nord() -> Self {
        Self {
            name: "Nord".to_string(),
            background: [46, 52, 64],
            foreground: [236, 239, 244],
            accent: [136, 192, 208],
            selection: [67, 76, 94],
            gutter: [52, 58, 70],
            line_highlight: [59, 66, 82],
            border: [67, 76, 94],
            sidebar: [41, 47, 59],
            tab_active: [59, 66, 82],
            tab_inactive: [46, 52, 64],
            status_bar: [136, 192, 208],
        }
    }
    
    /// Apply theme to egui context
    pub fn apply(&self, ctx: &Context) {
        let mut visuals = Visuals::dark();
        
        visuals.panel_fill = Color32::from_rgb(self.background[0], self.background[1], self.background[2]);
        visuals.widgets.noninteractive.bg_fill = Color32::from_rgb(self.sidebar[0], self.sidebar[1], self.sidebar[2]);
        visuals.widgets.inactive.bg_fill = Color32::from_rgb(self.tab_inactive[0], self.tab_inactive[1], self.tab_inactive[2]);
        visuals.widgets.active.bg_fill = Color32::from_rgb(self.accent[0], self.accent[1], self.accent[2]);
        visuals.widgets.hovered.bg_fill = Color32::from_rgb(self.selection[0], self.selection[1], self.selection[2]);
        visuals.selection.bg_fill = Color32::from_rgb(self.selection[0], self.selection[1], self.selection[2]);
        visuals.window_fill = Color32::from_rgb(self.background[0], self.background[1], self.background[2]);
        visuals.window_stroke.color = Color32::from_rgb(self.border[0], self.border[1], self.border[2]);
        
        ctx.set_visuals(visuals);
    }
    
    /// Get color as Color32
    pub fn background_color(&self) -> Color32 {
        Color32::from_rgb(self.background[0], self.background[1], self.background[2])
    }
    
    pub fn foreground_color(&self) -> Color32 {
        Color32::from_rgb(self.foreground[0], self.foreground[1], self.foreground[2])
    }
    
    pub fn accent_color(&self) -> Color32 {
        Color32::from_rgb(self.accent[0], self.accent[1], self.accent[2])
    }
}

/// Available themes
pub fn available_themes() -> Vec<Theme> {
    vec![
        Theme::dark(),
        Theme::light(),
        Theme::monokai(),
        Theme::dracula(),
        Theme::nord(),
    ]
}
