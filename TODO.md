# TODO

This file tracks tasks, improvements, and features planned for upcoming updates or releases of this repository.

> [!NOTE]
> This list is **not exhaustive** and may change over time. Items within a milestone are roughly ordered, but milestones themselves are sequenced deliberately — later ones depend on earlier ones.

## Table of Contents

- [TODO](#todo)
  - [Table of Contents](#table-of-contents)
  - [How to read this list](#how-to-read-this-list)
  - [Current focus](#current-focus)
  - [Stage 0 — Harness and corpus](#stage-0--harness-and-corpus)
    - [0.1 Project scaffolding](#01-project-scaffolding)
    - [0.2 Target protocol and MCP stdio adapter](#02-target-protocol-and-mcp-stdio-adapter)
    - [0.3 Trace capture](#03-trace-capture)
    - [0.4 First case, end to end](#04-first-case-end-to-end)
    - [0.5 Three attack classes](#05-three-attack-classes)
    - [0.6 Multi-run scoring](#06-multi-run-scoring)
    - [0.7 Report card](#07-report-card)
    - [0.8 Scan and publish real targets](#08-scan-and-publish-real-targets)
  - [Stage 1 — Distribution](#stage-1--distribution)
  - [Stage 2 — Enforcement](#stage-2--enforcement)
  - [Documentation](#documentation)
  - [Decisions](#decisions)
  - [Open questions](#open-questions)
  - [Explicitly not doing yet](#explicitly-not-doing-yet)
  - [Completed](#completed)

## How to read this list

- **Milestones** map to the stages in the [README roadmap](README.md#roadmap). The README states the destination; this file states the steps.
- **Each task is sized to be one branch and one pull request.** If a task cannot be reviewed in one sitting, it needs splitting.
- **Suggested branch names** follow the [branch naming guidelines](BRANCH_NAMING_GUIDELINES.md).
- **"Done when"** is the acceptance test for the milestone. A milestone is not finished because its boxes are ticked — it is finished when that sentence is true.
- **Blocked by** means the work cannot start until the referenced milestone ships.

## Current focus

**Milestone 0.2 — Target protocol and MCP stdio adapter.**

Scaffolding is done: the project builds, lints, type-checks under `mypy --strict`, and tests green in CI. The core vocabulary (`ToolSpec`, `ToolCall`, `ToolResult`, `Turn`, `Verdict`, `Severity`) and the `Target` protocol are implemented and tested.

Next is the first real adapter — launching an MCP server over stdio, listing its tools verbatim, and calling one — proven against a controllable fake server in the test suite.

## Stage 0 — Harness and corpus

The goal of Stage 0 is a harness that can run one attack against one target and produce a defensible number, then enough corpus to make that number interesting.

### 0.1 Project scaffolding

> **Done when:** `git clone` → install → `pytest` passes on a clean machine, and CI runs lint, types and tests on every pull request.

Branch: `chore/scaffolding`

- [x] Confirm the toolchain — Python 3.12+, `uv` for environments, `hatchling` as the build backend (`uv_build` would pin the backend to the uv version, and contributors building with `pip` should not have to care)
- [x] Add `pyproject.toml` with project metadata and a `gauntlet` console entry point
- [x] Create the package skeleton under `src/gauntlet/` — `types.py`, `targets/`, `detectors/`, `cli.py`. `runner.py`, `trace.py`, `score.py` and `report.py` deliberately land in their own milestones rather than as empty stubs, which would make coverage and strict typing report false confidence
- [x] Add `ruff` for linting and formatting, with config in `pyproject.toml`
- [x] Add `mypy` in strict mode — this codebase is protocol-heavy and types carry real weight here
- [x] Add `pytest` with a `tests/` directory and one smoke test
- [x] Add a Python `.gitignore`
- [x] Add `.github/workflows/ci.yml` — lint, type-check and test on push and pull request
- [x] Add `markdownlint` to CI, since this repository is documentation-heavy
- [x] Fix the six broken relative links in `.github/PULL_REQUEST_TEMPLATE.md`, the malformed fence and missing ToC entries in `VERSIONING.md`, and the `feat/` versus `feature/` contradiction between the branch and pull request guidelines
- [x] Fix [VERSIONING.md](VERSIONING.md) release steps — they reference `package.json`, inherited from a template; this project bumps `pyproject.toml`

### 0.2 Target protocol and MCP stdio adapter

> **Done when:** Gauntlet can start a real MCP server, list its tools, call one, and get a result back — proven against a fake server in the test suite.

Branches: `feat/target-protocol`, `feat/mcp-stdio-target`

- [x] Define the `Target` protocol: `list_tools()`, `call_tool()`, `converse()`
- [x] Define the shared data types: `ToolSpec`, `ToolCall`, `ToolResult`, `Turn`, plus `Verdict` and `Severity`
- [ ] Decide the target configuration format (YAML) — command, args, env, model, guardrail settings
- [ ] Implement `targets/mcp_stdio.py` — launch the server as a subprocess, speak MCP over stdin/stdout, handle startup, timeouts and teardown
- [ ] Write a controllable fake MCP server in `tests/fixtures/` so adapter behaviour is testable without a real server or a live model
- [ ] Handle the failure modes explicitly: server will not start, server hangs, server returns malformed responses
- [ ] Wire `converse()` to a model provider, with the provider configurable
- [ ] `targets/mcp_http.py` — the HTTP transport *(can trail the stdio adapter)*
- [ ] Document the adapter interface in `docs/writing-an-adapter.md`

### 0.3 Trace capture

> **Done when:** a run produces a JSON trace containing every tool call and argument, including parameters that never appeared in any UI.

Branch: `feat/trace`

- [ ] Implement `trace.py` — ordered events with timestamps: `tools_listed`, `user_turn`, `tool_call`, `tool_result`, `model_turn`
- [ ] Capture the tool list **as the target presented it**, descriptions included — this is the evidence for tool-poisoning cases
- [ ] Capture full arguments, including undeclared and hidden parameters
- [ ] Define a versioned JSON schema (`trace_version`) and serialise to it
- [ ] Add a redaction hook so traces are safe to publish, with configurable patterns for secrets and tokens
- [ ] Golden-file tests over recorded trace fixtures
- [ ] Add trace replay, so a detector can be developed and debugged without re-running a model

### 0.4 First case, end to end

> **Done when:** `gauntlet run tool-poisoning/description-instruction-injection --target my-agent.yaml` prints a verdict backed by a trace.

Branch: `feat/first-case`

- [ ] Define the case directory format: `case.yaml`, `payload/`, `expected.md`, `detector.py`
- [ ] Define the `case.yaml` schema: `id`, `class`, `severity`, `owasp`, `description`, `requires_tools`, `runs`
- [ ] Implement the case loader with validation and clear errors for malformed cases
- [ ] Implement `runner.py` — set up payload, drive the target, capture the trace, invoke the detector, tear down and restore
- [ ] Build the shared detector primitives in `detectors/`: `tool_called()`, `arg_contains()`, `call_order()`, `egress_to()`
- [ ] Define the `Verdict` type: `EXPLOITED`, `SAFE`, `ERROR` — and make sure `ERROR` is never silently scored as `SAFE`
- [ ] Build the local exfiltration sink — records what arrives, forwards nothing, asserts on receipt
- [ ] Write `corpus/tool-poisoning/description-instruction-injection/` as the reference case that every later case is modelled on
- [ ] Add the `gauntlet run` CLI command
- [ ] Guarantee teardown on failure — a crashed run must not leave a poisoned server running or a seeded file on disk

### 0.5 Three attack classes

> **Done when:** three classes have enough cases that a score across them is meaningful, and someone outside the project can add a fourth without reading the runner.

Branches: `feat/corpus-tool-poisoning`, `feat/corpus-cross-tool`, `feat/corpus-exfiltration`

- [ ] **Tool poisoning** — 4–6 cases: description injection, schema-field injection, instructions in enum values, unicode and homoglyph obfuscation, multi-server poisoning
- [ ] **Cross-tool contamination** — 4–6 cases: injection via search results, via file contents, via issue and ticket bodies, via API responses, via error messages
- [ ] **Exfiltration chains** — 4–6 cases: read then send, encode then send, chunked across multiple calls, exfiltration via URL parameters, exfiltration via an allowed webhook
- [ ] Write the case-authoring guide in `docs/writing-a-case.md`
- [ ] Add a `gauntlet new-case` scaffolder so contributors start from a valid skeleton
- [ ] Add a corpus safety checklist, enforced in the pull request template for case contributions
- [ ] Add CI validation for the corpus: schema-valid, detector importable, no live external endpoints
- [ ] Decide and document how cases declare which tools a target must have to be applicable

### 0.6 Multi-run scoring

> **Done when:** running the same case five times produces a rate and a flakiness signal, not a coin flip.

Branch: `feat/scoring`

- [ ] Run each case N times, recording a verdict per run
- [ ] Implement `score.py` — per-case success rate, per-class aggregate, severity-weighted overall
- [ ] Flag unstable cases rather than averaging their variance away
- [ ] Decide the severity weights and write down the reasoning
- [ ] Support deterministic seeding where the target allows it, and document clearly where it does not
- [ ] Implement comparison mode: two scans of one target → per-class delta
- [ ] Handle `ERROR` verdicts in scoring — excluded from the rate, reported separately, never counted as safe
- [ ] Parallelise runs, with concurrency capped to respect provider rate limits

### 0.7 Report card

> **Done when:** a scan produces a Markdown report a human wants to read and a JSON report a CI job can gate on.

Branch: `feat/report`

- [ ] Markdown report — headline score, per-class table, per-case detail, trace excerpt as evidence for each failure
- [ ] HTML report, self-contained and shareable
- [ ] `results.json` with a stable, versioned schema for CI consumption
- [ ] `gauntlet scan` — run the full corpus against a target
- [ ] `gauntlet report` and `gauntlet compare` for rendering and diffing
- [ ] Make the before-and-after delta the visual centrepiece of the comparison report
- [ ] Make the report state its own limits — corpus version, target version, run count, date

### 0.8 Scan and publish real targets

> **Done when:** `results/` holds published scans of several real targets, with methodology and versions pinned, and `v0.1.0` is tagged.

Branch: `docs/published-results`

- [ ] Choose the initial targets — a mix of MCP clients, MCP servers and at least one agent firewall
- [ ] Extend [SECURITY.md](SECURITY.md) with the disclosure policy for third-party findings, including the timeline
- [ ] Contact maintainers and disclose before publishing anything
- [ ] Define the `results/` layout: one directory per target-version, trace excerpts included, redacted
- [ ] Publish the guardrails-off versus guardrails-on delta for at least one target — this is the headline result
- [ ] Write the methodology page so results can be reproduced and challenged
- [ ] Update `CHANGELOG.md` and tag `v0.1.0` per [VERSIONING.md](VERSIONING.md)

## Stage 1 — Distribution

*Blocked by Stage 0.*

> **Done when:** someone who has never seen this repository can gate their build on an agent-security score.

- [ ] Publish to PyPI, with a `uvx gauntlet` / `pipx` install path
- [ ] Ship a first-run experience that produces a useful result within five minutes
- [ ] Build the GitHub Action, with a configurable score threshold and per-class thresholds
- [ ] Emit a pull request comment showing the score delta against the base branch
- [ ] Define the attack-pack format so cases can be distributed from outside this repository
- [ ] Add pack discovery and installation (`gauntlet pack add ...`)
- [ ] Write the full contribution guidelines for corpus cases, promised in the [README](README.md#contributing)
- [ ] Set up a corpus versioning policy — scores are only comparable within a corpus version, and that has to be visible
- [ ] Add a public results index, so scans across targets can be compared

## Stage 2 — Enforcement

*Blocked by Stage 1.*

> **Done when:** `gauntlet guard` blocks an attack that the corpus proves is dangerous, and can cite the case ID that justifies each rule.

- [ ] Write the design document for `gauntlet guard` before any code
- [ ] Implement the MCP proxy sitting between client and server
- [ ] Design the rule format, with every rule linked to the corpus case that justifies it
- [ ] Implement inbound checks: tool schema validation, description scanning, schema pinning against what was approved
- [ ] Implement outbound checks: argument inspection, egress allowlisting, chain detection across calls
- [ ] Add an audit log, in the same trace format the harness already uses
- [ ] **Scan the guard with Gauntlet itself** and publish the result — a defence that ships without its own report card is the exact problem this project was built to address
- [ ] Measure and document the latency cost of running behind the guard

## Documentation

Runs alongside implementation rather than after it.

- [x] Beginner-friendly documentation set in [docs/](docs/) — concepts, attack classes, how it works, threat model, glossary
- [ ] `docs/quickstart.md` — install and first scan *(blocked by 0.7)*
- [ ] `docs/writing-an-adapter.md` *(blocked by 0.2)*
- [ ] `docs/writing-a-case.md` *(blocked by 0.5)*
- [ ] `docs/reading-a-report.md` — how to interpret and how not to over-read a score *(blocked by 0.7)*
- [ ] `docs/ci-integration.md` *(blocked by Stage 1)*
- [ ] Architecture decision records for the choices worth remembering: trace-based detection, multi-run scoring, corpus-as-directories
- [ ] Diagrams for the pipeline and the trust boundaries — current versions are Mermaid, which is fine, but the README could use one
- [ ] Keep `docs/` honest as implementation lands — remove the "design, not shipped code" notes as each becomes shipped code

## Decisions

Resolved, with the reasoning recorded so they can be revisited rather than re-argued.

- **Toolchain** — Python 3.12+, `uv`, `hatchling` build backend, `ruff` for lint and format, `mypy --strict`, `pytest`. Line length 100.
- **Default `runs` count** — **5**. Enough to distinguish "blocked" from "blocked most of the time", cheap enough to run in CI. Overridable per case in `case.yaml`.
- **Cases the target cannot support** — a fourth verdict, `SKIPPED`, reported separately and excluded from the score. Counting them safe would inflate every report card; hiding them would conceal coverage gaps. `ERROR` is treated the same way, for the same reason.
- **Is the model part of the target?** — yes. The model is named in the target config, because a different model is a different measurement. Sweeping a corpus across several models is a Stage 1 CLI feature, not a property of the target.
- **First model provider** — Anthropic, behind a provider protocol, with OpenAI next and Ollama shortly after. Ollama matters disproportionately: contributors should be able to run the corpus without spending money, or the corpus stops receiving contributions.
- **Trace format** — versioned from the first commit (`trace_version`), kept internal for now. Whether to publish it as a spec other tools can emit is a Stage 1 question, once its shape has stopped moving.

## Open questions

- [ ] **How does the corpus stay current?** An unmaintained attack corpus quietly stops being meaningful while still producing confident numbers. Needs a stated review cadence and a way for a report card to show the age of the corpus it was scored against.
- [ ] **How are severity weights justified?** They are currently 1 / 3 / 8 / 20 for low through critical. The ordering is defensible; the specific ratios are not yet, and they move the headline number.
- [ ] **What is the minimum evidence a published finding carries?** Trace excerpt is settled. Whether a full replayable trace ships with each published scan affects how large `results/` gets and how much redaction has to be trusted.

## Explicitly not doing yet

Recorded so these are decisions rather than oversights.

- **All ten attack classes before three are solid.** Shallow coverage of everything produces a number that looks thorough and means nothing.
- **An LLM-as-judge detector.** Non-reproducible, and one more thing an attacker can talk around.
- **Live third-party endpoints in any payload.** The local sink is the only exfiltration destination, permanently.
- **A hosted service or dashboard.** The CLI and the CI action come first.
- **Fine-tuning or training defensive models.** This project measures; it does not train.
- **Long-horizon and cross-session attacks.** Real and worth doing, but they need a persistence model the harness does not have yet.

## Completed

- [x] Repository community standards — [README.md](README.md), [LICENSE](LICENSE), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), issue and pull request templates
- [x] Project positioning and architecture design, documented in the [README](README.md)
- [x] Attack corpus design — ten classes, with the first three chosen for depth over breadth
- [x] Beginner-friendly documentation set in [docs/](docs/)
- [x] Milestone 0.1 — project scaffolding: `pyproject.toml`, package skeleton, ruff, `mypy --strict`, pytest, and a four-job CI workflow
- [x] Core types and the `Target` protocol, at 100% test coverage
