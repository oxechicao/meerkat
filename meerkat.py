#!/usr/bin/env python3
"""
Meerkat (mrkt) - A command-line tool to work with AI libraries for development.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


# Configuration defaults
DEFAULT_CONFIG = {
    'MRKT_AGENT': 'copilot',
    'MRKT_AGENT_PATH': '',
    'MRKT_PREFIX': 'mrkt',
    'MRKT_PREFIX_SEPARATOR': '/',
    'MRKT_ALWAYS_QUIET': 'false',
    'MRKT_NO_VERIFY': 'false',
    'MRKT_NO_VERIFY_COMMIT': 'false',
    'MRKT_NO_VERIFY_PUSH': 'false',
}


def load_config():
    """Load configuration from .meerkatrc file and environment variables."""
    config = DEFAULT_CONFIG.copy()

    # Try to find .meerkatrc file
    config_file = find_config_file()
    if config_file:
        config.update(parse_config_file(config_file))

    # Override with environment variables
    for key in DEFAULT_CONFIG.keys():
        env_value = os.environ.get(key)
        if env_value:
            config[key] = env_value

    return config


def find_config_file():
    """Find .meerkatrc file in current directory or parent directories."""
    current = Path.cwd()

    while current != current.parent:
        config_path = current / '.meerkatrc'
        if config_path.exists():
            return config_path

        git_path = current / '.git'
        if git_path.exists():
            return current / '.meerkatrc' if (current / '.meerkatrc').exists() else None

        current = current.parent

    return None


def parse_config_file(config_path):
    """Parse .meerkatrc configuration file."""
    config = {}
    try:
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except Exception as e:
        print_error(f"Error reading config file: {e}")

    return config


def is_quiet_mode(config, args):
    """Determine if quiet mode should be enabled."""
    if hasattr(args, 'verbose') and args.verbose:
        return False

    if hasattr(args, 'quiet') and args.quiet:
        return True

    return config.get('MRKT_ALWAYS_QUIET', 'false').lower() == 'true'


def print_message(message, quiet=False):
    """Print message if not in quiet mode."""
    if not quiet:
        print(message)


def print_error(message):
    """Print error message to stderr."""
    print(f"Error: {message}", file=sys.stderr)


def run_command(command, capture_output=False, quiet=False):
    """Run a shell command and return the result."""
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
            print_error(f"Command failed: {command}")
            if capture_output and e.stderr:
                print_error(e.stderr)
        return None


def get_current_branch():
    """Get the current git branch name."""
    branch = run_command(
        "git rev-parse --abbrev-ref HEAD",
        capture_output=True,
        quiet=True
    )
    return branch if branch else "main"


def build_branch_name(config, prefix_type, branch_name, custom_prefix, no_prefix):
    """Build the full branch name with prefix."""
    if no_prefix:
        return branch_name

    prefix = determine_prefix(config, prefix_type, custom_prefix)
    if not prefix:
        return branch_name

    separator = config.get('MRKT_PREFIX_SEPARATOR', '/')
    return f"{prefix}{separator}{branch_name}"


def determine_prefix(config, prefix_type, custom_prefix):
    """Determine which prefix to use."""
    if custom_prefix:
        return custom_prefix

    if prefix_type:
        return prefix_type

    return config.get('MRKT_PREFIX', 'mrkt')


def create_and_push_branch(full_branch_name, quiet=False):
    """Create a new branch and push it to origin."""
    print_message(f"Creating branch: {full_branch_name}", quiet)

    # Create and checkout new branch
    if not run_command(f"git checkout -b {full_branch_name}", quiet=quiet):
        return False

    print_message("Pushing branch to origin...", quiet)

    # Push branch to origin
    if not run_command(f"git push -u origin {full_branch_name}", quiet=quiet):
        return False

    print_message("Branch created and pushed successfully!", quiet)
    return True


def get_ai_commit_message(config, story_file=None, quiet=False):
    """Generate commit message using AI agent."""
    agent_path = config.get('MRKT_AGENT_PATH')
    agent_name = config.get('MRKT_AGENT', 'copilot')

    # Get git diff
    diff_command = "git diff --cached"
    diff = run_command(diff_command, capture_output=True, quiet=True)

    if not diff:
        print_error("No staged changes to commit")
        return None

    # Build AI command
    if agent_path:
        ai_command = agent_path
    else:
        ai_command = agent_name

    # Build prompt
    prompt = "Generate a git commit message for the following changes:\n\n"
    prompt += diff

    if story_file and os.path.exists(story_file):
        with open(story_file, 'r') as f:
            story_content = f.read()
            prompt = f"Story context:\n{story_content}\n\n{prompt}"

    print_message("Generating commit message with AI...", quiet)

    # For now, using a placeholder - in real implementation,
    # this would call the actual AI agent
    # This is a simplified version - actual implementation depends on the AI CLI
    try:
        # Attempt to use GitHub Copilot CLI or similar
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

    # Fallback: generate simple message from diff
    return generate_simple_commit_message(diff)


def generate_simple_commit_message(diff):
    """Generate a simple commit message from diff."""
    # Extract file names from diff
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


def perform_rebase(quiet=False):
    """Rebase current branch on main."""
    print_message("Rebasing on main...", quiet)

    # Fetch latest changes
    if not run_command("git fetch origin main", quiet=quiet):
        return False

    # Rebase
    if not run_command("git rebase origin/main", quiet=quiet):
        return False

    return True


def perform_merge(quiet=False):
    """Merge main into current branch."""
    print_message("Merging main into branch...", quiet)

    # Fetch latest changes
    if not run_command("git fetch origin main", quiet=quiet):
        return False

    # Merge
    if not run_command("git merge origin/main", quiet=quiet):
        return False

    return True


def build_commit_command(config, message, wip=False):
    """Build the git commit command with appropriate flags."""
    if wip:
        message = f"WIP: {message}"

    no_verify = should_skip_verify_commit(config)
    verify_flag = " --no-verify" if no_verify else ""

    return f'git commit -m "{message}"{verify_flag}'


def build_push_command(config, branch):
    """Build the git push command with appropriate flags."""
    no_verify = should_skip_verify_push(config)
    verify_flag = " --no-verify" if no_verify else ""

    return f"git push origin {branch}{verify_flag}"


def should_skip_verify_commit(config):
    """Check if --no-verify should be used for commits."""
    if config.get('MRKT_NO_VERIFY_COMMIT', 'false').lower() == 'true':
        return True

    if config.get('MRKT_NO_VERIFY', 'false').lower() == 'true':
        return True

    return False


def should_skip_verify_push(config):
    """Check if --no-verify should be used for push."""
    if config.get('MRKT_NO_VERIFY_PUSH', 'false').lower() == 'true':
        return True

    if config.get('MRKT_NO_VERIFY', 'false').lower() == 'true':
        return True

    return False


def handle_start_command(args, config):
    """Handle the start command."""
    quiet = is_quiet_mode(config, args)

    # Determine prefix type
    prefix_type = None
    if args.feat:
        prefix_type = 'feat'
    elif args.hotfix:
        prefix_type = 'hotfix'
    elif args.release:
        prefix_type = 'release'

    # Get branch name
    branch_name = args.branch_name if args.branch_name else get_current_branch()

    # Build full branch name
    full_branch_name = build_branch_name(
        config,
        prefix_type,
        branch_name,
        args.prefix,
        args.no_prefix
    )

    # Create and push branch
    success = create_and_push_branch(full_branch_name, quiet)
    return 0 if success else 1


def handle_save_command(args, config):
    """Handle the save command - stage changes and commit with AI message."""
    quiet = is_quiet_mode(config, args)

    # Validate arguments
    exclusive_args = [args.rebase, args.merge]
    if sum(bool(x) for x in exclusive_args) > 1:
        print_error("Only one of --rebase or --merge can be used")
        return 1

    # Stage all changes
    print_message("Staging all changes...", quiet)
    if not run_command("git add .", quiet=quiet):
        return 1

    # Perform rebase or merge if requested
    if args.rebase:
        if not perform_rebase(quiet):
            return 1
    elif args.merge:
        if not perform_merge(quiet):
            return 1

    # Generate commit message
    commit_message = get_ai_commit_message(config, args.story, quiet)
    if not commit_message:
        return 1

    print_message(f"Commit message: {commit_message}", quiet)

    # Create commit
    commit_command = build_commit_command(config, commit_message, args.wip)
    if not run_command(commit_command, quiet=quiet):
        return 1

    print_message("Changes committed successfully!", quiet)
    return 0


def handle_update_command(args, config):
    """Handle the update command - commit with AI message and push to origin."""
    quiet = is_quiet_mode(config, args)

    # Validate arguments
    exclusive_args = [args.close, args.rebase, args.merge]
    if sum(bool(x) for x in exclusive_args) > 1:
        print_error("Only one of --close, --rebase, or --merge can be used")
        return 1

    # Use handle_save_command to stage and commit
    save_result = handle_save_command(args, config)
    if save_result != 0:
        return save_result

    # Get current branch
    current_branch = get_current_branch()

    # Handle --close option
    if args.close:
        print_message("Merging to main branch...", quiet)
        if not run_command("git checkout main", quiet=quiet):
            return 1

        if not run_command(f"git merge {current_branch}", quiet=quiet):
            return 1

        current_branch = "main"

    # Push changes
    print_message(f"Pushing to origin/{current_branch}...", quiet)
    push_command = build_push_command(config, current_branch)
    if not run_command(push_command, quiet=quiet):
        return 1

    print_message("Changes updated successfully!", quiet)
    return 0


def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='mrkt',
        description='A command-line tool to work with AI libraries for development'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only error messages are printed'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show all messages'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # START command
    start_parser = subparsers.add_parser(
        'start',
        help='Create a branch and push it to origin'
    )

    start_parser.add_argument(
        'branch_name',
        nargs='?',
        help='Name of the branch to create'
    )

    start_parser.add_argument(
        '--feat',
        action='store_true',
        help='Use feature as prefix'
    )

    start_parser.add_argument(
        '--hotfix',
        action='store_true',
        help='Use hotfix as prefix'
    )

    start_parser.add_argument(
        '--release',
        action='store_true',
        help='Use release as prefix'
    )

    start_parser.add_argument(
        '--prefix',
        type=str,
        help='Define a custom prefix'
    )

    start_parser.add_argument(
        '--no-prefix',
        action='store_true',
        help="Don't add any prefix"
    )

    start_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only error messages are printed'
    )

    start_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show all messages'
    )

    # SAVE command
    save_parser = subparsers.add_parser(
        'save',
        help='Create a commit with AI-generated message (no push)'
    )

    save_parser.add_argument(
        '--wip',
        action='store_true',
        help='Add WIP in the title of the message'
    )

    save_parser.add_argument(
        '--rebase',
        action='store_true',
        help='Rebase before commit'
    )

    save_parser.add_argument(
        '--merge',
        action='store_true',
        help='Merge main into branch before commit'
    )

    save_parser.add_argument(
        '--story',
        type=str,
        help='Path to story definition file for context'
    )

    save_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only error messages are printed'
    )

    save_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show all messages'
    )

    # UPDATE command
    update_parser = subparsers.add_parser(
        'update',
        help='Create a commit message with AI and push to origin'
    )

    update_parser.add_argument(
        '--wip',
        action='store_true',
        help='Add WIP in the title of the message'
    )

    update_parser.add_argument(
        '--close',
        action='store_true',
        help='Commit changes and merge to main branch'
    )

    update_parser.add_argument(
        '--rebase',
        action='store_true',
        help='Rebase before commit and push'
    )

    update_parser.add_argument(
        '--merge',
        action='store_true',
        help='Merge main into branch before commit and push'
    )

    update_parser.add_argument(
        '--story',
        type=str,
        help='Path to story definition file for context'
    )

    update_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only error messages are printed'
    )

    update_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show all messages'
    )

    # HELP command
    subparsers.add_parser(
        'help',
        help='Show help message'
    )

    return parser


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Load configuration
    config = load_config()

    # Handle commands
    if not args.command or args.command == 'help':
        parser.print_help()
        return 0

    if args.command == 'start':
        return handle_start_command(args, config)
    elif args.command == 'save':
        return handle_save_command(args, config)
    elif args.command == 'update':
        return handle_update_command(args, config)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
