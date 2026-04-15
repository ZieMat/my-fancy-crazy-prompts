# Git Workflow Rules

## Automated Git Commit Policy

When implementing changes, the agent MUST automatically stage and commit all modifications. This ensures version control integrity and clear attribution of AI-generated changes.

### Commit Requirements

1. **Stage all changes** before committing
2. **Use the following commit command format**:
   ```bash
   git commit --author="<AgentName> 🤖 <agent@localhost>" -m "<commit message>"
   ```

3. **Author attribution** must reflect the actual AI agent used:
   - **Qwen Code**: `--author="Qwen Code 🤖 <noreply@qwen.ai>"`
   - **Kilo Code**: `--author="Kilo Code 🤖 <noreply@kilo.dev>"`
   - **Cursor**: `--author="Cursor AI 🤖 <noreply@cursor.ai>"`
   - **GitHub Copilot**: `--author="GitHub Copilot 🤖 <noreply@github.com>"`
   - **Other agents**: Replace `<AgentName>` with the actual agent name and use appropriate email

4. **Commit message conventions**:
   - Use conventional commits when possible (e.g., `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`)
   - Be concise but descriptive
   - Include context for complex changes

### Example Workflow

```bash
# After making changes
git add .
git commit --author="Qwen Code 🤖 <noreply@qwen.ai>" -m "feat: add new authentication flow"
```

### Important Notes

- Never skip committing changes that were implemented
- Always verify staged changes before committing
- If working in a team, ensure commit messages align with team conventions
- Do not commit `.env` files or sensitive data
- For large changes, consider breaking into multiple logical commits
