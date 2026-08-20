"""Tests for the target adapter interface."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from gauntlet.targets import Target, TargetError
from gauntlet.types import Role, ToolResult, ToolSpec, Turn


class FakeTarget:
    """A minimal in-memory target, standing in for a real adapter."""

    def __init__(self, tools: Sequence[ToolSpec]) -> None:
        self._tools = tuple(tools)
        self.calls: list[tuple[str, Mapping[str, Any]]] = []

    @property
    def name(self) -> str:
        return "fake"

    def list_tools(self) -> Sequence[ToolSpec]:
        return self._tools

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> ToolResult:
        self.calls.append((name, arguments))
        return ToolResult(name=name, content="ok")

    def converse(self, prompt: str) -> Sequence[Turn]:
        return (Turn(role=Role.USER, text=prompt), Turn(role=Role.MODEL, text="done"))


def test_structural_target_satisfies_protocol() -> None:
    """Adapters conform structurally — no base class to inherit from."""
    target = FakeTarget([ToolSpec("t", "d")])
    assert isinstance(target, Target)


def test_target_accepts_a_structural_implementation() -> None:
    def drive(target: Target) -> str:
        return target.name

    assert drive(FakeTarget([])) == "fake"


def test_call_tool_records_arguments() -> None:
    target = FakeTarget([ToolSpec("read_file", "Read a file.")])
    result = target.call_tool("read_file", {"path": "/srv/reports/q3.csv"})

    assert result.name == "read_file"
    assert target.calls == [("read_file", {"path": "/srv/reports/q3.csv"})]


def test_target_error_is_a_runtime_error() -> None:
    assert issubclass(TargetError, RuntimeError)
