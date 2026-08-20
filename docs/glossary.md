# Glossary

Every term used across Gauntlet's documentation, defined in one or two plain sentences. Skim it, or use it as a lookup when a word in another page does not land.

Terms are grouped by what they belong to rather than alphabetically, because the concepts make more sense in clusters. Use your browser's find-in-page for a specific word.

## Table of Contents

- [Glossary](#glossary)
  - [Table of Contents](#table-of-contents)
  - [Agents and models](#agents-and-models)
  - [Protocols and plumbing](#protocols-and-plumbing)
  - [Attacks](#attacks)
  - [Defences](#defences)
  - [Gauntlet's own vocabulary](#gauntlets-own-vocabulary)
  - [Where to go next](#where-to-go-next)

## Agents and models

**LLM (Large Language Model)** — the text-prediction model underneath a chatbot. Reads text, writes text. On its own it cannot do anything else.

**Agent** — an LLM that has been given tools it can call. The difference between a system that answers you and a system that acts for you.

**Tool** — a function the model is allowed to invoke: read a file, send an email, query a database. Also called a function or an action.

**Tool description** — the written explanation attached to a tool so the model knows when to use it. The model treats it as an operating instruction, which is what makes it worth poisoning.

**Tool schema** — the machine-readable declaration of a tool's name, description and parameters.

**Tool call** — one invocation of a tool by the model, with concrete arguments. The atomic unit Gauntlet measures.

**Context** — everything the model can currently see: your messages, the tool descriptions, previous tool outputs, fetched content. All of it is one flat stream of text with no reliable trust markers.

**Context window** — the maximum amount of text a model can hold at once. Exceeding it forces something to be dropped, and what gets dropped is not always what you would choose.

**System prompt** — the instructions placed at the start of context to set the agent's rules. Influential, but not privileged: it is text in the same stream as everything else.

**Non-determinism** — the same input to the same model can produce different outputs on different runs. This is why Gauntlet scores across N runs rather than one.

## Protocols and plumbing

**MCP (Model Context Protocol)** — an open standard for exposing tools to agents, so any compliant client can use any compliant server. The USB-C port of agent tooling.

**MCP server** — a program that publishes a bundle of tools over MCP.

**MCP client** — the application that connects to MCP servers and gives their tools to a model. Your IDE assistant or desktop agent is usually the client.

**stdio** — standard input/output. One MCP transport: the client launches the server as a subprocess and they talk over pipes.

**HTTP transport** — the other common MCP transport, over the network rather than a subprocess.

**Adapter** — Gauntlet's translation layer that makes a target speak the runner's three-method interface: `list_tools()`, `call_tool()`, `converse()`.

## Attacks

**Prompt injection** — text that the model treats as an instruction when it was supposed to be data. The root cause of nearly everything in the corpus.

**Direct injection** — the attacker types the malicious instruction into the agent themselves.

**Indirect injection** — the attacker plants the instruction somewhere the agent will later read: a web page, a README, an issue, a file. They never touch your agent.

**Payload** — the actual malicious text or artefact a case plants.

**Tool poisoning** — hiding the attack in a tool's own description or schema, so it enters context at install time.

**Cross-tool contamination** — one tool's output carrying instructions that hijack a different tool.

**Hidden parameters** — schema fields the client UI never displays but the model still populates. Defeats human approval precisely because the human approved what they were shown.

**Rug-pull** — a tool that is benign when reviewed and mutates after it has been trusted.

**Exfiltration** — moving sensitive data out of a system that should have kept it in.

**Exfiltration chain** — an exfiltration assembled from steps that are each individually unremarkable. Read, encode, send.

**SSRF (Server-Side Request Forgery)** — coercing a system into making requests to addresses the attacker could not reach directly, such as internal services or a cloud metadata endpoint.

**Egress** — outbound network traffic. "Egress control" means restricting where a system may send data.

**Metadata endpoint** — a special address inside a cloud VM (classically `169.254.169.254`) that returns credentials to whoever asks from inside. A favourite SSRF destination.

**Privilege escalation** — chaining low-risk capabilities to achieve a high-risk effect that no single tool was permitted to produce.

**Confused deputy** — a privileged party tricked into using its authority on behalf of someone who lacks that authority. Agents are excellent confused deputies, because acting for others is their job.

**Context overflow** — flooding context with junk so that safety instructions are diluted or truncated away.

**Red team** — people who attack a system deliberately in order to find its weaknesses before someone hostile does.

**Threat model** — an explicit statement of who the attacker is, what they can do, and what you are and are not defending against.

**OWASP LLM Top 10** — the industry-standard list of the ten most critical LLM application risks. Gauntlet cases cite their identifiers (LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, and so on) where they apply.

## Defences

**Guardrail** — any control that constrains what an agent may do or say. Usually a classifier, a policy engine, or a filter.

**Agent firewall** — a proxy sitting between an MCP client and server, inspecting and blocking tool calls by policy.

**DLP (Data Loss Prevention)** — controls that detect and block sensitive data leaving a system.

**Injection classifier** — a model trained to spot prompt-injection attempts in text.

**Human in the loop** — requiring a person to approve an action before it executes. Strong against many attacks, and specifically defeated by hidden parameters.

**Allowlist** — an explicit list of what is permitted, with everything else denied. The safer default over blocklists, which only stop what you thought to name.

## Gauntlet's own vocabulary

**Target** — the system under test: an MCP server, an agent framework, or a firewall-wrapped configuration.

**Corpus** — the full collection of attack cases.

**Case** — one attack, as a directory: metadata, payload, expected-safe behaviour, detector.

**Case class** — the attack family a case belongs to, such as `tool_poisoning`. Scores aggregate by class.

**Runner** — the component that sets up a case, drives the target, records the trace, and tears down.

**Trace** — the ordered recording of every tool call, argument, result and turn produced during a run. Gauntlet's evidence.

**Detector** — a small function that reads a trace and returns a verdict. Reads actions, never prose.

**Verdict** — the outcome of one run of one case: `EXPLOITED`, `SAFE`, or `ERROR`.

**Local sink** — a server Gauntlet runs to receive simulated exfiltration. Records what arrives, forwards nothing, so "the secret escaped" is measurable without any secret escaping.

**Report card** — the generated summary of a scan: per-class scores, severity weighting, evidence excerpts.

**Delta** — the difference between two scans of the same target, typically guardrails off versus on. The most useful number Gauntlet produces.

**Severity weighting** — scoring that counts a high-severity failure for more than a low-severity one, so the headline number reflects real exposure.

**Attack pack** — a distributable set of corpus cases maintained outside this repository. Planned for Stage 1.

## Where to go next

- [Gauntlet in Plain English](concepts.md) — these terms in context
- [Attack Classes Explained](attack-classes.md) — the attack terms as stories
- [How Gauntlet Works](how-it-works.md) — the Gauntlet terms as a pipeline
