# Kilo Code Final Boss → Grok Build

**THE ULTIMATE SETUP FOR MAX CONTEXT, MODULARITY & AUTONOMY**

*Updated for 2026 — adapted from Kilo Code Final Boss to native Grok Build paths*

> This template originated as a Kilo Code setup. The structure below is remapped to what Grok Build actually discovers and loads at runtime. Use `grok inspect` to verify.

## WHAT IS THIS?

A production-grade Grok Build setup that gives you:

- Persistent project context via `AGENTS.md`
- Modular rules in `.grok/rules/`
- Plan mode + specialized subagents (architect, debug, explore)
- Per-subagent model routing in `config.toml`
- Lower context cost, automated guardrails, multi-agent orchestration

## FOLDER STRUCTURE

```
final-boss-grok-project/
├── README.md
├── AGENTS.md                          # main project instructions (~200 lines max)
├── .grok/
│   ├── config.toml                    # MCP, permissions, subagent model routing
│   ├── skills/
│   │   ├── security-review/
│   │   │   ├── SKILL.md
│   │   │   └── checklist.md
│   │   └── deploy/
│   │       └── SKILL.md
│   ├── agents/
│   │   ├── architect.md               # planning / design subagent
│   │   ├── debugger.md                # root-cause analysis subagent
│   │   └── reviewer.md                # code review subagent
│   ├── hooks/
│   │   ├── pre-task.json              # → tools/scripts/pre-task.sh
│   │   └── post-edit.json             # → tools/scripts/post-edit.sh
│   ├── rules/
│   │   ├── coding-standards.md
│   │   ├── testing.md
│   │   ├── architecture.md
│   │   └── security.md
│   ├── personas/                      # optional behavioral overlays
│   └── roles/                         # optional subagent role defaults
├── docs/
│   ├── architecture.md
│   └── decisions/
├── src/
│   └── ...                            # optional per-package AGENTS.md
└── tools/
    ├── scripts/
    │   ├── pre-task.sh
    │   └── post-edit.sh
    └── prompts/
```

> **Verify after setup:** `grok inspect` in the project root.

## ANALYSIS: WHAT DID NOT WORK (KILO ORIGINAL)

| Kilo Code element | Grok Build verdict |
|-------------------|--------------------|
| `KILO.md` | ❌ Not a recognized instruction file — use `AGENTS.md` |
| `kilo code/rules/` | ❌ Not scanned — use `.grok/rules/` |
| `skills/` (repo root) | ❌ Not discovered — use `.grok/skills/` |
| `agents/` (repo root) | ❌ Not discovered — use `.grok/agents/` |
| `hooks/*.sh` (repo root) | ❌ Hooks need `.grok/hooks/*.json` definitions |
| `agent-memory/` | ❌ Use built-in `~/.grok/memory/` + `/remember` |
| `workflows/*.js` | ❌ Use skills (`/release`) or `/execute-plan` |
| `observability/` | ⚠️ Manual notes only — use `/context` and `grok inspect` |
| Path-gated lazy rules | ⚠️ Partial — nested `AGENTS.md` loads on demand; `.grok/rules/` loads from root→CWD |
| Built-in Kilo modes UI | ⚠️ No 1:1 UI — mapped to Plan mode + subagent types (see below) |
| Multi-model per rule file | ⚠️ No per-rule model field — use `config.toml`, agent defs, skill frontmatter |

## THE CONTEXT LADDER

1. **EVERY SESSION** → `AGENTS.md` + `.grok/rules/` (loaded from repo root to CWD)
2. **SUBDIRECTORY SCOPE** → nested `AGENTS.md` files (loaded when working in that tree)
3. **ON INVOKE** → `.grok/skills/*` via `/name` (on demand)
4. **ISOLATED** → `.grok/agents/` subagents (own context; optional `isolation: worktree`)

## KILO MODES → GROK BUILD EQUIVALENTS

| Kilo Code mode | Grok Build equivalent |
|----------------|----------------------|
| Architect / Plan | Plan mode (`/plan`, `enter_plan_mode`) or `plan` subagent |
| Code | Default Grok Build session |
| Debug | `.grok/agents/debugger.md` subagent |
| Ask / Explore | `explore` subagent (`capability_mode: read-only`) |
| Custom | `.grok/agents/*.md` or `.grok/roles/*.toml` |

