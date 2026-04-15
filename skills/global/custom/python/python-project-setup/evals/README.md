Evals for `python-project-setup`

- Location: `evals/evals.json`
- Coverage: base uv project (no framework), FastAPI variant, Typer CLI variant.
- Each eval includes assertions for git init, tooling deps (ruff/ty/pytest and framework deps), env files, agents/skills + workflows scaffolding, package layout, entrypoint/stub, run/test commands.

How to run/grade (guidance):
- Generate outputs per prompt using the skill.
- For each assertion, verify presence in created files/summary (git init mentioned, deps in pyproject, files created, commands shown).
- Automate grading where possible by inspecting generated project tree and pyproject content.
