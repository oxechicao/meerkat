"""
Handlers for the `update` command.
"""
from .message import print_message, print_error
from .git import run_command, get_current_branch


def handle_update_command(args, config, quiet):
    exclusive_args = [getattr(args, 'close', False), getattr(args, 'rebase', False), getattr(args, 'merge', False)]
    if sum(bool(x) for x in exclusive_args) > 1:
        print_error("Only one of --close, --rebase, or --merge can be used")
        return 1
    # import local to avoid circular import at module import time
    from .handle_save import handle_save_command
    save_result = handle_save_command(args, config, quiet)
    if save_result != 0:
        return save_result
    current_branch = get_current_branch()
    if getattr(args, 'close', False):
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
