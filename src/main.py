"""
Main entry point for Meerkat CLI.
"""
import sys
from .input import create_parser
from .message import print_error
from .handle_start import handle_start_command
from .handle_save import handle_save_command
from .handle_update import handle_update_command
from .handle_help import handle_help_command

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
        return handle_help_command(parser)
    quiet = is_quiet_mode(config, args)
    if args.command == 'start':
        return handle_start_command(args, config, quiet)
    elif args.command == 'save':
        return handle_save_command(args, config, quiet)
    elif args.command == 'update':
        return handle_update_command(args, config, quiet)
    else:
        parser.print_help()
        return 1


