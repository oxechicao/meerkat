"""
Codex agent for generating commit messages.

This agent reuses the shared prompt and parsing utilities in `src.prompt`.
It calls the `codex` CLI (instead of `copilot`) and returns the parsed
conventional commit message when available.
"""
import subprocess

from .prompt import prompt, parse_output_message


def generate_commit_message_with_codex(story_file=None):
    """
    Generate a commit message using a Codex CLI.

    Args:
        story_file (str, optional): Path to the story file for context.

    Returns:
        str or None: The generated commit message, or None if failed.
    """
    command_prompt = prompt
    if story_file:
        command_prompt = f"{command_prompt} Also, uses as context reference the story on @{story_file}"

    try:
        result = subprocess.run(
            f'codex "{command_prompt}"',
            shell=True,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0 and result.stdout.strip():
            parsed = parse_output_message(result.stdout)
            if parsed:
                return parsed
            return None
    except Exception:
        pass

    return None
