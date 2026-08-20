"""Command-line entry point.

Deliberately minimal while the harness is being built. Subcommands land with the
milestones that make them meaningful: ``run`` in 0.4, ``scan`` and ``compare``
in 0.7. Shipping stubs that accept arguments and then do nothing would be worse
than shipping nothing.
"""

from __future__ import annotations

import argparse
import platform
import sys
from collections.abc import Sequence

from gauntlet import __version__

__all__ = ["main"]

_DESCRIPTION = "An adversarial test harness for AI agent systems."

_STATUS = """\
Gauntlet is in early development and cannot scan a target yet.

Implemented:
  - Core types and the target adapter interface

Next:
  - MCP stdio adapter          (milestone 0.2)
  - Trace capture              (milestone 0.3)
  - First case, end to end     (milestone 0.4)

Plan:  https://github.com/dileepadev/gauntlet/blob/main/TODO.md
Docs:  https://github.com/dileepadev/gauntlet/blob/main/docs/README.md
"""


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gauntlet", description=_DESCRIPTION)
    parser.add_argument(
        "--version",
        action="version",
        version=f"gauntlet {__version__}",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="show which milestones are implemented",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI. Returns the process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.status:
        print(_STATUS, end="")
        print(f"Running on Python {platform.python_version()}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
