# Copilot Instructions for normfn

## Project Overview

`normfn` is a command-line utility written in Python that normalizes filenames and directories by prefixing them with ISO-8601 formatted dates (YYYY-MM-DD). The tool:

- Detects existing dates in filenames using intelligent heuristics and reformats them to ISO-8601
- Automatically adds dates to files lacking them (using ctime, mtime, or current time)
- Makes filenames naturally sortable
- Supports both Linux and macOS with undo capability via shell scripts
- Is based on Mark Hurst's "Bit Literacy" naming strategy

The project is a single-file Python executable (~886 lines) with comprehensive test coverage.

## Code Conventions

### General Principles

- **Minimal Comments**: Only add comments when they provide useful insight not obvious from the code itself. Let the code explain itself whenever possible.
- **Type Annotations**: Always use full modern type annotations in Python code. This project requires Python 3.12+.
- **Conventional Commits**: Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) format for all commit messages (enforced by CI).

### Code Quality Tools

The project uses:
- **Ruff**: For comprehensive linting (configured in `pyproject.toml` with extensive rules)
- **BasedPyright**: For static type checking (configured in `pyproject.toml`)
- **UV**: Package manager for dependency management (replaces pip/poetry)

Ruff configuration in `pyproject.toml`:
- Selects ALL rules, then ignores specific ones (COM, D100, D101, D103, D105, D107, FBT001, G004, ISC003, TRY003)
- These ignores are intentional design decisions for this codebase

### Code Style

- Follow existing patterns in the codebase
- Use the same coding style as the existing code in `normfn`
- Maintain consistency with test file patterns in `tests/`

## Build and Test

### Setup Development Environment

**Option 1: Using UV (recommended, matches CI environment)**

1. **Install UV package manager** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**:
   ```bash
   uv sync --locked --all-extras --dev
   ```

**Option 2: Using pip**

If UV is not available, you can install dependencies with pip:
```bash
pip3 install freezegun pexpect
```

**Development dependencies installed:**
- `freezegun>=1.5.5` - for time mocking in tests
- `pexpect>=4.9.0` - for subprocess testing (usually pre-installed on Linux)

### Running Tests

**Quick test run** (recommended for development):
```bash
make unittest
# OR
python3 -m unittest discover -s tests/
# OR with UV
uv run -- python -m unittest discover -s tests -p "*.py"
```

**Verbose test output**:
```bash
make unittest_verbose
# OR
python3 -m unittest discover -s tests/ -f -v
```

**Test Structure**:
- `tests/BaseTestClasses.py` - Base test classes
- `tests/Direct/` - Direct API tests (calling normfn functions directly)
- `tests/Subprocess/` - Subprocess/CLI tests (testing command-line interface)

### Linting and Type Checking

While not explicitly run in CI workflows, the project is configured for:

**Ruff linting**:
```bash
uv run ruff check .
```

**Type checking with BasedPyright**:
```bash
uv run basedpyright normfn
```

Note: These tools are configured in `pyproject.toml` but need to be installed via UV or pip.

### Building Packages

The project supports multiple distribution formats:

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

**System-wide** (requires write access to `/usr/local`):
```bash
make install
```

**User directory**:
```bash
PREFIX=~/.local make install
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

5. **release-please.yml** - Automated release management and versioning

6. **update-readme.yml** - Auto-updates README.md from code output
   - Looks for markers: `[START AUTO UPDATE]` and `[END AUTO UPDATE]`
   - Updates help text in README automatically

## Project Structure

```
normfn/
├── normfn                    # Main executable Python script (~886 lines)
├── tests/                    # Test suite
│   ├── BaseTestClasses.py   # Base test classes
│   ├── Direct/              # Direct API tests
│   └── Subprocess/          # CLI/subprocess tests
├── .github/
│   └── workflows/           # CI/CD configuration files
├── debian/                  # Debian packaging configuration
├── brew/                    # Homebrew formula template
├── osx/                     # macOS Finder service integration
├── Makefile                 # Build, install, package targets
├── pyproject.toml          # Python project metadata and tool config
├── uv.lock                 # Locked dependencies (UV package manager)
├── README.md               # Main documentation
├── HACKING.md             # Brief development notes
└── CHANGELOG.md           # Version history
```

### Key Files

- **normfn** - The main executable; single Python file with full type annotations
- **pyproject.toml** - Project configuration including:
  - Python version requirement (>=3.12)
  - Ruff linting rules
  - BasedPyright configuration
  - Development dependencies
- **Makefile** - Build automation for packaging, installation, and testing
- **uv.lock** - Locked dependency versions for reproducible builds

## Development Workflow

1. **Make changes** to `normfn` or test files
2. **Write/update tests** in appropriate test directory (Direct or Subprocess)
3. **Run tests** to verify changes: `make unittest`
4. **Check code style** (if needed): `uv run ruff check .`
5. **Verify types** (if needed): `uv run basedpyright normfn`
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

The README.md contains auto-generated sections between `[START AUTO UPDATE]` and `[END AUTO UPDATE]` markers. These are automatically updated by CI when the help text in `normfn` changes. Do not manually edit content between these markers.

### Platform Support

- Primary platforms: Linux and macOS
- The tool works with filesystem timestamps (ctime, mtime)
- Note: ctime is NOT file creation time on Linux/macOS

### Packaging

- Debian packages are built with version from `git describe --tags`
- Homebrew formula uses abbreviated tag version
- Arch Linux PKGBUILD uses tag with hyphens converted to underscores

## Common Tasks

### Adding a New Feature

1. Understand the single-file architecture of `normfn`
2. Write tests first (TDD approach recommended)
3. Implement feature with full type annotations
4. Run tests: `make unittest`
5. Update README if user-facing changes
6. Use conventional commit (e.g., `feat: add new option for...`)

### Fixing a Bug

1. Write a failing test that demonstrates the bug
2. Fix the bug in `normfn`
3. Verify test passes: `make unittest`
4. Use conventional commit (e.g., `fix: correct date parsing for...`)

### Updating Dependencies

1. Edit `pyproject.toml` dependency-groups section
2. Run `uv sync` to update `uv.lock`
3. Test with updated dependencies
4. Commit both `pyproject.toml` and `uv.lock`

### Running the Tool Locally

```bash
# Direct execution
./normfn [options] [files...]

# With dry-run to see what would happen
./normfn --dry-run [files...]

# Verbose output for debugging
./normfn -v [files...]
./normfn -vv [files...]  # doubly verbose
```

## Troubleshooting

### Tests Failing

- Ensure you're using Python 3.12 or higher
- Make sure dependencies are installed: `uv sync --locked --all-extras --dev` OR `pip3 install freezegun pexpect`
- **Common error**: `ModuleNotFoundError: No module named 'freezegun'` - Install dependencies first
- Check if tests are environment-specific (time zones, filesystem behavior)

### Import Errors

- The project uses a single-file structure; `normfn` should be executable
- Tests import from the main `normfn` file

### CI Failures

- **Check conventional commit format** - This is strictly enforced
- **CodeQL alerts** - Review security findings carefully
- **Test failures on specific Python versions** - May need version-specific handling
