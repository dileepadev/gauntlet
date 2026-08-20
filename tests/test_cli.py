"""Tests for the command-line entry point."""

from __future__ import annotations

import pytest

from gauntlet import __version__
from gauntlet.cli import main


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])

    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_status_reports_current_milestone(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--status"]) == 0
    out = capsys.readouterr().out
    assert "early development" in out
    assert "TODO.md" in out


def test_no_arguments_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert "usage: gauntlet" in capsys.readouterr().out
