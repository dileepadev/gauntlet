# Gauntlet

**Prove whether your agent setup can actually be exploited.**

Gauntlet is an adversarial test harness for AI agent systems. Point it at your MCP servers, your agent framework, or your agent firewall, and it runs a corpus of real attack classes and returns a reproducible report card: what got through, what was blocked, and what your configuration is genuinely exposed to.

> [!NOTE]
> **Status: early development.** The corpus design and architecture below are settled; implementation is in progress. Nothing here is usable yet. Watch the repo or check the roadmap for current state.

## Why this exists

Open-source defences for AI agents arrived fast: policy-enforcing proxies that sit between an MCP client and server, inbound and outbound tool-call checks, DLP and egress control, injection classifiers, and guardrail frameworks from major labs. The defensive layer is well served.

## What's missing is the proof

Nearly every one of these tools asserts its own efficacy without shipping the adversarial suite that would demonstrate it. And when researchers red-teamed a set of widely used MCP clients in early 2026, they found significant disparities between them — some clients well guarded, others susceptible to cross-tool poisoning, hidden parameter exploitation, and unauthorized tool invocation. That work was a paper, not a tool anyone can run against their own stack.

So the question this project answers is not *"how do I block attacks?"* but:

> Given my actual configuration, which attacks currently succeed?

## What it does

1. **Targets** an agent system through an adapter — an MCP server over stdio or HTTP, or an agent framework's tool-calling loop.
2. **Runs** a corpus of attack cases against it, capturing a full trace of every tool call and argument.
3. **Detects** outcomes from the trace rather than from model text, so results are reproducible and arguable.
4. **Scores** per attack class, weighted by severity, across multiple runs to account for model non-determinism.
5. **Reports** a Markdown or HTML report card, and can run in CI to catch regressions.

### The most useful number

Run the same target twice — guardrails off, then on — and Gauntlet reports the delta. That single comparison is what lets anyone, including firewall authors, demonstrate that a defence actually works.

## Attack corpus

Each case is a directory containing setup, payload, expected-safe behaviour, and a detector. Cases map to OWASP LLM Top 10 identifiers where applicable.

| Class | What it tests |
| --- | --- |
| Tool poisoning | Malicious instructions embedded in a tool's description or schema |
| Cross-tool contamination | Tool A's output hijacking tool B |
| Hidden parameters | Schema fields invisible in the client UI but populated by the model |
| Rug-pull | Tool schema benign at install, mutated after trust is established |
| Indirect injection | Payload arriving via fetched page, README, issue, or file content |
| Exfiltration chains | Read secret → encode → send through an allowed tool |
| SSRF / egress | Tool coerced into reaching internal IPs or metadata endpoints |
| Privilege escalation | Chaining low-risk tools into a high-risk effect |
| Context overflow | Flooding context to displace safety instructions |
| Confused deputy | Agent applying its own credentials on behalf of untrusted input |

Initial release covers tool poisoning, cross-tool contamination, and exfiltration chains properly, rather than all ten shallowly.

## Scope and ethics

This is a test harness for systems you control, not an attack toolkit.

- Payloads target **your own configured systems only**.
- Simulated exfiltration goes to a **local sink**. No live third-party endpoints.
- No working malware, no credential theft against real services, no payloads designed to damage systems.
- Findings against third-party software are disclosed responsibly before publication.

If you cannot run a case safely against your own infrastructure, it does not belong in the corpus.

## Architecture

```tree
gauntlet/
├── corpus/                    # attack cases: metadata, payload, detector
├── src/gauntlet/
│   ├── targets/               # mcp_stdio | mcp_http | framework adapters
│   ├── runner.py              # executes a case against a target
│   ├── trace.py               # captures every tool call and argument
│   ├── detectors/             # shared detection primitives
│   ├── score.py               # per-class and severity-weighted scoring
│   └── report.py              # report card generation
├── results/                   # published scans
└── docs/                      # concepts, attack classes, threat model, glossary
```

Adding a new target is a new adapter implementing `list_tools()`, `call_tool()`, and `converse()`. Adding a new attack is a new corpus directory. Neither requires touching the runner.

## Documentation

New to agent security? [**Gauntlet in Plain English**](docs/concepts.md) explains the whole idea with no security background assumed.

| Page | What it covers |
| --- | --- |
| [Gauntlet in Plain English](docs/concepts.md) | Agents, tools, MCP, prompt injection, and what Gauntlet does about them |
| [Attack Classes Explained](docs/attack-classes.md) | All ten classes above, one short story each |
| [How Gauntlet Works](docs/how-it-works.md) | The pipeline: target, case, run, trace, detect, score, report |
| [Threat Model](docs/threat-model.md) | The attacker, the trust boundaries, and the limits of any score |
| [Glossary](docs/glossary.md) | Every term, defined in one or two lines |

Full index in [docs/](docs/README.md).

## Roadmap

The detailed, milestone-by-milestone build plan lives in [TODO.md](TODO.md).

### Stage 0 — Harness and corpus

- [ ] Target protocol and MCP stdio adapter
- [ ] Trace capture
- [ ] First complete case, end to end, with detector
- [ ] Three attack classes, multi-run scoring
- [ ] Report card generation
- [ ] Scan and publish results for several real targets

### Stage 1 — Distribution

- [ ] Installable CLI
- [ ] GitHub Action to gate builds on an agent-security score
- [ ] Community-contributable attack packs

### Stage 2 — Enforcement

- [ ] `gauntlet guard`: a proxy that blocks what the corpus proves is dangerous — shipping with the evidence behind each rule

## Contributing

Attack cases are the most valuable contribution. A good case is reproducible, safely scoped, and comes with a detector that reads the trace rather than the model's text. Start with [How Gauntlet Works](docs/how-it-works.md) and the safety rules in the [threat model](docs/threat-model.md#safety-rules-for-the-corpus); full contribution guidelines for cases will follow the first release.

## Author

Built by [Dileepa Bandara](https://dileepa.dev) — AI Engineer working on agents, MCP, and retrieval systems.
