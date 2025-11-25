# Second Brain - AI Agent Development Guide

## Project Overview

Second Brain is a **global, persistent knowledge base** for tracking daily work, projects, tasks, and epics. It's designed for developers who want to track their work, organize their knowledge, and leverage AI agents for productivity.

**Key Features:**
- Work log tracking with automatic timestamping
- Project and task management
- Epic & issue management with dependency tracking (powered by Beads)
- Report generation for performance reviews
- AI agent integration via MCP server
- Sync across machines via private GitHub repository
- 100% offline-capable core features

## Essential Documentation

### Getting Started
- [README.md](README.md) - Project overview, features, installation
- [Quick Start Guide](docs/quickstart.md) - Get started in 5 minutes
- [Installation Guide](docs/installation.md) - Detailed installation for all platforms

### Architecture & Design
- [Architecture](docs/architecture.md) - System design, storage layer, data flow
- [Epics & Dependencies](docs/epics-and-dependencies.md) - Epic/issue management with Beads
- [Task-Issue Integration](docs/task-issue-integration.md) - How tasks and issues work together
- [Implementation Plan](docs/development/implementation-plan.md) - Development roadmap

### User-Facing Documentation
- [CLI Reference](docs/cli-reference.md) - All commands and options
- [MCP Server Setup](docs/mcp-server.md) - Connect to AI agents (Claude Code, Claude Desktop, Gemini)
- [Slash Commands](docs/slash-commands.md) - Claude Code workflows
- [Workflows](docs/workflows.md) - Common usage patterns
- [Examples](examples/README.md) - Slash command examples and usage

### Additional Resources
- [Notes Guide](docs/notes.md) - Note-taking system
- [Documentation Index](docs/index.md) - Full documentation index
- [Sync Guide](docs/sync_local_sb_with_cloud.md) - Syncing data across machines

## Development Setup

### Prerequisites
- Python 3.10 or higher
- uv package manager (recommended)

### Quick Setup

```bash
# Clone repository
git clone https://github.com/seanm/second-brain.git
cd second-brain

# Setup development environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/

# Lint
ruff check src/

# Type check
mypy src/
```

### Development Dependencies

The `[dev]` extra includes:
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `black` - Code formatter (line length: 100)
- `ruff` - Fast Python linter (line length: 100)
- `mypy` - Static type checker

## Project Structure

```
second-brain/
├── src/second_brain/
│   ├── cli.py              # Main CLI implementation (62KB+, comprehensive)
│   ├── mcp_server.py       # MCP server for AI agents (FastMCP-based)
│   ├── config.py           # Configuration management (SECOND_BRAIN_DIR)
│   ├── db/                 # Database models and operations
│   ├── storage/            # File storage (markdown, frontmatter)
│   ├── integrations/       # External integrations (Jira, Beads)
│   ├── crypto/             # Encryption layer (RSA+AES hybrid)
│   ├── tools/              # MCP tools implementation
│   └── utils/              # Utility functions
├── tests/
│   └── test_basic.py       # Basic test suite
├── docs/                   # Comprehensive documentation
├── examples/
│   ├── commands/           # Slash commands for Claude Code (29 files)
│   └── skills/             # Claude Code skills
├── pyproject.toml          # Project configuration, dependencies, tooling
└── README.md               # Main project documentation
```

## Key Technical Details

### Storage Architecture

**Hybrid approach** - Best of both worlds:
- **SQLite database** (`~/.second-brain/data/index.db`) - Fast queries and relationships
- **Markdown files** (`~/.second-brain/data/projects/`, `work_logs/`, etc.) - Human-readable, git-friendly
- **Beads JSONL files** (`~/.second-brain/.beads/`) - Epic/dependency tracking
- **Automatic syncing** - Changes in one format update the other

### Environment Variables

```bash
# Primary configuration
export SECOND_BRAIN_DIR="$HOME/.second-brain"  # Main directory (required)
export SECOND_BRAIN_DATA_DIR="$SECOND_BRAIN_DIR/data"  # Optional override

# For MCP server configuration
# See docs/mcp-server.md for setup
```

### Code Style & Standards

- **Line length:** 100 characters (black, ruff)
- **Target version:** Python 3.10+
- **Type hints:** Required for all functions (mypy enforced)
- **Formatting:** black (enforced)
- **Linting:** ruff (enforced)

### Main Entry Points

- **CLI:** `sb` command → `second_brain.cli:main()`
- **MCP Server:** `second-brain-mcp` → `second_brain.mcp_server:main()`

