use wasm_bindgen::prelude::*;
use serde::Deserialize;
use web_sys::console;

#[derive(Deserialize)]
struct RepoStats {
    stargazers_count: u32,
    forks_count: u32,
    open_issues_count: u32,
}

#[derive(Deserialize)]
struct Contributor {
    login: String,
    avatar_url: String,
    html_url: String,
    contributions: u32,
}

#[wasm_bindgen(start)]
pub async fn main_js() -> Result<(), JsValue> {
    console::log_1(&"🚀 Rust (WASM) initialized for Valyxo Web!".into());
    
    // Fetch and update stats
    update_stats().await?;
    
    // Fetch and update contributors
    update_contributors().await?;

    Ok(())
}

async fn update_stats() -> Result<(), JsValue> {
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");

    // Mocking the fetch for now or using reqwest
    // Note: In a real WASM fetch we rely on window.fetch or reqwest
    // Here using simple window.fetch wrapper logic or reqwest if compiled
    
    // For simplicity efficiently updating DOM placeholders first
    if let Some(el) = document.get_element_by_id("star-count") {
        el.set_text_content(Some("Loading (Rust)..."));
    }

    match reqwest::get("https://api.github.com/repos/SandwichEater577/Valyxo").await {
        Ok(resp) => {
            if let Ok(stats) = resp.json::<RepoStats>().await {
                if let Some(el) = document.get_element_by_id("star-count") {
                    el.set_text_content(Some(&format!("{} stars", stats.stargazers_count)));
                }
                if let Some(el) = document.get_element_by_id("fork-count") {
                    el.set_text_content(Some(&format!("{} forks", stats.forks_count)));
                }
                if let Some(el) = document.get_element_by_id("issue-count") {
                    el.set_text_content(Some(&format!("{} issues", stats.open_issues_count)));
                }
            }
        }
        Err(e) => {
            console::error_1(&format!("Failed to fetch stats: {:?}", e).into());
        }
    }
    
    Ok(())
}

async fn update_contributors() -> Result<(), JsValue> {
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");
    
    if let Some(container) = document.get_element_by_id("contributors-list") {
       match reqwest::get("https://api.github.com/repos/SandwichEater577/Valyxo/contributors").await {
           Ok(resp) => {
               if let Ok(contributors) = resp.json::<Vec<Contributor>>().await {
                   let filtered: Vec<&Contributor> = contributors.iter()
                       .filter(|c| c.login.to_lowercase() != "michalmazur")
                       .collect();
                   
                   container.set_inner_html(""); // Clear loading
                   
                   for c in filtered {
                       // Create elements cleanly
                       let a = document.create_element("a")?;
                       a.set_attribute("href", &c.html_url)?;
                       a.set_attribute("target", "_blank")?;
                       a.set_attribute("class", "contributor")?;
                       
                       let img = document.create_element("img")?;
                       img.set_attribute("src", &c.avatar_url)?;
                       img.set_attribute("class", "contributor-avatar-img")?;
                       
                       let span_name = document.create_element("span")?;
                       span_name.set_text_content(Some(&c.login));
                       
                       let span_commits = document.create_element("span")?;
                       span_commits.set_attribute("class", "contributor-commits")?;
                       span_commits.set_text_content(Some(&format!("{} commits", c.contributions)));
                       
                       a.append_child(&img)?;
                       a.append_child(&span_name)?;
                       a.append_child(&span_commits)?;
                       
                       container.append_child(&a)?;
                   }
               }
           }
           Err(_) => {}
       }
    }
    Ok(())
}
