# Grok Build Final Boss Project Structure

**THE ULTIMATE SETUP FOR MAX CONTEXT, MODULARITY & AUTONOMY**

*Updated for 2026 — native Grok Build paths*

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
├── AGENTS.md                          # main project instructions (~200 lines max)
├── .grok/
│   ├── config.toml                    # project MCP, permissions, plugins
│   ├── skills/
│   │   ├── security-review/
│   │   │   ├── SKILL.md
│   │   │   └── checklist.md
│   │   ├── deploy/
│   │   │   └── SKILL.md
│   │   └── release/
│   │       ├── SKILL.md
│   │       └── changelog.tmpl
│   ├── agents/
│   │   ├── code-reviewer.md
│   │   ├── debugger.md
│   │   └── db-validator.md
│   ├── hooks/
│   │   ├── format.json                # → scripts/format.sh
│   │   └── protect.json               # → scripts/protect.sh
│   ├── rules/
│   │   ├── testing.md
│   │   ├── api-design.md
│   │   └── frontend/
│   │       └── react.md
│   ├── personas/                      # optional behavioral overlays
│   └── roles/                         # optional subagent role defaults
├── docs/
│   ├── architecture.md
│   └── decisions/
├── src/
│   ├── api/
│   │   └── AGENTS.md                  # scoped rules for API package
│   └── payments/
│       └── AGENTS.md                  # scoped rules for payments package
└── tools/
    ├── scripts/
    │   ├── format.sh
    │   └── protect.sh
    └── prompts/
```

> **Verify after setup:** run `grok inspect` in the project root to confirm Grok discovers your rules, skills, agents, hooks, and MCP servers.

## THE CONTEXT LADDER

1. **EVERY SESSION** → `AGENTS.md` + `.grok/rules/` (loaded from repo root to CWD)
2. **SUBDIRECTORY SCOPE** → nested `AGENTS.md` files (loaded when working in that tree)
3. **ON INVOKE** → `.grok/skills/*` via `/name` (on demand)
4. **ISOLATED** → `.grok/agents/` subagents (own context window; optional `isolation: worktree`)

## GUIDANCE vs ENFORCEMENT

**AGENTS.md / .grok/rules/ = ASKED**
Instructions Grok reads and usually follows. Conventions, commands, architecture context.

**VS**

**config.toml + hooks = FORCED**
`[permission]` deny rules block dangerous commands. `PreToolUse` / `PostToolUse` hooks in `.grok/hooks/*.json` guard before and after every tool use.

## THE AGENT LAYER

- **SUBAGENTS**: `.grok/agents/*.md` — own prompt, tools, model; spawn via `spawn_subagent` or bundled skills like `/review`
- **SKILLS**: `.grok/skills/*/SKILL.md` — repeatable workflows invoked as `/skill-name`
- **WORKTREES**: subagent `isolation: worktree`, or `/new` / `/fork --worktree` for parallel isolated sessions

## AUTO MEMORY

Enable cross-session memory with `GROK_MEMORY=1` or `[memory] enabled = true` in `~/.grok/config.toml`.

Grok stores memory in `~/.grok/memory/` (global + per-workspace). Use `/remember`, `/flush`, and `/memory` — not a repo-local `agent-memory/` folder.

## HOOKS

Hook definitions live in `.grok/hooks/*.json`. Each JSON file wires shell scripts (e.g. `tools/scripts/format.sh`) to lifecycle events (`PreToolUse`, `PostToolUse`, `SessionStart`).

Project hooks require folder trust (`/hooks-trust` or `--trust` on first run).

## GOLDEN RULES

- 📄 KEEP `AGENTS.md` UNDER ~200 LINES. Split into `.grok/rules/` when it grows.
- ▶️ LIST REAL COMMANDS (`npm test`, `build`, `lint`) so Grok can verify its own work.
- 🔒 SECRETS STAY IN `$ENV_VAR` REFERENCES. Never commit literals in `config.toml`.
- 🔗 COMMIT `.grok/` — your setup is team infrastructure.
- 🔍 RESEARCH → SUBAGENT (`explore` type) + SKILL + HOOK
- ⚖️ TRUTH & HELPFULNESS FIRST — Grok native strength: always prioritize accuracy and maximum usefulness.

## QUICK START

1. Copy the structure to your project root.
2. Customize `AGENTS.md` and `.grok/rules/` for your conventions.
3. Add project-specific subagents in `.grok/agents/`.
4. Wire guardrails in `.grok/hooks/` and permissions in `.grok/config.toml`.
5. Run `grok inspect` to confirm everything loads.

## MIGRATION FROM CLAUDE CODE FINAL BOSS

| Old (Claude-style) | Grok Build native |
|--------------------|-------------------|
| `GROK.md` / `CLAUDE.md` | `AGENTS.md` |
| `rules/` (repo root) | `.grok/rules/` |
| `skills/` (repo root) | `.grok/skills/` |
| `agents/` (repo root) | `.grok/agents/` |
| `hooks/*.sh` (repo root) | `.grok/hooks/*.json` → `tools/scripts/*.sh` |
| `.grok/settings.json` | `.grok/config.toml` (+ `~/.grok/config.toml` for global settings) |
| `agent-memory/` | `~/.grok/memory/` (built-in) |
| `workflows/*.js` | skills (`/release`) or `/execute-plan` |
| `.worktreeinclude` | subagent `isolation: worktree` |

---

*Inspired by the legendary Claude Code Final Boss setup. Adapted for Grok Build's native discovery paths, subagents, skills, hooks, and cross-session memory.*
