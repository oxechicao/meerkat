"""
Handlers for the `save` command.
"""
from .message import print_message, print_error, get_ai_commit_message
from .git import run_command, get_git_status_info, perform_rebase, perform_merge


def handle_save_command(args, config, quiet):
    exclusive_args = [getattr(args, 'rebase', False), getattr(args, 'merge', False)]
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

    if getattr(args, 'rebase', False):
        if not perform_rebase(quiet):
            return 1
    elif getattr(args, 'merge', False):
        if not perform_merge(quiet):
            return 1

    commit_message = get_ai_commit_message(config, getattr(args, 'story', None), quiet)
    if not commit_message:
        return 1

    final_message = f"WIP: {commit_message}" if getattr(args, 'wip', False) else commit_message
    print_message("Commit message preview:", quiet)
    print_message("─" * 50, quiet)
    print_message(final_message, quiet)
    print_message("─" * 50, quiet)
    print_message("", quiet)
    commit_command = build_commit_command(config, commit_message, getattr(args, 'wip', False))
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
