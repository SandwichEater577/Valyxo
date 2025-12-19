/**
 * Valyxo Native Backend - TypeScript Definitions
 */

// ============================================================================
// Types
// ============================================================================

export interface FileInfo {
  path: string;
  name: string;
  size: number;
  isDir: boolean;
  isFile: boolean;
  isSymlink: boolean;
  modified: number;
  created: number;
  extension: string | null;
}

export interface SearchMatch {
  path: string;
  lineNumber: number;
  lineContent: string;
  columnStart: number;
  columnEnd: number;
}

export interface TerminalInfo {
  id: string;
  shell: string;
  cwd: string;
  cols: number;
  rows: number;
  running: boolean;
}

export interface IndexStats {
  totalFiles: number;
  totalSize: number;
  indexedAt: number;
  rootPath: string;
  isIndexing: boolean;
}

export interface FileMatch {
  path: string;
  name: string;
  score: number;
  extension: string | null;
}

export interface IndexEntry {
  path: string;
  name: string;
  extension: string | null;
  size: number;
  modified: number;
  symbols: string[];
}

export interface GitStatusEntry {
  path: string;
  status: "added" | "modified" | "deleted" | "untracked" | "conflicted";
  staged: boolean;
}

export interface GitCommitInfo {
  id: string;
  message: string;
  author: string;
  email: string;
  time: number;
}

export interface GitBranchInfo {
  name: string;
  isHead: boolean;
  isRemote: boolean;
  commitId: string;
}

export interface GitDiffInfo {
  filesChanged: number;
  insertions: number;
  deletions: number;
  diffText: string;
}

export interface GitRepoInfo {
  path: string;
  isBare: boolean;
  isEmpty: boolean;
  headBranch: string | null;
  headCommit: string | null;
}

export interface ProcessInfo {
  id: string;
  command: string;
  args: string[];
  cwd: string;
  running: boolean;
  exitCode: number | null;
  pid: number | null;
}

export interface ProcessOutput {
  stdout: string;
  stderr: string;
  exitCode: number;
  success: boolean;
}

// ============================================================================
// Core Functions
// ============================================================================

export function initNativeBackend(): string;
export function getVersion(): string;
export function healthCheck(): boolean;
export function isNativeAvailable(): boolean;

// ============================================================================
// File Operations
// ============================================================================

export namespace fileOps {
  export function readFile(path: string): string;
  export function readFileBytes(path: string): Buffer;
  export function writeFile(path: string, content: string): void;
  export function writeFileBytes(path: string, content: Buffer): void;
  export function getFileInfo(path: string): FileInfo;
  export function listDirectory(path: string, recursive?: boolean): FileInfo[];
  export function searchInFiles(
    directory: string,
    pattern: string,
    filePattern?: string | null,
    maxResults?: number
  ): SearchMatch[];
  export function createDirectory(path: string): void;
  export function deletePath(path: string, recursive?: boolean): void;
  export function copyPath(source: string, destination: string): void;
  export function movePath(source: string, destination: string): void;
  export function pathExists(path: string): boolean;
  export function getFileHash(path: string): string;
}

// ============================================================================
// Terminal
// ============================================================================

export namespace terminal {
  export function create(
    shell?: string | null,
    cwd?: string | null,
    cols?: number,
    rows?: number
  ): string;
  export function write(id: string, data: string): void;
  export function read(id: string, maxBytes?: number): string;
  export function resize(id: string, cols: number, rows: number): void;
  export function getInfo(id: string): TerminalInfo;
  export function list(): TerminalInfo[];
  export function close(id: string): void;
  export function closeAll(): number;
}

// ============================================================================
// Settings
// ============================================================================

export namespace settings {
  export function init(
    path: string,
    defaults?: Record<string, any> | null
  ): void;
  export function get<T = any>(key: string): T | null;
  export function set(key: string, value: any): void;
  export function remove(key: string): boolean;
  export function getAll(): Record<string, any>;
  export function reset(): void;
  export function save(): void;
  export function reload(): void;
}

// ============================================================================
// File Indexer
// ============================================================================

export namespace indexer {
  export function start(rootPath: string, respectGitignore?: boolean): void;
  export function getStats(): IndexStats;
  export function searchFiles(query: string, maxResults?: number): FileMatch[];
  export function searchSymbols(
    query: string,
    maxResults?: number
  ): FileMatch[];
  export function getByExtension(extension: string): IndexEntry[];
  export function clear(): void;
  export function refresh(): number;
}

// ============================================================================
// Git
// ============================================================================

export namespace git {
  export function isRepo(path: string): boolean;
  export function getRepoInfo(path: string): GitRepoInfo;
  export function status(path: string): GitStatusEntry[];
  export function add(repoPath: string, files: string | string[]): number;
  export function unstage(repoPath: string, files: string | string[]): number;
  export function commit(
    repoPath: string,
    message: string,
    authorName?: string | null,
    authorEmail?: string | null
  ): string;
  export function log(repoPath: string, maxCount?: number): GitCommitInfo[];
  export function branches(
    repoPath: string,
    includeRemote?: boolean
  ): GitBranchInfo[];
  export function createBranch(
    repoPath: string,
    name: string,
    checkout?: boolean
  ): void;
  export function checkout(repoPath: string, branchName: string): void;
  export function diff(repoPath: string, staged?: boolean): GitDiffInfo;
  export function init(path: string): string;
  export function clone(url: string, path: string): string;
  export function currentBranch(repoPath: string): string | null;
}

// ============================================================================
// Process Management
// ============================================================================

export namespace process {
  export function spawn(
    command: string,
    args?: string[],
    cwd?: string | null,
    env?: Record<string, string> | null
  ): string;
  export function run(
    command: string,
    args?: string[],
    cwd?: string | null,
    env?: Record<string, string> | null,
    timeout?: number | null
  ): ProcessOutput;
  export function shell(command: string, cwd?: string | null): ProcessOutput;
  export function write(id: string, data: string): void;
  export function getInfo(id: string): ProcessInfo;
  export function list(): ProcessInfo[];
  export function kill(id: string): boolean;
  export function wait(id: string): number;
  export function killAll(): number;
}

// ============================================================================
// Default Export
// ============================================================================

declare const _default: {
  init: typeof initNativeBackend;
  getVersion: typeof getVersion;
  healthCheck: typeof healthCheck;
  isNativeAvailable: typeof isNativeAvailable;
  fileOps: typeof fileOps;
  terminal: typeof terminal;
  settings: typeof settings;
  indexer: typeof indexer;
  git: typeof git;
  process: typeof process;
};

export default _default;
