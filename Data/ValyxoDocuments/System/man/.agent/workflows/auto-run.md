---
description: Auto-run all terminal commands without user approval
---

// turbo-all

When this workflow is active, all terminal commands will be executed automatically without requiring user confirmation.

## Usage

Simply mention `/auto-run` at the start of your request, or say "use auto-run mode" to enable this behavior.

## What this does

- Deletes files without asking
- Runs build commands automatically
- Executes git commands directly
- Installs packages without confirmation

## Safety Note

Only use this when you trust the changes being made. The agent will still exercise judgment on potentially destructive operations.
