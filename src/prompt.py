"""
Shared prompt text and parsing utilities for AI agents.

This module exposes a `prompt` variable containing the base prompt
used to generate commit messages and a `parse_output_message` helper
that extracts the Conventional Commit message from the agent output.
"""
import re
from typing import Optional


# Base prompt used by agents. Keep as a plain string so agents can
# extend it with story file context when needed.
prompt = (
    "Generate a git commit message for the following changes in "
    "@temp_git_message_reference.md "
    "I want only the commit message. "
    "I will use this commit message directly. "
    "BE SURE TO ONLY RETURN THE COMMIT MESSAGE. "
    "DO NOT USE MARKDOWN FORMATTING. "
    "Write a list of changes detailed "
    "Write topics as the following example: "
    "'Command Handler Refactoring (Task 4):'. "
    "Then, write the list of changes. "
    "Write a detailed commit message that accurately reflects the changes. "
    "The first line should be a concise summary (max 50 characters), "
    "followed by a blank line and then a more detailed description. "
    "The first line should follow the conventional commit format."
)


def parse_output_message(output: str) -> Optional[str]:
    """
    Extract the commit message starting from a Conventional Commit header.

    Returns the text from the first line that matches a Conventional Commit
    header (e.g. "feat(scope): summary") until the end. Returns `None`
    if no matching header is found or the output is empty.
    """
    if not output:
        return None

    pattern = re.compile(r"^[a-z]+(?:\([^\)]*\))?(?:!)?:\s+.+", re.IGNORECASE)

    lines = output.splitlines()
    for idx, line in enumerate(lines):
        if pattern.match(line.strip()):
            return "\n".join(lines[idx:]).strip()

    return None
