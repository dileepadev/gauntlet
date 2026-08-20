"""Gauntlet: an adversarial test harness for AI agent systems.

Gauntlet runs a corpus of real attack cases against an agent configuration and
reports which ones actually succeeded, judged from a trace of what the agent
did rather than from what it said about itself.

See https://github.com/dileepadev/gauntlet for the threat model and the
scope-and-ethics rules that govern the corpus.
"""

from gauntlet.types import (
    Role,
    Severity,
    ToolCall,
    ToolResult,
    ToolSpec,
    Turn,
    Verdict,
)

__version__ = "0.0.1"

__all__ = [
    "Role",
    "Severity",
    "ToolCall",
    "ToolResult",
    "ToolSpec",
    "Turn",
    "Verdict",
    "__version__",
]
