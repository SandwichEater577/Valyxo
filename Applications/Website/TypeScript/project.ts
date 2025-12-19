// Valyxo Project Page Logic (TypeScript)
// Handles WASM loading and GitHub API interaction

// Type for the WASM module
interface WasmModule {
  main_js: () => Promise<void>;
}

// Fallback logic interfaces
interface RepoStats {
  stargazers_count: number;
  forks_count: number;
  open_issues_count: number;
}

interface Contributor {
  login: string;
  avatar_url: string;
  html_url: string;
  contributions: number;
}

// Color map for languages
const LANGUAGE_COLORS: Record<string, string> = {
  Python: "#3572A5",
  Rust: "#dea584",
  JavaScript: "#f1e05a",
  HTML: "#e34c26",
  CSS: "#563d7c",
  Go: "#00ADD8",
  TypeScript: "#2b7489",
  Shell: "#89e051",
};

// Main execution - WASM disabled until built
async function run() {
  // Note: WASM integration is ready but module needs to be compiled first
  // Run: cd Applications/Website/wasm && wasm-pack build --target web
  // Then uncomment the WASM code below

  // For now, use the TypeScript fallback directly
  fallbackLogic();

  /* WASM code (uncomment after building):
  try {
    const wasm = await import("../wasm/pkg/valyxo_web.js");
    await wasm.default();
    await wasm.main_js();
  } catch (e) {
    console.warn("WASM failed:", e);
    fallbackLogic();
  }
  */
}

// Executed if WASM fails or is not present
function fallbackLogic() {
  fetchGitHubStats();
  fetchContributors();
  fetchLanguages();
}

async function fetchGitHubStats() {
  try {
    const response = await fetch(
      "https://api.github.com/repos/SandwichEater577/Valyxo"
    );
    if (!response.ok) throw new Error("API error");
    const data = (await response.json()) as RepoStats;

    updateText("star-count", `${data.stargazers_count} stars`);
    updateText("fork-count", `${data.forks_count} forks`);
    updateText("issue-count", `${data.open_issues_count} issues`);
  } catch (error) {
    updateText("star-count", "0 stars");
    updateText("fork-count", "0 forks");
    updateText("issue-count", "0 issues");
  }
}

async function fetchContributors() {
  const container = document.getElementById("contributors-list");
  if (!container) return;

  try {
    const response = await fetch(
      "https://api.github.com/repos/SandwichEater577/Valyxo/contributors"
    );
    if (!response.ok) throw new Error("API error");
    const contributors = (await response.json()) as Contributor[];

    const filtered = contributors.filter(
      (c) => c.login.toLowerCase() !== "michalmazur"
    );

    container.innerHTML = filtered
      .map(
        (c) => `
        <a href="${c.html_url}" target="_blank" class="contributor">
            <img src="${c.avatar_url}" alt="${c.login}" class="contributor-avatar-img" />
            <span>${c.login}</span>
            <span class="contributor-commits">${c.contributions} commits</span>
        </a>
        `
      )
      .join("");
  } catch (error) {
    container.innerHTML = `
        <div class="contributor">
            <div class="contributor-avatar">?</div>
            <span>Unable to load contributors</span>
        </div>`;
  }
}

async function fetchLanguages() {
  try {
    const response = await fetch(
      "https://api.github.com/repos/SandwichEater577/Valyxo/languages"
    );
    if (!response.ok) throw new Error("API error");
    const languages = (await response.json()) as Record<string, number>;

    const totalBytes = Object.values(languages).reduce((a, b) => a + b, 0);
    const langBar = document.getElementById("language-bar");
    const langList = document.getElementById("language-list");

    if (langBar) langBar.innerHTML = "";
    if (langList) langList.innerHTML = "";

    for (const [lang, bytes] of Object.entries(languages)) {
      const percent = ((bytes / totalBytes) * 100).toFixed(1);
      if (parseFloat(percent) < 1.0) continue;

      const color = LANGUAGE_COLORS[lang] || "#ccc";

      // Bar segment
      const segment = document.createElement("div");
      segment.className = "lang-segment";
      segment.style.width = percent + "%";
      segment.style.backgroundColor = color;
      segment.title = `${lang}: ${percent}%`;
      if (langBar) langBar.appendChild(segment);

      // List item
      const item = document.createElement("div");
      item.className = "lang-item";
      item.innerHTML = `
                <span class="lang-dot" style="background-color: ${color}"></span> 
                ${lang} 
                <span class="lang-percent">${percent}%</span>
            `;
      if (langList) langList.appendChild(item);
    }
  } catch (error) {
    console.error("Failed to load languages", error);
  }
}

function updateText(id: string, text: string) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

// Start the application
run();
