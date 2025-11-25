"""
Main entry point for Meerkat CLI.
"""
import sys
from .input import create_parser
from .message import print_message, print_error, get_ai_commit_message
from .git import (
    run_command, get_current_branch, get_git_status_info, create_and_push_branch,
    perform_rebase, perform_merge
)

def load_config():
    import os
    from pathlib import Path
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
    config = DEFAULT_CONFIG.copy()
    config_file = find_config_file()
    if config_file:
        config.update(parse_config_file(config_file))
    for key in DEFAULT_CONFIG.keys():
        env_value = os.environ.get(key)
        if env_value:
            config[key] = env_value
    return config

def find_config_file():
    from pathlib import Path
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
    if hasattr(args, 'verbose') and args.verbose:
        return False
    if hasattr(args, 'quiet') and args.quiet:
        return True
    return config.get('MRKT_ALWAYS_QUIET', 'false').lower() == 'true'

def main():
    parser = create_parser()
    args = parser.parse_args()
    config = load_config()
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

def handle_start_command(args, config):
    quiet = is_quiet_mode(config, args)
    prefix_type = None
    if args.feat:
        prefix_type = 'feat'
    elif args.hotfix:
        prefix_type = 'hotfix'
    elif args.release:
        prefix_type = 'release'
    branch_name = args.branch_name if args.branch_name else get_current_branch()
    full_branch_name = build_branch_name(
        config,
        prefix_type,
        branch_name,
        args.prefix,
        args.no_prefix
    )
    success = create_and_push_branch(full_branch_name, quiet)
    return 0 if success else 1

def build_branch_name(config, prefix_type, branch_name, custom_prefix, no_prefix):
    if no_prefix:
        return branch_name
    prefix = determine_prefix(config, prefix_type, custom_prefix)
    if not prefix:
        return branch_name
    separator = config.get('MRKT_PREFIX_SEPARATOR', '/')
    return f"{prefix}{separator}{branch_name}"

def determine_prefix(config, prefix_type, custom_prefix):
    if custom_prefix:
        return custom_prefix
    if prefix_type:
        return prefix_type
    return config.get('MRKT_PREFIX', 'mrkt')

def handle_save_command(args, config):
    quiet = is_quiet_mode(config, args)
    exclusive_args = [args.rebase, args.merge]
    if sum(bool(x) for x in exclusive_args) > 1:
        print_error("Only one of --rebase or --merge can be used")
        return 1
    print_message("Staging all changes...", quiet)
    if not run_command("git add .", quiet=quiet):
        return 1
    status_info = get_git_status_info()
    if status_info and not quiet:
        print_message(f"\nStaged {status_info['total_files']} file(s):", quiet)
        for file_info in status_info['files']:
            status_label = {
                'M': 'Modified',
                'A': 'Added',
                'D': 'Deleted',
                'R': 'Renamed'
            }.get(file_info['status'], file_info['status'])
            print_message(f"  [{status_label}] {file_info['name']}", quiet)
        print_message(
            f"\n+{status_info['additions']} lines added, "
            f"-{status_info['deletions']} lines removed\n",
            quiet
        )
    if args.rebase:
        if not perform_rebase(quiet):
            return 1
    elif args.merge:
        if not perform_merge(quiet):
            return 1
    commit_message = get_ai_commit_message(config, args.story, quiet)
    if not commit_message:
        return 1
    final_message = f"WIP: {commit_message}" if args.wip else commit_message
    print_message("Commit message preview:", quiet)
    print_message("─" * 50, quiet)
    print_message(final_message, quiet)
    print_message("─" * 50, quiet)
    print_message("", quiet)
    commit_command = build_commit_command(config, commit_message, args.wip)
    if not run_command(commit_command, quiet=quiet):
        return 1
    print_message("Changes committed successfully!", quiet)
    return 0

def build_commit_command(config, message, wip=False):
    if wip:
        message = f"WIP: {message}"
    no_verify = config.get('MRKT_NO_VERIFY_COMMIT', 'false').lower() == 'true' or config.get('MRKT_NO_VERIFY', 'false').lower() == 'true'
    verify_flag = " --no-verify" if no_verify else ""
    return f'git commit -m "{message}"{verify_flag}'

def handle_update_command(args, config):
    quiet = is_quiet_mode(config, args)
    exclusive_args = [args.close, args.rebase, args.merge]
    if sum(bool(x) for x in exclusive_args) > 1:
        print_error("Only one of --close, --rebase, or --merge can be used")
        return 1
    save_result = handle_save_command(args, config)
    if save_result != 0:
        return save_result
    current_branch = get_current_branch()
    if args.close:
        print_message("Merging to main branch...", quiet)
        if not run_command("git checkout main", quiet=quiet):
            return 1
        if not run_command(f"git merge {current_branch}", quiet=quiet):
            return 1
        current_branch = "main"
    print_message(f"Pushing to origin/{current_branch}...", quiet)
    push_command = build_push_command(config, current_branch)
    if not run_command(push_command, quiet=quiet):
        return 1
    print_message("Changes updated successfully!", quiet)
    return 0

def build_push_command(config, branch):
    no_verify = config.get('MRKT_NO_VERIFY_PUSH', 'false').lower() == 'true' or config.get('MRKT_NO_VERIFY', 'false').lower() == 'true'
    verify_flag = " --no-verify" if no_verify else ""
    return f"git push origin {branch}{verify_flag}"

