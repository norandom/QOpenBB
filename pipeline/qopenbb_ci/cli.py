"""Expose package identity without advertising unimplemented delivery commands."""

import argparse

from qopenbb_ci import __version__


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    parser.parse_args()
    parser.print_help()
