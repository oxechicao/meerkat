"""
Handlers for the `start` command.
"""
from .git import get_current_branch, create_and_push_branch


def handle_start_command(args, config, quiet):
    prefix_type = None
    if getattr(args, 'feat', False):
        prefix_type = 'feat'
    elif getattr(args, 'hotfix', False):
        prefix_type = 'hotfix'
    elif getattr(args, 'release', False):
        prefix_type = 'release'
    branch_name = args.branch_name if getattr(args, 'branch_name', None) else get_current_branch()
    full_branch_name = build_branch_name(
        config,
        prefix_type,
        branch_name,
        getattr(args, 'prefix', None),
        getattr(args, 'no_prefix', False)
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
