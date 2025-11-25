"""
Handler for the `help` command.
"""


def handle_help_command(parser):
    parser.print_help()
    return 0
