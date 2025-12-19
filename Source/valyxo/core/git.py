"""Valyxo Git Integration v0.6.0

Built-in git commands for seamless version control.

Commands:
    git status      Show working tree status
    git add         Add files to staging
    git commit      Commit changes
    git push        Push to remote
    git pull        Pull from remote
    git branch      List/create branches
    git checkout    Switch branches
    git log         Show commit history
    git diff        Show changes
"""

import os
import subprocess
from typing import List, Optional, Tuple, Dict, Any


class ValyxoGitError(Exception):
    """Git operation error."""
    pass


class ValyxoGit:
    """Git integration for Valyxo."""
    
    def __init__(self, cwd: str = None):
        self.cwd = cwd or os.getcwd()
        self._git_available = self._check_git()
    
    def _check_git(self) -> bool:
        """Check if git is available on the system."""
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _run_git(self, args: List[str], check: bool = True) -> Tuple[bool, str]:
        """Run a git command.
        
        Returns:
            Tuple of (success, output)
        """
        if not self._git_available:
            return False, "Git is not installed or not in PATH"
        
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout.strip()
            if result.returncode != 0:
                output = result.stderr.strip() or output
            
            return result.returncode == 0, output
        except subprocess.TimeoutExpired:
            return False, "Git command timed out"
        except Exception as e:
            return False, f"Git error: {e}"
    
    def is_repo(self) -> bool:
        """Check if current directory is a git repository."""
        success, _ = self._run_git(["rev-parse", "--git-dir"])
        return success
    
    def init(self) -> str:
        """Initialize a new git repository."""
        success, output = self._run_git(["init"])
        if success:
            return "✓ Initialized empty Git repository"
        return f"✗ {output}"
    
    def status(self, short: bool = False) -> str:
        """Get repository status."""
        args = ["status"]
        if short:
            args.append("-s")
        
        success, output = self._run_git(args)
        if success:
            return output if output else "Nothing to commit, working tree clean"
        return f"✗ {output}"
    
    def add(self, files: List[str] = None) -> str:
        """Stage files for commit."""
        if files is None or files == ["."] or files == ["*"]:
            args = ["add", "-A"]
        else:
            args = ["add"] + files
        
        success, output = self._run_git(args)
        if success:
            return "✓ Files staged for commit"
        return f"✗ {output}"
    
    def commit(self, message: str) -> str:
        """Commit staged changes."""
        if not message:
            return "✗ Commit message required"
        
        success, output = self._run_git(["commit", "-m", message])
        if success:
            # Extract commit hash from output
            lines = output.split('\n')
            return f"✓ {lines[0]}" if lines else "✓ Changes committed"
        return f"✗ {output}"
    
    def push(self, remote: str = "origin", branch: str = None) -> str:
        """Push commits to remote."""
        args = ["push", remote]
        if branch:
            args.append(branch)
        else:
            # Push current branch
            args.extend(["-u", remote, "HEAD"])
        
        success, output = self._run_git(args)
        if success:
            return f"✓ Pushed to {remote}"
        return f"✗ {output}"
    
    def pull(self, remote: str = "origin", branch: str = None) -> str:
        """Pull changes from remote."""
        args = ["pull", remote]
        if branch:
            args.append(branch)
        
        success, output = self._run_git(args)
        if success:
            return output if output else "✓ Already up to date"
        return f"✗ {output}"
    
    def branch(self, name: str = None, delete: bool = False) -> str:
        """List, create, or delete branches."""
        if name is None:
            # List branches
            success, output = self._run_git(["branch", "-a"])
            if success:
                return output if output else "No branches"
            return f"✗ {output}"
        
        if delete:
            success, output = self._run_git(["branch", "-d", name])
            if success:
                return f"✓ Deleted branch: {name}"
            return f"✗ {output}"
        
        # Create branch
        success, output = self._run_git(["branch", name])
        if success:
            return f"✓ Created branch: {name}"
        return f"✗ {output}"
    
    def checkout(self, target: str, create: bool = False) -> str:
        """Switch branches or restore files."""
        args = ["checkout"]
        if create:
            args.append("-b")
        args.append(target)
        
        success, output = self._run_git(args)
        if success:
            return f"✓ Switched to {'new ' if create else ''}branch: {target}"
        return f"✗ {output}"
    
    def log(self, count: int = 10, oneline: bool = True) -> str:
        """Show commit history."""
        args = ["log", f"-{count}"]
        if oneline:
            args.append("--oneline")
        
        success, output = self._run_git(args)
        if success:
            return output if output else "No commits yet"
        return f"✗ {output}"
    
    def diff(self, staged: bool = False, file: str = None) -> str:
        """Show changes."""
        args = ["diff"]
        if staged:
            args.append("--staged")
        if file:
            args.append(file)
        
        success, output = self._run_git(args)
        if success:
            return output if output else "No changes"
        return f"✗ {output}"
    
    def clone(self, url: str, directory: str = None) -> str:
        """Clone a repository."""
        args = ["clone", url]
        if directory:
            args.append(directory)
        
        success, output = self._run_git(args)
        if success:
            return f"✓ Cloned repository"
        return f"✗ {output}"
    
    def remote(self, add: str = None, url: str = None) -> str:
        """Manage remotes."""
        if add and url:
            success, output = self._run_git(["remote", "add", add, url])
            if success:
                return f"✓ Added remote: {add}"
            return f"✗ {output}"
        
        # List remotes
        success, output = self._run_git(["remote", "-v"])
        if success:
            return output if output else "No remotes configured"
        return f"✗ {output}"
    
    def stash(self, pop: bool = False, list_stashes: bool = False) -> str:
        """Stash changes."""
        if list_stashes:
            success, output = self._run_git(["stash", "list"])
            if success:
                return output if output else "No stashes"
            return f"✗ {output}"
        
        if pop:
            success, output = self._run_git(["stash", "pop"])
            if success:
                return "✓ Applied stashed changes"
            return f"✗ {output}"
        
        success, output = self._run_git(["stash"])
        if success:
            return "✓ Stashed changes"
        return f"✗ {output}"
    
    def get_current_branch(self) -> str:
        """Get current branch name."""
        success, output = self._run_git(["branch", "--show-current"])
        if success:
            return output if output else "HEAD detached"
        return "unknown"
    
    def get_repo_info(self) -> Dict[str, Any]:
        """Get repository information."""
        if not self.is_repo():
            return {"is_repo": False}
        
        _, remote = self._run_git(["remote", "get-url", "origin"])
        _, branch = self._run_git(["branch", "--show-current"])
        _, commit = self._run_git(["rev-parse", "--short", "HEAD"])
        _, status = self._run_git(["status", "-s"])
        
        changes = len(status.split('\n')) if status else 0
        
        return {
            "is_repo": True,
            "remote": remote if remote and not remote.startswith("✗") else None,
            "branch": branch or "unknown",
            "commit": commit or "unknown",
            "changes": changes
        }


def parse_git_command(args: str) -> Tuple[str, List[str]]:
    """Parse a git command string into subcommand and arguments."""
    parts = args.strip().split()
    if not parts:
        return "help", []
    
    return parts[0].lower(), parts[1:]
