"""
Copilot agent for generating commit messages.
"""
import re
import subprocess


def parse_copilot_output(output):
    """
    Parse Copilot CLI output and extract the commit message starting
    from a Conventional Commit header.

    This finds the first line that matches the Conventional Commits
    header pattern (e.g. "feat(scope): short description") and returns
    the text from that line to the end. If no Conventional Commit header
    is found, returns None.

    Args:
        output (str): Full stdout from Copilot CLI.

    Returns:
        str or None: The cleaned commit message, or None if parsing fails.
    """
    if not output:
        return None

    # Match conventional commit headers like:
    # feat: summary
    # fix(scope): summary
    # chore!: summary
    pattern = re.compile(r"^[a-z]+(?:\([^\)]*\))?(?:!)?:\s+.+", re.IGNORECASE)

    lines = output.splitlines()
    for idx, line in enumerate(lines):
        if pattern.match(line.strip()):
            # Return from the matched header to the end
            return "\n".join(lines[idx:]).strip()

    return None


def generate_commit_message_with_copilot(story_file=None):
    """
    Generate a commit message using GitHub Copilot CLI.

    Args:
        story_file (str, optional): Path to the story file for context.

    Returns:
        str or None: The generated commit message, or None if failed.
    """
    prompt = ("Generate a git commit message for the following changes in "
              "@temp_git_message_reference.md"
              "I want only the commit message."
              "I will use this commit message directly."
              "BE SURE TO ONLY RETURN THE COMMIT MESSAGE."
              "DO NOT USE MARKDOWN FORMATTING."
              "Write a list of changes detailed"
              "Write topics as the following example: "
              "'Command Handler Refactoring (Task 4):'."
              "Then, write the list of changes."
              "Write a detailed commit message that accurately reflects the changes."
              "The first line should be a concise summary (max 50 characters),"
              "followed by a blank line and then a more detailed description."
              "The first line should follow the conventional commit format."
            )
    if story_file:
        prompt += f"Also, uses as context reference the story on @{story_file}"

    try:
        result = subprocess.run(
            f'copilot -p "{prompt}" --allow-all-tools',
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode == 0 and result.stdout.strip():
            parsed = parse_copilot_output(result.stdout)
            if parsed:
                return parsed
            # If parsing failed, treat as no valid commit message
            return None
    except Exception:
        pass

    return None