## MODEL ROUTING

Grok Build routes models via `config.toml`, agent definitions, and skill frontmatter — not via markdown rule files.

```toml
# ~/.grok/config.toml or project overrides where supported
[subagents.models]
explore = "grok-build"          # fast research
plan = "grok-build"              # deep planning

[subagents.toggle]
plan = true
explore = true
```

Per-agent override in `.grok/agents/architect.md` frontmatter:

```yaml
---
model: grok-build
description: Design before coding
tools:
  - read_file
  - grep_search
  - list_dir
disallowedTools:
  - search_replace
---
```

Per-skill override in `SKILL.md` frontmatter: `model: grok-build`.

## GUIDANCE vs ENFORCEMENT

**AGENTS.md / .grok/rules/ = ASKED**
Instructions Grok reads and usually follows.

**VS**

**config.toml + hooks = FORCED**
`[permission]` deny rules block dangerous commands. `PreToolUse` / `PostToolUse` hooks guard every tool use.

## AUTO MEMORY

Enable with `GROK_MEMORY=1` or `[memory] enabled = true` in `~/.grok/config.toml`.

Use `/remember`, `/flush`, `/memory` — not a repo-local `agent-memory/` folder. Update `AGENTS.md` for durable team conventions.

## HOOKS

Definitions in `.grok/hooks/*.json` pointing to `tools/scripts/*.sh`. Project hooks require `/hooks-trust` or `--trust`.

## GOLDEN RULES

- 📄 KEEP `AGENTS.md` UNDER ~200 LINES. Split into `.grok/rules/` when it grows.
- 🚀 START COMPLEX TASKS IN PLAN MODE (`/plan`) before multi-file implementation
- ▶️ LIST REAL COMMANDS (`npm test`, `build`, `lint`) so Grok can self-verify
- 🔒 SECRETS IN `$ENV_VAR` ONLY — never commit literals in `config.toml`
- 🔗 COMMIT `.grok/` + `AGENTS.md` — team infrastructure
- 🔍 RESEARCH → `explore` subagent; IMPLEMENT → default session; REVIEW → `/review` or reviewer agent
- ⚖️ TRUTH FIRST — prioritize accuracy over speed

## QUICK START

1. Copy the structure to your project root.
2. Write standards and tech decisions into `AGENTS.md`.
3. Add reusable rules in `.grok/rules/`.
4. For complex features: `/plan` first, then implement in the main session.
5. Configure model routing in `config.toml` and agent/skill frontmatter.
6. Run `grok inspect` to confirm discovery.

## MIGRATION FROM KILO CODE FINAL BOSS

| Kilo Code | Grok Build native |
|-----------|-------------------|
| `KILO.md` | `AGENTS.md` (merge content) |
| `kilo code/rules/` | `.grok/rules/` |
| `skills/` (root) | `.grok/skills/` |
| `agents/` (root) | `.grok/agents/` |
| `hooks/*.sh` | `.grok/hooks/*.json` → `tools/scripts/*.sh` |
| `agent-memory/` | `~/.grok/memory/` |
| `workflows/*.js` | skills or `/execute-plan` |
| `observability/` | `/context`, `grok inspect` |
| Kilo Architect mode | `/plan` or `plan` subagent |
| Kilo Debug mode | `debugger` subagent in `.grok/agents/` |
| Model per rule file | `[subagents.models]` + agent/skill `model:` |

## SAMPLE AGENTS.md

```markdown
# Project AGENTS.md

You are an expert software engineer working in this project.

## Core Principles
- Use `/plan` for new features or refactors touching > 3 files
- Follow rules in `.grok/rules/`
- Research with `explore` subagent; implement in main session
- Write self-documenting code
- Run tests before committing

## Tech Stack
- ...

## Commands
- Test: `npm test`
- Lint: `npm run lint`
- Build: `npm run build`
```

## SAMPLE RULE (.grok/rules/coding-standards.md)

```markdown
# Coding Standards

- Use TypeScript strict mode
- Prefer functional patterns where possible
- All public functions must have JSDoc
- Error handling: never swallow errors
```

---

*Adapted from the Kilo Code Final Boss and Claude Code Final Boss templates. Remapped to Grok Build's native discovery paths, Plan mode, subagents, skills, hooks, and cross-session memory.*
