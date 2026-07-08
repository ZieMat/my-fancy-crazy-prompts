# Kilo Code Final Boss Project Structure

**THE ULTIMATE SETUP FOR MAX CONTEXT, MODULARITY & AUTONOMY WITH KILO CODE**

*Updated for 2026 — native Kilo Code paths (VS Code extension & CLI)*

## WHAT IS THIS?

A production-grade Kilo Code setup that gives you:

- Persistent project context via `AGENTS.md`
- Modular custom rules in `.kilo/rules/` (wired through `kilo.jsonc`)
- Built-in agents: **code**, **plan**, **ask**, **debug**
- Custom agents and subagents in `.kilo/agents/`
- Skills on demand in `.kilo/skills/`
- Workflows as slash commands in `.kilo/commands/`
- Multi-model routing per agent (`provider/model` format)

> Docs: [kilo.ai/docs/customize](https://kilo.ai/docs/customize) · Verify agents with `kilo agent list`

## FOLDER STRUCTURE (KILO NATIVE)

```
final-boss-kilo-project/
├── README.md
├── AGENTS.md                          # primary project context (~300 lines max)
├── kilo.jsonc                         # project config: instructions, agents, skills
├── .kilo/
│   ├── rules/
│   │   ├── coding-standards.md
│   │   ├── testing.md
│   │   ├── architecture.md
│   │   └── security.md
│   ├── skills/
│   │   ├── security-review/
│   │   │   ├── SKILL.md
│   │   │   └── checklist.md
│   │   └── deploy/
│   │       └── SKILL.md
│   ├── agents/
│   │   ├── reviewer.md                # custom primary or subagent
│   │   └── test-engineer.md
│   ├── commands/
│   │   └── release-train.md           # workflow → /release-train
│   └── plans/                         # plan agent writes here (auto-managed)
├── docs/
│   ├── architecture.md
│   └── decisions/
└── src/
    ├── api/
    │   └── AGENTS.md                  # loaded when agent reads files here
    └── payments/
        └── AGENTS.md
```

### Example `kilo.jsonc`

```jsonc
{
  "$schema": "https://app.kilo.ai/config.json",
  "instructions": [
    ".kilo/rules/*.md"
  ],
  "agent": {
    "code": {
      "model": "xai/grok-4",
      "temperature": 0.3
    },
    "plan": {
      "model": "anthropic/claude-sonnet-4-20250514"
    },
    "reviewer": {
      "description": "Read-only security and style review",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "permission": {
        "edit": "deny",
        "bash": "deny"
      }
    }
  },
  "skills": {
    "paths": []
  }
}
```

## WHAT WAS WRONG IN THE OLD TEMPLATE

| Old element | Kilo Code verdict |
|-------------|-------------------|
| `KILO.md` | ❌ Not recognized — use `AGENTS.md` |
| `kilo code/rules/` (with space) | ❌ Use `.kilo/rules/` + `instructions` in `kilo.jsonc` |
| `skills/` (repo root) | ❌ Use `.kilo/skills/` |
| `agents/` (repo root) | ❌ Use `.kilo/agents/` or `.kilo/agent/` |
| `workflows/*.js` | ❌ Use `.kilo/commands/*.md` (slash commands) |
| `agent-memory/` | ❌ Deprecated — migrate to `AGENTS.md` |
| `hooks/*.sh` (repo root) | ⚠️ Not a native hook system — use permissions in `kilo.jsonc` or shell integration |
| `observability/` | ⚠️ Manual notes — track usage via Kilo settings / provider dashboards |
| Model per rule file | ❌ Route models via `kilo.jsonc` `agent.<name>.model` or agent `.md` frontmatter |

## THE CONTEXT LADDER

1. **EVERY SESSION** → `AGENTS.md` (auto-loaded at project root)
2. **RULES** → `.kilo/rules/` via `instructions` in `kilo.jsonc` (global + project merge)
3. **ON DEMAND** → `.kilo/skills/*/SKILL.md` (agent reads when task matches `description`)
4. **PER DIRECTORY** → nested `AGENTS.md` (loaded when agent reads files in that tree)
5. **ISOLATED** → subagents (`mode: subagent`) or `/command` with `subtask: true`

### Instruction priority (highest first)

| Priority | Source |
|----------|--------|
| 1 | Agent prompt (`agent.<name>.prompt` or `.md` body) |
| 2 | Project `instructions` in `kilo.jsonc` |
| 3 | `AGENTS.md` at project root |
| 4 | Global `instructions` in `~/.config/kilo/kilo.jsonc` |
| 5 | Skills (loaded on demand) |

## GUIDANCE vs ENFORCEMENT

**AGENTS.md / .kilo/rules/ = ASKED**
Markdown instructions Kilo follows on a best-effort basis.

**VS**

**kilo.jsonc `permission` + agent `permission` = FORCED**
Tool access (`edit`, `bash`, `read`, `task`, etc.) with `allow` / `deny` / `ask`. Last matching glob rule wins.

## THE AGENT LAYER

### Built-in agents (use these first)

| Agent | Use for |
|-------|---------|
| **plan** | Architecture and implementation plans (writes to `.kilo/plans/` only) |
| **code** | Default implementation and editing |
| **debug** | Systematic troubleshooting |
| **ask** | Read-only Q&A and exploration |

Switch agents: agent picker, `/agents`, or `Ctrl+.` / `Cmd+.`

### Custom agents & subagents

- **Primary agents**: `.kilo/agents/*.md` with `mode: primary` or `mode: all`
- **Subagents**: `mode: subagent` — invoked via Task tool or `@agent-name`
- **Built-in subagents**: `general`, `explore` (read-only codebase search)

### Workflows (slash commands)

Place `.md` files in `.kilo/commands/`. Invoke as `/filename` (without `.md`).

Optional frontmatter: `description`, `agent`, `model`, `subtask`.

## MODEL ROUTING

Pin models per agent in `kilo.jsonc` or agent frontmatter (`provider/model` format):

- **Fast iteration** → lighter models on `code` agent
- **Deep planning** → stronger model on `plan` agent
- **Review / security** → dedicated subagent with read-only permissions

The model picker remembers your last choice per agent across sessions.

## MEMORY & CONTEXT

- **AGENTS.md** replaces the deprecated memory bank — commit durable conventions here
- Per-directory `AGENTS.md` for monorepo scoping (lazy-loaded on file read)
- `AGENTS.md` is write-protected — Kilo asks before modifying it

## GOLDEN RULES (KILO EDITION)

- 📄 KEEP `AGENTS.md` UNDER ~300 LINES — split detail into `.kilo/rules/`
- 🚀 START COMPLEX TASKS IN **plan** AGENT before multi-file implementation
- ▶️ LIST REAL COMMANDS (`npm test`, `lint`, `build`) so Kilo can self-verify
- 🔒 SECRETS IN `$ENV_VAR` ONLY — never commit API keys in `kilo.jsonc`
- 🔗 COMMIT `AGENTS.md`, `kilo.jsonc`, and `.kilo/` — team infrastructure
- 🔍 RESEARCH → **ask** or `@explore`; IMPLEMENT → **code**; REVIEW → custom reviewer subagent
- ⚖️ TRUTH FIRST — pick the right model for the task, demand accuracy

## QUICK START

1. Copy the structure to your project root.
2. Write standards and tech stack into `AGENTS.md`.
3. Add rules in `.kilo/rules/` and reference them in `kilo.jsonc` → `instructions`.
4. For new features: switch to **plan** agent, then **code** for implementation.
5. Add workflows in `.kilo/commands/` and skills in `.kilo/skills/`.
6. Run `kilo agent list` to confirm custom agents load.

## MIGRATION FROM OLD FINAL BOSS TEMPLATE

| Old | Kilo Code native |
|-----|------------------|
| `KILO.md` | Merge into `AGENTS.md` |
| `kilo code/rules/` | `.kilo/rules/` + `kilo.jsonc` `instructions` |
| `skills/` (root) | `.kilo/skills/` |
| `agents/` (root) | `.kilo/agents/` |
| `workflows/*.js` | `.kilo/commands/*.md` |
| `agent-memory/` | `AGENTS.md` |
| Architect mode | Built-in **plan** agent |
| `.kilocode/rules/` (legacy) | `.kilo/rules/` (still backward-compatible) |

## SAMPLE AGENTS.md

```markdown
# Project AGENTS.md

You are an expert software engineer working in this project.

## Core Principles
- Use the **plan** agent for new features or refactors touching > 3 files
- Follow rules in `.kilo/rules/`
- Prefer fast models for iteration, stronger models for architecture
- Write self-documenting code
- Run tests before committing

## Tech Stack
- ...

## Commands
- Test: `npm test`
- Lint: `npm run lint`
- Build: `npm run build`
```

## SAMPLE RULE (.kilo/rules/coding-standards.md)

```markdown
# Coding Standards

- Use TypeScript strict mode
- Prefer functional patterns where possible
- All public functions must have JSDoc
- Error handling: never swallow errors
```

## SAMPLE WORKFLOW (.kilo/commands/release-train.md)

```markdown
---
description: Release train — changelog, version bump, tag
agent: code
---

# Release Train

1. Run tests with `npm test`
2. Gather merged PRs since last tag (`git log`)
3. Update CHANGELOG.md and package version
4. Create annotated tag and push
5. Ask user to confirm before publishing
```

Invoke with `/release-train`.

---

*Adapted from the Claude Code Final Boss template. Remapped to Kilo Code's native paths: `AGENTS.md`, `kilo.jsonc`, `.kilo/rules/`, `.kilo/skills/`, `.kilo/agents/`, `.kilo/commands/`. Based on [Kilo Code docs](https://kilo.ai/docs/customize) and the [Kilo-Org/kilocode](https://github.com/Kilo-Org/kilocode) reference repo.*
