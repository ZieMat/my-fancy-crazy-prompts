# Grok Build Final Boss Structure

Production-grade Grok Build layout for lower context cost, modular prompts, guardrails, and multi-agent workflows.

## Folder Tree

```
project-root/
├── README.md
├── AGENTS.md                          # main project instructions (~200 lines max)
├── .grok/
│   ├── config.toml                    # project MCP, permissions, plugins
│   ├── skills/
│   │   ├── security-review/SKILL.md
│   │   ├── deploy/SKILL.md
│   │   └── release/SKILL.md
│   ├── agents/
│   │   ├── code-reviewer.md
│   │   ├── debugger.md
│   │   └── db-validator.md
│   ├── hooks/
│   │   ├── format.json
│   │   └── protect.json
│   ├── rules/
│   │   ├── testing.md
│   │   ├── api-design.md
│   │   └── frontend/react.md
│   ├── personas/                      # optional
│   └── roles/                         # optional
├── docs/
│   ├── architecture.md
│   └── decisions/
├── src/
│   └── <package>/AGENTS.md            # optional per-package scope
└── tools/
    └── scripts/
        ├── format.sh
        └── protect.sh
```

## Context Ladder

1. **Every session** — `AGENTS.md` + `.grok/rules/` (loaded from repo root to CWD)
2. **Subdirectory scope** — nested `AGENTS.md` (loaded when working in that tree)
3. **On invoke** — `.grok/skills/*` via `/skill-name`
4. **Isolated** — `.grok/agents/` subagents (own context; optional `isolation: worktree`)

## Guidance vs Enforcement

| Layer | Type | Mechanism |
|-------|------|-----------|
| `AGENTS.md`, `.grok/rules/` | Asked | Instructions Grok reads and usually follows |
| `.grok/config.toml` `[permission]` | Forced | Deny rules block dangerous tool use |
| `.grok/hooks/*.json` | Forced | Pre/post tool guardrails |

## Golden Rules

- Keep `AGENTS.md` under ~200 lines; split detail into `.grok/rules/`
- List real commands (`test`, `lint`, `build`) so Grok can self-verify
- Secrets only as `$ENV_VAR` references — never commit literals in `config.toml`
- Commit `.grok/` and `AGENTS.md` as team infrastructure
- Research → `explore` subagent; implement → main session; review → `/review` or reviewer agent
- Verify with `grok inspect` after setup

## Migration from Legacy Layouts

| Legacy (Claude-style) | Grok Build native |
|-----------------------|-------------------|
| `GROK.md` / `CLAUDE.md` | `AGENTS.md` |
| `rules/` (repo root) | `.grok/rules/` |
| `skills/` (repo root) | `.grok/skills/` |
| `agents/` (repo root) | `.grok/agents/` |
| `hooks/*.sh` (repo root) | `.grok/hooks/*.json` → `tools/scripts/*.sh` |
| `.grok/settings.json` | `.grok/config.toml` |
| `agent-memory/` | `~/.grok/memory/` + `/remember`, `/flush` |
| `workflows/*.js` | project skills or `/execute-plan` |
| `.worktreeinclude` | subagent `isolation: worktree` |