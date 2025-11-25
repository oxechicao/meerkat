"""
Git-related operations for Meerkat CLI.
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, capture_output=False, quiet=False):
    try:
        if capture_output:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        else:
            result = subprocess.run(
                command,
                shell=True,
                check=True
            )
            return True
    except subprocess.CalledProcessError as e:
        if not quiet:
            print(f"Error: Command failed: {command}", file=sys.stderr)
            if capture_output and e.stderr:
                print(e.stderr, file=sys.stderr)
        return None

def get_current_branch():
    branch = run_command(
        "git rev-parse --abbrev-ref HEAD",
        capture_output=True,
        quiet=True
    )
    return branch if branch else "main"

def get_git_status_info():
    status_output = run_command(
        "git diff --cached --name-status",
        capture_output=True,
        quiet=True
    )
    if not status_output:
        return None
    files = []
    lines = status_output.split('\n')
    for line in lines:
        if not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) >= 2:
            status = parts[0]
            filename = parts[1]
            files.append({'status': status, 'name': filename})
    stat_output = run_command(
        "git diff --cached --numstat",
        capture_output=True,
        quiet=True
    )
    total_additions = 0
    total_deletions = 0
    if stat_output:
        stat_lines = stat_output.split('\n')
        for line in stat_lines:
            if not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                try:
                    additions = int(parts[0]) if parts[0] != '-' else 0
                    deletions = int(parts[1]) if parts[1] != '-' else 0
                    total_additions += additions
                    total_deletions += deletions
                except ValueError:
                    continue
    return {
        'files': files,
        'total_files': len(files),
        'additions': total_additions,
        'deletions': total_deletions
    }

def create_and_push_branch(full_branch_name, quiet=False):
    print(f"Creating branch: {full_branch_name}")
    if not run_command(f"git checkout -b {full_branch_name}", quiet=quiet):
        return False
    print("Pushing branch to origin...")
    if not run_command(f"git push -u origin {full_branch_name}", quiet=quiet):
        return False
    print("Branch created and pushed successfully!")
    return True

def perform_rebase(quiet=False):
    print("Rebasing on main...")
    if not run_command("git fetch origin main", quiet=quiet):
        return False
    if not run_command("git rebase origin/main", quiet=quiet):
        return False
    return True

def perform_merge(quiet=False):
    print("Merging main into branch...")
    if not run_command("git fetch origin main", quiet=quiet):
        return False
    if not run_command("git merge origin/main", quiet=quiet):
        return False
    return True
