# Kilo Code Final Boss Project Structure

**THE ULTIMATE SETUP FOR MAX CONTEXT, MODULARITY & AUTONOMY WITH KILO CODE**

*Updated for 2026 – Custom Rules, Agent Modes, Multi-Model Routing, AGENTS.md First*

## WHAT IS THIS?

A production-grade Kilo Code setup that gives you:

- Persistent project context via AGENTS.md (core of Kilo)
- Custom rules scanned from `kilo code/rules/`
- Built-in Agent Modes (Architect/Plan, Code, Debug, Ask, Custom)
- Intelligent multi-model routing (Grok, Claude, local models...)
- Lower context cost, modular prompts, automated guardrails, multi-agent orchestration

## FOLDER STRUCTURE (KILO NATIVE)

```
final-boss-kilo-project/
├── README.md
├── AGENTS.md                 # Main persistent context (Kilo loads this first)
├── KILO.md                  # Additional Kilo-specific instructions
├── kilo code/               # Scanned by Kilo Code for custom configs
│   └── rules/
│       ├── coding-standards.md
│       ├── testing.md
│       ├── architecture.md
│       └── security.md
├── skills/
│   ├── security-review/
│   │   └── SKILL.md
│   └── deploy/
│       └── SKILL.md
├── agents/
│   ├── architect.md
│   ├── debugger.md
│   └── reviewer.md
├── workflows/
│   └── release-train.js
├── agent-memory/
│   └── default/
│       └── MEMORY.md
├── hooks/
│   ├── pre-task.sh
│   └── post-edit.sh
├── observability/
│   └── usage-metrics.md
├── docs/
│   ├── architecture.md
│   └── decisions/
└── src/
    └── ... (your code with optional local KILO.md)
```

## THE CONTEXT LADDER (KILO ADAPTED)

1. **EVERY SESSION** → AGENTS.md + kilo code/rules/ (Kilo auto-loads)
2. **PATH-GATED** → kilo code/rules/*.md with paths (lazy loaded per task)
3. **ON INVOKE** → skills/* or custom agent modes (on demand)
4. **ISOLATED** → agents/ & workflows/ (dedicated context per mode)

## GUIDANCE vs ENFORCEMENT

**AGENTS.md / kilo code/rules/ = ASKED**
Kilo loads these markdown files and follows your project standards, coding conventions and architecture decisions.

**VS**

**Kilo Settings + local hooks = FORCED**
Use Kilo's built-in guardrails + local pre/post scripts to enforce formatting, security scans and dangerous command blocks regardless of model output.

## THE AGENT LAYER & MODES

Kilo ships with powerful built-in modes – use them!

- **Architect / Plan mode**: Design before coding (highly recommended for complex tasks)
- **Code mode**: Implementation and editing
- **Debug mode**: Root cause analysis and fixes
- **Ask mode**: Questions and exploration
- **Custom modes**: Defined in rules/ or AGENTS.md

**SUBAGENTS**: Extend with agents/*.md for specialized roles (reviewer, db-expert...)
**WORKFLOWS**: Orchestrate multi-mode or multi-model flows

## MODEL ROUTING (KILO SUPERPOWER)

- Grok → Fast iteration, creative solutions, tool-use heavy tasks
- Claude → Deep reasoning, complex architecture, high precision
- Local / cheaper models → Simple refactors and boilerplate
- Document preferred model per rule/skill in kilo code/rules/

## AUTO MEMORY

Kilo maintains context across interactions. Commit updates to AGENTS.md and agent-memory/. Use for long-running projects.

## HOOKS & OBSERVABILITY

Local hooks in hooks/ run before/after Kilo actions. Track token usage, mode switches and model costs in observability/.

## GOLDEN RULES (KILO EDITION)

- 📄 KEEP AGENTS.md UNDER ~300 LINES. This is Kilo's primary context source – keep it focused.
- 🚀 ALWAYS START COMPLEX TASKS IN ARCHITECT MODE
- ▶️ LIST REAL COMMANDS & TEST COMMANDS so Kilo can self-verify
- 🔒 SECRETS IN ENV VARS ONLY
- 🔗 COMMIT `kilo code/` and AGENTS.md – team infrastructure
- 🔍 USE THE RIGHT MODE + RIGHT MODEL for every subtask
- ⚖️ TRUTH FIRST – even when switching models, demand accuracy

## QUICK START

1. Add the folder structure to your project.
2. Write your project standards, tech decisions and coding rules into **AGENTS.md**.
3. Create reusable rules in `kilo code/rules/` (Kilo will discover them).
4. In Kilo Code IDE/CLI switch to **Architect** mode for planning, then **Code** mode for implementation.
5. Customize model routing in your rules files.
6. Use observability/ to monitor and improve your agentic workflow.

All previous improvements from Claude Code evaluation are included: central README, standardized SKILL.md format, explicit Git/CI hooks, team sharing rules, and observability.

---

*Adapted from the Claude Code Final Boss and Grok Build templates. Tailored specifically for Kilo Code's unique strengths: open multi-model support, built-in agent personas, and powerful custom rules system.*

## SAMPLE AGENTS.md (copy & customize)

```markdown
# Project AGENTS.md for Kilo Code

You are an expert software engineer working in this project.

## Core Principles
- Always use Architect mode for new features or refactors > 3 files
- Follow the rules in kilo code/rules/
- Prefer Grok for speed, Claude for complex logic
- Write self-documenting code
- Run tests before committing

## Tech Stack
- ...

## Coding Standards
- ...
```

## SAMPLE RULE (kilo code/rules/coding-standards.md)

```markdown
# Coding Standards

- Use TypeScript strict mode
- Prefer functional patterns where possible
- All public functions must have JSDoc
- Error handling: never swallow errors
```
