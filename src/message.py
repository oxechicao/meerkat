"""
Message building and commit message generation for Meerkat CLI.
"""
import os
import subprocess
from .git import run_command

def print_message(message, quiet=False):
    if not quiet:
        print(message)

def print_error(message):
    print(f"Error: {message}", file=sys.stderr)

def get_ai_commit_message(config, story_file=None, quiet=False):
    agent_path = config.get('MRKT_AGENT_PATH')
    agent_name = config.get('MRKT_AGENT', 'copilot')
    diff_command = "git diff --cached"
    diff = run_command(diff_command, capture_output=True, quiet=True)
    if not diff:
        print_error("No staged changes to commit")
        return None
    print_message("\nGenerating commit message with AI...", quiet)
    print_message("Context being used:", quiet)
    print_message("  - Git diff (staged changes)", quiet)
    if agent_path:
        ai_command = agent_path
        print_message(f"  - AI Agent: {agent_path}", quiet)
    else:
        ai_command = agent_name
        print_message(f"  - AI Agent: {agent_name}", quiet)
    prompt = "Generate a git commit message for the following changes:\n\n"
    prompt += diff
    if story_file and os.path.exists(story_file):
        with open(story_file, 'r') as f:
            story_content = f.read()
            prompt = f"Story context:\n{story_content}\n\n{prompt}"
            print_message(f"  - Story file: {story_file}", quiet)
    print_message("", quiet)
    try:
        result = subprocess.run(
            f'echo "{prompt}" | {ai_command}',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return generate_simple_commit_message(diff)

def generate_simple_commit_message(diff):
    lines = diff.split('\n')
    files = []
    for line in lines:
        if line.startswith('diff --git'):
            parts = line.split()
            if len(parts) >= 4:
                file_path = parts[3].replace('b/', '')
                files.append(file_path)
    if files:
        if len(files) == 1:
            return f"Update {files[0]}"
        else:
            return f"Update {len(files)} files"
    return "Update files"
