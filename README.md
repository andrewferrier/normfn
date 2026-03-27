# normfn

`normfn` is a command-line utility that 'normalizes' (renames) files and
directories to use a leading [ISO-8601](https://xkcd.com/1179/) date prefix
(`YYYY-MM-DD-rest-of-name.ext`), inspired by Mark Hurst's file naming strategy
from [Bit Literacy](https://bitliteracy.com/). Files sort naturally and
consistently in any file manager or shell listing.

It detects and reformats dates already present in filenames, or adds one from
the file's timestamps if none is found.

## Features

- **Intelligent date detection**: Recognises a wide range of date formats
  already embedded in filenames (e.g. `2024_03_15`, `15-03-2024`, `March 15
  2024`) and reformats them to ISO-8601.

- **Timestamp fallback**: When no date is found in the filename, normfn falls
  back to the file's filesystem timestamps (ctime and mtime) or the current
  time. By default (`--earliest`), it uses the oldest; `--latest` uses the
  newest; `--now` always uses the current time. Note: on Linux and macOS, ctime
  is *not* file creation time.

- **PDF metadata**: For PDF files, normfn reads the embedded creation date from
  the file's metadata (if available and the optional `pypdf` library is
  installed), preferring it over filesystem timestamps.

- **Time-based naming**: Use `--add-time` to include the time of day (not just
  the date) in the prefix, producing filenames like
  `2026-03-27T09-15-00-report.pdf`.

- **Recursive processing**: Use `-r`/`--recursive` to rename files throughout an
  entire directory tree.

- **Undo log**: Every rename is recorded as a shell command in
  `~/.local/state/normfn-undo.log.sh` so it can be reversed. (See the comments
  at the top of that file for instructions on how to undo changes.)

- **Default exclusions**: By default, normfn skips hidden files, lock files,
  files inside version-control directories, and other misc files. Use `--all` to
  override this.

## Examples

Add a date prefix to a file that has none (uses the file's oldest timestamp):

(`-v` is optional, but shows renames):

```sh
$ normfn -v report.pdf
INFO: report.pdf moved to 2026-03-27-report.pdf
```

Reformat a date already in the filename to ISO-8601:

```sh
$ normfn -v "Invoice_2024_03_15_acme.pdf"
INFO: Invoice_2024_03_15_acme.pdf moved to 2024-03-15-Invoice_acme.pdf
```

Preview what would happen without making changes:

```sh
$ normfn --dry-run *.txt
INFO: Not moving notes.txt to 2026-03-27-notes.txt; dry run.
INFO: Not moving todo-25-12-2025.txt to 2025-12-25-todo.txt; dry run.
```

Add a time component to the prefix:

```sh
$ normfn -v --add-time meeting-notes.docx
INFO: meeting-notes.docx moved to 2026-03-27T09-15-00-meeting-notes.docx
```

Replace the entire filename with just the date prefix:

```sh
$ normfn -v --discard-existing-name "Invoice_2024_03_15_acme.pdf"
INFO: Invoice_2024_03_15_acme.pdf moved to 2024-03-15.pdf
```

Rename a directory and all files inside it recursively:

```sh
$ normfn -v -r project/
INFO: project/ moved to 2026-03-27-project/
INFO: 2026-03-27-project/report.pdf moved to 2026-03-27-project/2024-06-01-report.pdf
INFO: 2026-03-27-project/notes.txt moved to 2026-03-27-project/2026-03-27-notes.txt
```

## Installation

`normfn` requires at least Python 3.12.

### Install from GitHub (any platform with Python)

To install the latest development version directly from GitHub:

```sh
pip install git+https://github.com/andrewferrier/normfn
# or
pipx install git+https://github.com/andrewferrier/normfn
# or
uv tool install git+https://github.com/andrewferrier/normfn
```

### Debian / Ubuntu Linux

Download the `.deb` file from the Assets of the [latest
release](https://github.com/andrewferrier/normfn/releases/latest) and install
using any standard `.deb` installation approach, e.g.:

```sh
dpkg -i normfn*.deb
```

### Arch Linux

Download the `.pkg.tar.zst` file from the Assets of the [latest
release](https://github.com/andrewferrier/normfn/releases/latest) and install
with pacman:

```sh
pacman -U normfn-*.pkg.tar.zst
```

## Usage

<!-- [START AUTO UPDATE] -->
<!-- Please keep comment here to allow auto-update -->
```
usage: normfn [-v] [-h] [-V] [--config PATH] [--initialize-config] [-n] [-i]
              [-a] [-f] [-t] [-d] [-r] [--now | --latest | --earliest]
              [filename ...]

Normalizes filenames by prefixing a date to them. See
https://github.com/andrewferrier/normfn for more information.

positional arguments:
  filename              Filenames

options:
  -v, --verbose         Add debugging output. Using this twice makes it doubly
                        verbose.
  -h, --help            Show help information for normfn.
  -V, --version         Show the version of normfn and exit.
  --config PATH         Path to the configuration file. Defaults to
                        /home/runner/.config/normfn/normfn.toml.
  --initialize-config   Create a template configuration file at the path given
                        by --config (default:
                        /home/runner/.config/normfn/normfn.toml) and exit.
                        Fails if the file already exists.
  -n, --dry-run         Don't actually make any changes, just show them.
                        Forces a single level of verbosity (-v).
  -i, --interactive     Ask about each change before it is done.
  -a, --all             Affect all files, including those in default exclude
                        lists.
  -f, --force           Overwrite target files if they already exist (USE WITH
                        CAUTION, consider using --dry-run first).
  -t, --add-time        If a time is not found in the filename, add one.
  -d, --discard-existing-name
                        Discard existing name and just use the date/time
                        prefix.
  -r, --recursive       Recurse into directories specified on the command
                        line. The default is not to do this, and simply look
                        at the name of the directory itself.
  --now                 Use date and time now as the default file prefix for
                        filenames without them.
  --latest, --newest    Use the latest of ctime and mtime to define a file
                        prefix for files without them. Note: ctime is *not*
                        file creation on Linux/OS X; see
                        http://lwn.net/Articles/397442/.
  --earliest, --oldest  Use earliest of ctime and mtime to define a file
                        prefix for files without them. This is the default.

```
<!-- [END AUTO UPDATE] -->

## Logging and Other Information

For safety, by default, `normfn` keeps a log file in
`~/.local/state/normfn-undo.log.sh` of all the actions it takes, in
shell format to make it easier to undo them. See the comment at the head of that
file (once normfn has generated it) for more information. The undo log location
and other persistent preferences are configured via the config file (see below).

For more information on all the options available, run `normfn --help`.

## Configuration

`normfn` reads persistent preferences from a TOML configuration file located at
`${XDG_CONFIG_HOME}/normfn/normfn.toml`.

If `XDG_CONFIG_HOME` is not set, it defaults to `~/.config`, so the effective
default path is `~/.config/normfn/normfn.toml`. If the file does not exist,
`normfn` silently uses its built-in defaults.

### Initialising the config file

To create a starter config file (with all options commented out and annotated),
run:

```sh
normfn --initialize-config
```

All the options are documented as comments in the generated file itself.

Project hosted [on github](https://github.com/andrewferrier/normfn).
