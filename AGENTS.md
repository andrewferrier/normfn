# Agent Instructions for normfn

## Project Overview

`normfn` is a command-line utility written in Python that normalizes filenames and directories by prefixing them with ISO-8601 formatted dates (YYYY-MM-DD). See `README.md` for more detail on what it does.

The project is a Python package with a `src/` layout, installable via pip or uv, with comprehensive test coverage.

## Code Conventions

### General Principles

- **Minimal Comments**: Only add comments when they provide useful insight not obvious from the code itself. Let the code explain itself whenever possible.
- **Type Annotations**: Always use full modern type annotations in Python code. This project requires Python 3.12+.
- **Conventional Commits**: Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) format for all commit messages (enforced by CI).

### Code Quality Tools

The project uses:

- **Ruff**: For comprehensive linting (see `pyproject.toml` for complete configuration)
- **BasedPyright**: For static type checking (configured in `pyproject.toml`)
- **uv**: Package manager for dependency management (replaces pip/poetry)

### Code Style

- Follow existing patterns in the codebase
- Maintain consistency with test file patterns in `tests/`

## Build and Test

### Setup Development Environment

1. **Install UV package manager** (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

1. **Install dependencies**:

   ```bash
   uv sync
   ```

Development dependencies installed: see `[dependency-groups]` in `pyproject.toml`

### Running Tests

To run tests:

```bash
make test
```

**Test Structure**:

- `tests/BaseTestClasses.py` - Base test classes
- `tests/Direct/` - Direct API tests (calling `normfn.core.main()` directly)
- `tests/Subprocess/` - Subprocess/CLI tests (testing command-line interface via `python -m normfn`)

#### Testing Philosophy

- Implement and update unit tests where appropriate
- Tests are organized into Direct (API) and Subprocess (CLI) categories
- Use `freezegun` for time-based testing
- Use `pexpect` for interactive subprocess testing

### Linting and Type Checking

**Ruff linting**:

```bash
uv run ruff check .
```

**Type checking with BasedPyright**:

```bash
uv run basedpyright src/normfn
```

### Building Packages

The project supports multiple distribution formats:

**Wheel / sdist** (via hatchling + hatch-vcs, version derived from git tags):

```bash
uv run hatchling build
```

**Debian package**:

```bash
make builddeb
```

**Arch Linux package**:

```bash
make buildarch
```

**Homebrew formula** (macOS):

```bash
make install_osx_brew
```

### Installation

**From PyPI** (once published):

```bash
pip install normfn
# or
uv tool install normfn
```

**From a local clone**:

```bash
pip install .
# or into a specific prefix
pip install --prefix=~/.local .
```

**macOS Finder integration**:

```bash
make install_osx_finder
```

## CI/CD Workflows

The project has several GitHub Actions workflows in `.github/workflows/`.
Whenever you are making systematic changes to e.g. build or test processes,
review these to see if they need changing.

## Development Workflow

1. Make changes to files in `src/normfn/`
1. Write/update tests in appropriate test directory (Direct or Subprocess)
1. Run tests to verify changes
1. Check code style (if needed)
1. Verify types (if needed)
1. See if changes need updates to `.github/copilot-instructions.md`
1. Use conventional commit format when committing

## Important Notes

### README Auto-Update

The README.md contains auto-generated sections between `[START AUTO UPDATE]` and `[END AUTO UPDATE]` markers. These are automatically updated by CI when the help text changes. Do not manually edit content between these markers.

### Platform Support

- Primary platforms: Linux and macOS
- The tool works with filesystem timestamps (ctime, mtime)
- Note: ctime is NOT file creation time on Linux/macOS

### Versioning and Packaging

- Version is derived automatically from git tags via `hatch-vcs` — never set manually in `pyproject.toml`
- Debian packages: built via `pip install --prefix=/usr --root=<stagingdir>` inside Makefile
- Arch Linux: `PKGBUILD` is committed to the repo; `pkgver()` calls `git describe`; builds wheel with `python -m build --no-isolation`; installs with `python -m installer`
- Homebrew: formula template in `brew/normfn_template.rb`; installs via pip into prefix

## Common Tasks

### Running the Tool Locally

```bash
# Via installed entry point (after uv sync)
uv run normfn [options] [files...]

# As a module
uv run python -m normfn [options] [files...]

# With dry-run to see what would happen
uv run normfn --dry-run [files...]

# Verbose output for debugging
uv run normfn -v [files...]
uv run normfn -vv [files...]  # doubly verbose
```
