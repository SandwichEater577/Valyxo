import os
import time
import threading
from typing import Dict, Optional, Any


class ValyxoJobsManager:
    """Job management system for ValyxoHub.
    
    Manages background and foreground job execution, tracking status,
    runtime, and allowing job termination.
    """

    def __init__(self) -> None:
        """Initialize job manager with empty job list."""
        self.jobs: Dict[int, Dict[str, Any]] = {}
        self.job_counter: int = 0
        self.lock: threading.Lock = threading.Lock()

    def create_job(self, filepath: str) -> int:
        """Create and register a new job.
        
        Args:
            filepath: Path to script file being executed
        
        Returns:
            Job process ID (PID)
        """
        with self.lock:
            self.job_counter += 1
            pid = self.job_counter
            self.jobs[pid] = {
                "path": filepath,
                "status": "running",
                "thread": None,
                "start": time.time(),
                "stop": False
            }
            return pid

    def update_status(self, pid: int, status: str) -> None:
        """Update job status.
        
        Args:
            pid: Job process ID
            status: New status string
        """
        with self.lock:
            if pid in self.jobs:
                self.jobs[pid]["status"] = status

    def stop_job(self, pid: int) -> bool:
        """Request job termination.
        
        Args:
            pid: Job process ID
        
        Returns:
            True if job found and marked for termination
        """
        with self.lock:
            if pid not in self.jobs:
                return False
            
            self.jobs[pid]["stop"] = True
            self.jobs[pid]["status"] = "terminating"
            return True

    def get_job(self, pid: int) -> Optional[Dict[str, Any]]:
        """Get job information.
        
        Args:
            pid: Job process ID
        
        Returns:
            Job info dict or None if not found
        """
        with self.lock:
            return self.jobs.get(pid)

    def list_jobs(self) -> None:
        """Display all active jobs."""
        with self.lock:
            if not self.jobs:
                print("No active jobs")
                return
            
            for pid, info in sorted(self.jobs.items()):
                age = int(time.time() - info.get("start", time.time()))
                filename = os.path.basename(info["path"])
                status = info["status"]
                print(f"#{pid} {filename} [{status}] ({age}s)")
