---
name: python-linter
description: >-
  Run ruff and ty to check Python code quality, then fix the errors they report.
  Use this skill whenever the user asks to lint, type-check, clean up, or fix
  the mess in Python code. Also trigger when the user mentions ruff, ty, code
  style, type errors, technical debt, or wants to tidy up a Python project.
  This skill enforces that every finding from ruff and ty must be addressed —
  never bypassed.
compatibility:
  - uv
  - ruff
  - ty
---

# Ruff & Ty Code Quality

Use this skill to run `ruff` and `ty` on Python projects, interpret their output, and fix the issues they surface. Both tools are authoritative — every finding must be addressed.

## Prerequisites

- Project uses `uv` for dependency management
- `ruff` and `ty` are installed in the environment
- If either is missing, stop and inform the user — do not attempt to install them

## Execution order

1. **Run `ruff`** — catches style violations and obvious bugs first
2. **Run `ty`** — validates type annotations after lint is clean
3. **Fix findings** — address all errors before moving on

## Commands

### Whole project

```bash
# Lint the entire project
uv run ruff check .

# Type-check the entire project
uv run ty check .
```

### Specific file

```bash
# Lint a single file
uv run ruff check <file_path>

# Type-check a single file
uv run ty check <file_path>
```

### Fix and reformat

```bash
# Auto-fix what ruff can, then format
uv run ruff check --fix .
uv run ruff format .

# Manual review after auto-fix
uv run ruff check .
```

## How to fix issues

1. **Run the tool** and capture all findings
2. **Prioritize** — fix errors before warnings, group by file
3. **Apply fixes** — use `edit` to correct each issue in the source file
4. **Re-run** the tool to confirm the fix resolved the issue
5. **Repeat** until the tool reports zero findings

## Rules

- **Never bypass findings.** Do not dismiss, rationalize, or ignore ruff or ty output. The user configures these tools to disable irrelevant rules, so every result that surfaces is intentional.
- **Prefer `--fix` when safe.** Use `ruff check --fix` for auto-fixable issues, then manually address the rest.
- **Fix the code, not the tool.** Do not add `# noqa` comments, disable rules, or weaken type annotations to silence errors. Address the root cause in the source code.
- **One issue at a time.** Fix findings file by file to avoid introducing regressions. Re-run the tool after each file to confirm progress.
- **Report summary.** After all fixes, report how many issues were found and resolved, grouped by tool and severity.

## Example workflow

```bash
# 1. Check current state
uv run ruff check .
uv run ty check .

# 2. Auto-fix what's possible
uv run ruff check --fix .
uv run ruff format .

# 3. Manually fix remaining issues file by file
# (use edit tool to fix each finding)

# 4. Verify clean
uv run ruff check .
uv run ty check .
```
