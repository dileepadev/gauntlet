# Gauntlet Documentation

Everything written about Gauntlet, organised by what you are trying to do.

> [!NOTE]
> **Gauntlet is in early development.** The corpus design and architecture are settled and documented here; the implementation is in progress. These pages describe what is being built, and are marked where they describe design rather than shipped behaviour.

## Start here

**New to AI agent security?** Read [Gauntlet in Plain English](concepts.md). It assumes no security background and no AI background beyond having used a chatbot, and it explains the single flaw that every attack in this project exploits. Fifteen minutes, and the rest of these pages will make sense.

## All pages

| Page | What it covers | Read it if |
| --- | --- | --- |
| [Gauntlet in Plain English](concepts.md) | Agents, tools, MCP, prompt injection, and what Gauntlet does about them | You are new, or you need to explain this project to someone |
| [Attack Classes Explained](attack-classes.md) | All ten attack classes, one short story each | You want to know what is actually being tested |
| [How Gauntlet Works](how-it-works.md) | The pipeline: target, case, run, trace, detect, score, report | You want to contribute code or a case |
| [Threat Model](threat-model.md) | The attacker, the trust boundaries, and the limits of any score | You are about to quote a Gauntlet result to someone |
| [Glossary](glossary.md) | Every term, defined in one or two lines | A word in another page did not land |

## Reading paths

**"I just want to understand the project."**
[Concepts](concepts.md) → [Attack Classes](attack-classes.md). Stop there. That is the whole idea.

**"I want to contribute an attack case."**
[Concepts](concepts.md) → [Attack Classes](attack-classes.md) → [How It Works](how-it-works.md) → [Threat Model](threat-model.md) (the safety rules are binding) → [CONTRIBUTING.md](../CONTRIBUTING.md).

**"I want to contribute to the harness."**
[How It Works](how-it-works.md) → the [README architecture](../README.md#architecture) → [TODO.md](../TODO.md) for what is unclaimed.

**"I am evaluating whether to use this."**
[Threat Model](threat-model.md) first — specifically [what Gauntlet does not measure](threat-model.md#what-gauntlet-does-not-measure) and [reading a score honestly](threat-model.md#reading-a-score-honestly). Then [How It Works](how-it-works.md).

**"I got lost in the jargon."**
[Glossary](glossary.md), then back to wherever you were.

## Not yet written

These land as the implementation does. See [TODO.md](../TODO.md) for progress.

- **Quickstart** — installing and running your first scan
- **Writing an adapter** — supporting a new agent system
- **Writing a case** — the corpus contribution guide
- **Reading a report card** — interpreting the output
- **CI integration** — gating builds on an agent-security score

## Elsewhere in the repository

| File | Purpose |
| --- | --- |
| [README.md](../README.md) | Project overview and roadmap |
| [TODO.md](../TODO.md) | The detailed build plan |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | How to contribute |
| [SECURITY.md](../SECURITY.md) | Reporting a vulnerability in Gauntlet itself |
| [CHANGELOG.md](../CHANGELOG.md) | Notable changes per release |
| [VERSIONING.md](../VERSIONING.md) | Versioning strategy |
