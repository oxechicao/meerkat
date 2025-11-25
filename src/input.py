"""
Argument parsing and input validation for Meerkat CLI.
"""
import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        prog='mrkt',
        description='A command-line tool to work with AI libraries for development'
    )
    parser.add_argument('--quiet', action='store_true', help='Only error messages are printed')
    parser.add_argument('--verbose', action='store_true', help='Show all messages')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    start_parser = subparsers.add_parser('start', help='Create a branch and push it to origin')
    start_parser.add_argument('branch_name', nargs='?', help='Name of the branch to create')
    start_parser.add_argument('--feat', action='store_true', help='Use feature as prefix')
    start_parser.add_argument('--hotfix', action='store_true', help='Use hotfix as prefix')
    start_parser.add_argument('--release', action='store_true', help='Use release as prefix')
    start_parser.add_argument('--prefix', type=str, help='Define a custom prefix')
    start_parser.add_argument('--no-prefix', action='store_true', help="Don't add any prefix")
    start_parser.add_argument('--quiet', action='store_true', help='Only error messages are printed')
    start_parser.add_argument('--verbose', action='store_true', help='Show all messages')
    save_parser = subparsers.add_parser('save', help='Create a commit with AI-generated message (no push)')
    save_parser.add_argument('--wip', action='store_true', help='Add WIP in the title of the message')
    save_parser.add_argument('--rebase', action='store_true', help='Rebase before commit')
    save_parser.add_argument('--merge', action='store_true', help='Merge main into branch before commit')
    save_parser.add_argument('--story', type=str, help='Path to story definition file for context')
    save_parser.add_argument('--quiet', action='store_true', help='Only error messages are printed')
    save_parser.add_argument('--verbose', action='store_true', help='Show all messages')
    update_parser = subparsers.add_parser('update', help='Create a commit message with AI and push to origin')
    update_parser.add_argument('--wip', action='store_true', help='Add WIP in the title of the message')
    update_parser.add_argument('--close', action='store_true', help='Commit changes and merge to main branch')
    update_parser.add_argument('--rebase', action='store_true', help='Rebase before commit and push')
    update_parser.add_argument('--merge', action='store_true', help='Merge main into branch before commit and push')
    update_parser.add_argument('--story', type=str, help='Path to story definition file for context')
    update_parser.add_argument('--quiet', action='store_true', help='Only error messages are printed')
    update_parser.add_argument('--verbose', action='store_true', help='Show all messages')
    subparsers.add_parser('help', help='Show help message')
    return parser
