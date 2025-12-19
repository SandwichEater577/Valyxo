/**
 * Valyxo Native Backend - Test Script
 *
 * Run with: node test.js
 */

const path = require("path");
const fs = require("fs");

// Try to load native module
let native;
try {
  native = require("./index.js");
  console.log("✅ Native module loaded successfully");
} catch (e) {
  console.log("⚠️  Native module not built yet");
  console.log("   Run: build.bat (Windows) or ./build.sh (Mac/Linux)");
  console.log("");
  console.log("Error:", e.message);
  process.exit(1);
}

console.log("");
console.log("============================================");
console.log("Valyxo Native Backend Test");
console.log("============================================");
console.log("");

// Test functions
async function runTests() {
  let passed = 0;
  let failed = 0;

  function test(name, fn) {
    try {
      fn();
      console.log(`✅ ${name}`);
      passed++;
    } catch (e) {
      console.log(`❌ ${name}: ${e.message}`);
      failed++;
    }
  }

  // Core tests
  console.log("--- Core Functions ---");

  test("isNativeAvailable", () => {
    const result = native.isNativeAvailable();
    if (typeof result !== "boolean") throw new Error("Expected boolean");
  });

  if (native.isNativeAvailable()) {
    test("initNativeBackend", () => {
      const result = native.init();
      if (!result.includes("Valyxo")) throw new Error("Unexpected result");
    });

    test("getVersion", () => {
      const result = native.getVersion();
      if (!result.includes("Native")) throw new Error("Unexpected result");
    });

    test("healthCheck", () => {
      const result = native.healthCheck();
      if (result !== true) throw new Error("Health check failed");
    });

    // File operations tests
    console.log("");
    console.log("--- File Operations ---");

    const testFile = path.join(__dirname, "test_file.txt");
    const testContent =
      "Hello from Valyxo Native!\n" + new Date().toISOString();

    test("writeFile", () => {
      native.fileOps.writeFile(testFile, testContent);
    });

    test("readFile", () => {
      const content = native.fileOps.readFile(testFile);
      if (content !== testContent) throw new Error("Content mismatch");
    });

    test("pathExists", () => {
      if (!native.fileOps.pathExists(testFile))
        throw new Error("File should exist");
    });

    test("getFileInfo", () => {
      const info = native.fileOps.getFileInfo(testFile);
      if (!info.name) throw new Error("Missing name");
      if (info.size === 0) throw new Error("Size should not be 0");
    });

    test("listDirectory", () => {
      const entries = native.fileOps.listDirectory(__dirname);
      if (!Array.isArray(entries)) throw new Error("Expected array");
      if (entries.length === 0)
        throw new Error("Directory should not be empty");
    });

    // Cleanup test file
    try {
      native.fileOps.deletePath(testFile);
    } catch (e) {
      fs.unlinkSync(testFile);
    }

    // Git tests (if in a git repo)
    console.log("");
    console.log("--- Git Operations ---");

    const repoPath = path.resolve(__dirname, "..");

    test("git.isRepo", () => {
      const result = native.git.isRepo(repoPath);
      console.log(`   (is git repo: ${result})`);
    });

    if (native.git.isRepo(repoPath)) {
      test("git.currentBranch", () => {
        const branch = native.git.currentBranch(repoPath);
        console.log(`   (branch: ${branch})`);
      });

      test("git.status", () => {
        const status = native.git.status(repoPath);
        console.log(`   (${status.length} changed files)`);
      });

      test("git.branches", () => {
        const branches = native.git.branches(repoPath);
        console.log(`   (${branches.length} branches)`);
      });
    }

    // Indexer tests
    console.log("");
    console.log("--- File Indexer ---");

    test("indexer.start", () => {
      native.indexer.start(__dirname, true);
    });

    test("indexer.getStats", () => {
      const stats = native.indexer.getStats();
      console.log(`   (${stats.totalFiles} files indexed)`);
    });

    test("indexer.searchFiles", () => {
      const results = native.indexer.searchFiles("index", 10);
      console.log(`   (${results.length} matches for 'index')`);
    });

    test("indexer.clear", () => {
      native.indexer.clear();
    });
  } else {
    console.log("");
    console.log("⚠️  Native backend not available, skipping native tests");
  }

  // Summary
  console.log("");
  console.log("============================================");
  console.log(`Tests: ${passed} passed, ${failed} failed`);
  console.log("============================================");

  process.exit(failed > 0 ? 1 : 0);
}

runTests().catch((e) => {
  console.error("Test error:", e);
  process.exit(1);
});
