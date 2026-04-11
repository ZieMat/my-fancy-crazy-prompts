# AGENTS.md

## Project Overview

**my-fancy-crazy-prompts** is a personal repository for managing AI coding agent prompts, skills, configurations, and experimental personas. It serves as a centralized hub for custom skills, agent platform configs, MCP servers, and personalized agent behavior rules.

## Directory Structure

```
my-fancy-crazy-prompts/
├── .agents/skills/          # Installed agent skills
├── skills/                  # Custom workspace skills
├── config_files/            # Agent platform configurations
├── mcp/servers/             # MCP server definitions
├── experimental/            # Experimental prompt personas
├── personalize/             # Agent behavior customization
└── .qwen/                   # Qwen Code configuration
```

*Note: This repository grows dynamically. Explore subdirectories for specific skills and configurations.*

## Key Guidelines

### Adding Skills

1. Create directory under `skills/<skill-name>/`
2. Write `SKILL.md` with YAML frontmatter (`name`, `description`) and instructions
3. Add `evals/evals.json` for test prompts (if applicable)

### Modifying Agent Behavior

- **Qwen Code**: Edit `.qwen/settings.json`
- **Kilo Code**: Edit `config_files/kilo.jsonc`
- **Personalization**: Edit `personalize/personalize.md`

### Adding MCP Servers

1. Create a JSONC file in `mcp/servers/`
2. Follow the MCP server schema for your platform

## Code Style & Security

- Use standard Markdown for documentation
- Config files use JSONC (JSON with comments)
- Skill manifests use YAML frontmatter in SKILL.md
- **Never commit secrets** — `.env` files stay local only
- Use project-relative paths

## Security Considerations

- Some skills (e.g., network scanning) require explicit user authorization
- `.env.example` files must contain only placeholders
- Respect platform permission settings

## Testing & Quality

- Skills may include evals in `evals/evals.json`
- Verify SKILL.md frontmatter is valid YAML
- Validate JSONC syntax when adding MCP servers
- Test new skills against their evals before merging

## Additional Notes

- **Language**: Responses must be in English only, unless explicitly requested otherwise
- **Verbosity & Commands**: See `personalize/personalize.md` for verbosity levels and slash commands
- **Experimental Content**: Review `experimental/` folder carefully before adopting
- **Skill Portability**: Keep paths relative; skills can be copied between agent platforms
