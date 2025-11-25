"""
Message building and commit message generation for Meerkat CLI.
"""
import os
import subprocess
import sys
from .git import run_command


def print_message(message, quiet=False):
    if not quiet:
        print(message)


def print_error(message):
    print(f"Error: {message}", file=sys.stderr)


def save_reference_to_file(diff):
    with open('temp_git_message_reference.md', 'w') as f:
        f.write(diff)


def get_agent_message(config, diff, story_file=None, quiet=False):
    """
    Select and call the configured AI agent to generate a commit message.

    Falls back to `generate_simple_commit_message(diff)` on failure or
    when no known agent is configured.
    """
    agent_path = config.get('MRKT_AGENT_PATH')
    agent_name = config.get('MRKT_AGENT', 'codex')

    print_message("\nGenerating commit message with AI...", quiet)
    print_message("Context being used:", quiet)
    print_message("  - Git diff (staged changes)", quiet)

    # If no explicit agent name configured, just return simple message
    if not agent_name:
        print_message("  - AI Agent: (none configured), using simple generator", quiet)
        return generate_simple_commit_message(diff)

    # Copilot special flow: create temp reference file and call module
    if agent_name == 'copilot':
        print_message(f"  - AI Agent: {agent_name}", quiet)
        if story_file:
            print_message(f"  - Story file: {story_file}", quiet)
        save_reference_to_file(diff)
        try:
            from .agent_copilot import generate_commit_message_with_copilot

            msg = generate_commit_message_with_copilot(story_file)
        except Exception:
            msg = None
        finally:
            try:
                os.remove('temp_git_message_reference.md')
            except Exception:
                pass

        if msg:
            print_message("AI agent call succeeded.\n", quiet)
            print_message(f"AI Output: {msg}\n", quiet)
            return msg

        print_message("AI agent call failed, falling back to simple commit message generation.\n\n", quiet)
        return generate_simple_commit_message(diff)

    # Codex: call dedicated module
    if agent_name == 'codex':
        print_message(f"  - AI Agent: {agent_name}", quiet)
        if story_file:
            print_message(f"  - Story file: {story_file}", quiet)
        try:
            from .agent_codex import generate_commit_message_with_codex

            msg = generate_commit_message_with_codex(story_file)
        except Exception:
            msg = None

        if msg:
            print_message("AI agent call succeeded.\n", quiet)
            print_message(f"AI Output: {msg}\n", quiet)
            return msg

        print_message("AI agent call failed, falling back to simple commit message generation.\n\n", quiet)
        return generate_simple_commit_message(diff)

    # Unknown agent: try invoking via provided path or name as a CLI
    if agent_path:
        ai_command = agent_path
        display_agent = agent_path
    else:
        ai_command = agent_name
        display_agent = agent_name

    print_message(f"  - AI Agent: {display_agent}", quiet)

    prompt_text = "Generate a git commit message for the following changes:\n\n"
    prompt_text += diff
    if story_file and os.path.exists(story_file):
        with open(story_file, 'r') as f:
            story_content = f.read()
            prompt_text = f"Story context:\n{story_content}\n\n{prompt_text}"
            print_message(f"  - Story file: {story_file}", quiet)

    print_message("Try to call agent prompt. \n\n", quiet)
    try:
        command = ai_command + ' -p "' + prompt_text + '"'
        print_message(f"AI Command: {ai_command}\n", quiet)
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            print_message("AI agent call succeeded.\n", quiet)
            print_message(f"AI Output: {result.stdout}\n", quiet)
            return result.stdout.strip()
    except Exception:
        print_message(
            "AI agent call failed, falling back "
            + "to simple commit message generation.\n\n",
            quiet
        )

    return generate_simple_commit_message(diff)


def get_ai_commit_message(config, story_file=None, quiet=False):
    diff_command = "git diff --cached"
    diff = run_command(diff_command, capture_output=True, quiet=True)
    if not diff:
        print_error("No staged changes to commit")
        return None

    return get_agent_message(config, diff, story_file, quiet)


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
