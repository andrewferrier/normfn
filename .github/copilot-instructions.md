# Copilot Instructions for normfn

## Project Overview

`normfn` is a command-line utility written in Python that normalizes filenames and directories by prefixing them with ISO-8601 formatted dates (YYYY-MM-DD). The tool:

- Detects existing dates in filenames using intelligent heuristics and reformats them to ISO-8601
- Automatically adds dates to files lacking them (using ctime, mtime, or current time)
- Makes filenames naturally sortable
- Supports both Linux and macOS with undo capability via shell scripts
- Is based on Mark Hurst's "Bit Literacy" naming strategy

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
- **UV**: Package manager for dependency management (replaces pip/poetry)

### Code Style

- Follow existing patterns in the codebase
- Maintain consistency with test file patterns in `tests/`

## Build and Test

### Setup Development Environment

1. **Install UV package manager** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

**Development dependencies installed (see `[dependency-groups]` in `pyproject.toml`):**
- `freezegun>=1.5.5` - for time mocking in tests
- `pexpect>=4.9.0` - for subprocess testing
- `pypdf>=3.0.0` - for PDF metadata tests

### Running Tests

**Quick test run** (recommended for development):
```bash
make unittest
# OR with UV directly
uv run -- python -m unittest discover -s tests -p "*.py"
```

**Verbose test output**:
```bash
make unittest_verbose
```

**Test Structure**:
- `tests/BaseTestClasses.py` - Base test classes; `invokeDirectly` uses `from normfn.core import main`; subprocess tests use `python -m normfn`
- `tests/Direct/` - Direct API tests (calling `normfn.core.main()` directly)
- `tests/Subprocess/` - Subprocess/CLI tests (testing command-line interface via `python -m normfn`)

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

The project has several GitHub Actions workflows in `.github/workflows/`:

1. **unittest.yml** - Runs unit tests on:
   - Python 3.12, 3.13, 3.14
   - Ubuntu latest
   - Uses UV package manager
   - Command: `uv run -- python -m unittest discover -s tests -p "*.py"`

2. **codeql.yml** - Code security and quality analysis (GitHub CodeQL)

3. **actionlint.yml** - Validates GitHub Actions workflow files

4. **check-conventional-commit.yml** - Enforces conventional commit message format

5. **release-please.yml** - Automated release management; on release:
   - Builds and uploads `.deb` (Ubuntu runner)
   - Builds and uploads `.pkg.tar.zst` Arch package (`archlinux:latest` container, via `makepkg`)

6. **update-readme.yml** - Auto-updates README.md from code output
   - Looks for markers: `[START AUTO UPDATE]` and `[END AUTO UPDATE]`
   - Updates help text in README automatically

## Project Structure

```
normfn/
├── src/normfn/               # Main package
│   ├── __init__.py           # Re-exports main()
│   ├── __main__.py           # Entry point: logger setup + main()
│   ├── args.py               # Args dataclass + parse_arguments()
│   ├── core.py               # main(), walk_tree(), process_filename()
│   ├── dates.py              # YearRegexes, create_regex(), datetime_prefix()
│   ├── exceptions.py         # FatalError, QuitError
│   └── files.py              # File ops, exclude patterns, undo log, prompts
├── tests/                    # Test suite
│   ├── BaseTestClasses.py    # Base test classes
│   ├── Direct/               # Direct API tests
│   └── Subprocess/           # CLI/subprocess tests
├── .github/
│   └── workflows/            # CI/CD configuration files
├── debian/                   # Debian packaging configuration
├── brew/                     # Homebrew formula template
├── osx/                      # macOS Finder service integration
├── PKGBUILD                  # Arch Linux package build file (committed)
├── Makefile                  # Build, install, package targets
├── pyproject.toml            # Python project metadata and tool config
├── uv.lock                   # Locked dependencies (UV package manager)
├── README.md                 # Main documentation
├── HACKING.md                # Brief development notes
└── CHANGELOG.md              # Version history
```

## Development Workflow

1. **Make changes** to files in `src/normfn/`
2. **Write/update tests** in appropriate test directory (Direct or Subprocess)
3. **Run tests** to verify changes: `make unittest`
4. **Check code style** (if needed): `uv run ruff check .`
5. **Verify types** (if needed): `uv run basedpyright src/normfn`
6. **Use conventional commit format** when committing
7. **CI will automatically**:
   - Run tests on multiple Python versions
   - Check conventional commit format
   - Run CodeQL security analysis
   - Validate GitHub Actions workflows

## Important Notes

### Testing Philosophy

- Implement and update unit tests where appropriate
- Tests are organized into Direct (API) and Subprocess (CLI) categories
- Use `freezegun` for time-based testing
- Use `pexpect` for interactive subprocess testing

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

### Adding a New Feature

1. Identify which module in `src/normfn/` the change belongs to
2. Write tests first (TDD approach recommended)
3. Implement feature with full type annotations
4. Run tests: `make unittest`
5. Update README if user-facing changes
6. Use conventional commit (e.g., `feat: add new option for...`)

### Fixing a Bug

1. Write a failing test that demonstrates the bug
2. Fix the bug in the appropriate `src/normfn/` module
3. Verify test passes: `make unittest`
4. Use conventional commit (e.g., `fix: correct date parsing for...`)

### Updating Dependencies

1. Edit `pyproject.toml` `[dependency-groups]` section
2. Run `uv sync` to update `uv.lock`
3. Test with updated dependencies
4. Commit both `pyproject.toml` and `uv.lock`

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

## Troubleshooting

### Tests Failing

- Ensure you're using Python 3.12 or higher
- Make sure dependencies are installed: `uv sync`
- **Common error**: `ModuleNotFoundError: No module named 'freezegun'` — run `uv sync` first
- Check if tests are environment-specific (time zones, filesystem behavior)

### Import Errors

- The package lives in `src/normfn/`; ensure the package is installed (`uv sync` sets this up via editable install)
- Do not run tests with bare `python`; use `uv run python` so the venv is active

### CI Failures

- **Check conventional commit format** — This is strictly enforced
- **CodeQL alerts** — Review security findings carefully
- **Test failures on specific Python versions** — May need version-specific handling
