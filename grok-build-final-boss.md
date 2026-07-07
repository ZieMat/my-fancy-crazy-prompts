# Grok Build Final Boss Project Structure

**THE ULTIMATE SETUP FOR MAX CONTEXT, MODULARITY & AUTONOMY**

*Updated for 2026 - Optimized for Grok & xAI*

## WHAT IS THIS?

A production-grade Grok Build setup that gives you:

- Lower context cost
- Modular prompts
- Persistent memory
- Automated guardrails
- Multi-agent workflows
- Native tool-use & truth-seeking integration

## FOLDER STRUCTURE

```
final-boss-grok-project/
├── README.md
├── GROK.md
├── GROK.local.md
├── AGENTS.md
├── .grok.json
├── .worktreeinclude
├── .grok/
│   ├── settings.json
│   └── settings.local.json
├── rules/
│   ├── testing.md
│   ├── api-design.md
│   └── frontend/
│       └── react.md
├── skills/
│   ├── security-review/
│   │   ├── SKILL.md
│   │   └── checklist.md
│   ├── deploy/
│   │   └── SKILL.md
│   └── release/
│       ├── SKILL.md
│       └── changelog.tmpl
├── agents/
│   ├── code-reviewer.md
│   ├── debugger.md
│   └── db-validator.md
├── workflows/
│   └── release-train.js
├── agent-memory/
│   └── debugger/
│       └── MEMORY.md
├── hooks/
│   ├── format.sh
│   └── protect.sh
├── observability/
│   └── usage-metrics.md
├── output-styles/
│   └── review-mode.md
├── docs/
│   ├── architecture.md
│   └── decisions/
├── src/
│   ├── api/
│   │   └── GROK.md
│   └── payments/
│       └── GROK.md
└── tools/
    ├── scripts/
    └── prompts/
```

## THE CONTEXT LADDER

1. **EVERY SESSION** → GROK.md + rules/ (no paths)
2. **PATH-GATED** → rules/*.md with paths (lazy load)
3. **ON INVOKE** → skills/* via /name (on demand)
4. **ISOLATED** → agents/ & workflows/ (own context)

## GUIDANCE vs ENFORCEMENT

**GROK.md / rules = ASKED**
Instructions Grok reads and usually follows. Conventions, commands, architecture context.

**VS**

**settings + hooks = FORCED**
permissions.deny blocks dangerous commands. Pre/PostToolUse formats every edit. Scripts wired in settings.json guard before & after every tool use.

## THE AGENT LAYER

- **SUBAGENTS**: agents/*.md – Own prompt, tools, model & memory
- **WORKFLOWS**: workflows/*.js – Orchestrate many subagents from one command
- **WORKTREES**: .worktreeinclude – Parallel agents on isolated checkouts with full .env

## AUTO MEMORY

Grok writes, you commit. Persists across sessions in agent-memory/ and ~/.grok/projects/

## HOOKS

Scripts wired in .grok/settings.json. Guardrails before & after every tool use. Integrated with Git hooks for team consistency.

## GOLDEN RULES

- 📄 KEEP GROK.md UNDER ~200 LINES. Split into rules/ when it grows.
- ▶️ LIST REAL COMMANDS (npm test, build, lint) so Grok can verify its own work.
- 🔒 SECRETS STAY IN $ENV_VAR REFERENCES. Never in .grok.json literally.
- 🔗 COMMIT .grok/ + .gitignore *.local.* Your setup is team infrastructure.
- 🔍 RESEARCH → SUBAGENT PROCEDURE + SKILL GUARANTEE + HOOK
- ⚖️ TRUTH & HELPFULNESS FIRST – Grok native strength: always prioritize accuracy and maximum usefulness.

## QUICK START & IMPROVEMENTS INCORPORATED

1. Copy structure to your project root.
2. Customize GROK.md and rules/ for your conventions.
3. Add your project-specific agents in agents/.
4. Use observability/ to track token usage and agent performance.
5. When starting session with Grok, reference AGENTS.md and relevant rules.

This template incorporates all improvements from the original Claude Code evaluation: central README, standardized skill/agent formats, explicit CI/Git integration examples, and team-ready .gitignore rules.

---

*Inspired by the legendary Claude Code Final Boss setup. Adapted and enhanced for Grok's strengths in tool-use, real-time reasoning and creative problem solving.*