### Key Dependencies

- **FastMCP** (>=0.2.0) - MCP server framework
- **Click** (>=8.1.0) - CLI framework
- **SQLAlchemy** (>=2.0.0) - Database ORM
- **Rich** (>=13.0.0) - Terminal formatting
- **Beads-MCP** (>=0.1.0) - Dependency tracking
- **Pydantic** (>=2.0.0) - Data validation
- **Jira** (>=3.5.0) - Jira integration (optional)
- **python-frontmatter** (>=1.0.0) - Markdown frontmatter parsing

## Important Implementation Notes

### Global Installation Model

Second Brain is designed to be installed **globally** and work from any directory:

```bash
uv tool install git+https://github.com/seanm/second-brain.git
sb init --global
```

All data lives in `~/.second-brain/` (or `$SECOND_BRAIN_DIR`), not in project directories.

### Beads Integration

Epic and issue management is powered by [Beads](https://github.com/cased/beads):
- Issues stored in `~/.second-brain/.beads/issues.jsonl`
- Dependencies in `~/.second-brain/.beads/dependencies.jsonl`
- Initialize per-project: `sb init --beads --prefix SB`
- Create epic + project together: `sb issue create-with-project`

### Encryption Layer

New encryption system (SB-6):
- Hybrid RSA (4096-bit) + AES-256-GCM encryption
- RSA for key exchange, AES for data
- Keys stored in `~/.second-brain/keys/`
- See `src/second_brain/crypto/` for implementation

### MCP Server vs CLI

Second Brain provides two interfaces:
1. **CLI Tool** (`sb` commands) - Direct terminal usage
2. **MCP Server** - AI agent integration (Claude Code, Claude Desktop, Gemini)

Both interfaces share the same underlying storage and business logic.

### Slash Commands

27+ pre-built workflows in `examples/commands/`:
- `/sb-log` - Add work log entries
- `/sb-task-create` - Create tasks
- `/sb-issue-ready` - Find ready work (no blockers)
- `/sb-epic-project-create` - Create epic + project together
- `/sb-weekly-summary` - Weekly review
- See [examples/README.md](examples/README.md) for full list

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=second_brain --cov-report=html

# Run specific test
pytest tests/test_basic.py

# Run with verbose output
pytest -v
```

## CI/CD

Currently, no automated CI/CD pipeline is configured. Future enhancements could include:
- GitHub Actions for automated testing
- Pre-commit hooks for black/ruff/mypy
- Automated releases to PyPI
- Documentation generation

## Common Development Tasks

### Adding a New CLI Command

1. Add command function in `src/second_brain/cli.py`
2. Use Click decorators (`@click.command()`, `@click.option()`)
3. Follow existing patterns (see `log_add`, `task_add`, etc.)
4. Update `docs/cli-reference.md`

### Adding a New MCP Tool

1. Add tool function in `src/second_brain/mcp_server.py`
2. Use FastMCP decorators (`@mcp.tool()`)
3. Follow existing patterns
4. Update `docs/mcp-server.md`

### Adding a New Slash Command

1. Create `.md` file in `examples/commands/`
2. Follow existing format (see `sb-log.md`, `sb-task-create.md`)
3. Test with Claude Code
4. Update `examples/README.md`

### Debugging

```bash
# Enable verbose logging
export SECOND_BRAIN_DEBUG=1

# Check database location
sb init --global  # Shows where data is stored

# Inspect database
sqlite3 ~/.second-brain/data/index.db
```

## Contributing Guidelines

1. **Code Style:** Run `black` and `ruff` before committing
2. **Type Hints:** All functions must have type hints
3. **Tests:** Add tests for new features
4. **Documentation:** Update relevant docs in `docs/`
5. **Commit Messages:** Clear, descriptive commits
6. **Line Length:** 100 characters max

## Troubleshooting

### Common Issues

**"No such table" errors:**
- Database not initialized: `sb init --global`
- Wrong `SECOND_BRAIN_DIR`: Check environment variable

**Beads commands not working:**
- Beads not initialized: `sb init --beads --prefix SB`
- Missing `.beads/` directory

**MCP server not connecting:**
- Check `mcp.json` configuration
- Verify `SECOND_BRAIN_DIR` in MCP config
- See `docs/mcp-server.md` for setup

## License

MIT License - See LICENSE file for details.

## Repository

- **GitHub:** https://github.com/seanm/second-brain
- **Issues:** https://github.com/seanm/second-brain/issues
- **Documentation:** https://github.com/seanm/second-brain#readme
