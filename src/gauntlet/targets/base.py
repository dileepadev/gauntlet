"""The interface every target adapter implements.

A *target* is whatever is being tested: an MCP server over stdio, an MCP server
over HTTP, or an agent framework's own tool-calling loop. An *adapter* makes one
of those look like the three methods below.

Adding support for a new agent system means writing one adapter. It does not
mean touching the runner, the corpus, or the scorer — that separation is what
lets the corpus grow without coordination.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol, runtime_checkable

from gauntlet.types import ToolResult, ToolSpec, Turn

__all__ = ["Target", "TargetError"]


class TargetError(RuntimeError):
    """The target could not be reached, started, or driven.

    Raised for transport-level failures — a server that will not start, a
    timeout, a malformed response. The runner turns this into ``Verdict.ERROR``
    rather than letting it look like safe behaviour: a target that crashed has
    not demonstrated anything about its security.
    """


@runtime_checkable
class Target(Protocol):
    """A system under test, reduced to three operations."""

    @property
    def name(self) -> str:
        """Human-readable identifier, used in reports and trace metadata."""
        ...

    def list_tools(self) -> Sequence[ToolSpec]:
        """Return the tools exactly as the target presents them.

        Descriptions and schemas must be returned verbatim, including anything
        that looks like an injected instruction. Sanitising here would destroy
        the evidence that tool-poisoning cases exist to capture.
        """
        ...

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> ToolResult:
        """Invoke a tool directly, bypassing the model.

        Used by case setup and teardown, and by detectors that need to observe
        side effects. This is the harness pressing the button itself.
        """
        ...

    def converse(self, prompt: str) -> Sequence[Turn]:
        """Send a prompt and let the model decide which tools to call.

        This is where the interesting failures happen, because the decision to
        call a tool is the model's rather than the harness's. Returns every turn
        produced, including the tool calls made along the way.
        """
        ...
