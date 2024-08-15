# normfn

`normfn` is a command-line utility designed to rename files and directories to
follow a normalized pattern including a leading date. This is a modified version
of Mark Hurst's file naming strategy from the book [Bit
Literacy](https://bitliteracy.com/), but based on the international standard,
ISO-8601. It also makes other modifications to filenames, listed below.

`normfn` has an opinionated sense of what a filename should look
like. It prefers `YYYY-MM-DD-rest-of-the-filename.ext`, where `Y`, `M`, and
`D` are the year, month and day that filename corresponds to respectively. At
the moment, you cannot change this pattern, although longer-term it made be made
configurable if there's enough interest.

This default pattern is the ISO-8601 pattern, which is
[superior](https://xkcd.com/1179/). In particular, it's useful because it sorts
naturally when listing files, browsing them with a file manager, etc.

In general, run with the default options, `normfn` will try to locate anything
that it thinks looks like a date in the filename, using some built-in
heuristics, and reformat the filename to follow the pattern above. If it doesn't
find a date, it will add one, using one of the dates/times it finds in the
filesystem that correspond to the file. On Linux and OS X (the supported
platforms), there are three: the ctime, the mtime, and the time *now* --- i.e.
the time when you run `normfn`. Using the `--earliest` option --- the default
--- will pick whichever of these times is earliest (oldest).

## Installation

`normfn` requires at least Python 3.10.

### Debian / Ubuntu Linux

Download the `.deb` file from the Assets of the [latest
release](https://github.com/andrewferrier/normfn/releases/latest) and install
using any standard `.deb` installation approach, e.g. `dpkg -i normfn*.deb`.

### Other Platforms

* Clone this repository locally and change to the directory where you cloned it.

* If you have write-access to the system-wide `/usr/local/bin` directory, just
  run `make install`.

* If you don't, install it in your user directory with `PREFIX=~/.local make
  install` (`~/.local/bin/` needs to be in your `$PATH`).

## Usage

<!-- [START AUTO UPDATE] -->
<!-- Please keep comment here to allow auto-update -->
```
usage: normfn [-v] [-h] [-n] [-i] [-a] [-f] [-t] [-d] [-r]
              [--max-years-ahead MAX_YEARS_AHEAD]
              [--max-years-behind MAX_YEARS_BEHIND]
              [--undo-log-file UNDO_LOG_FILE | --no-undo-log-file]
              [--now | --latest | --earliest]
              [filename ...]

Normalizes filenames by prefixing a date to them. See
https://github.com/andrewferrier/normfn for more information.

positional arguments:
  filename              Filenames

options:
  -v, --verbose         Add debugging output. Using this twice makes it doubly
                        verbose.
  -h, --help            Show help information for normfn.
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
  --max-years-ahead MAX_YEARS_AHEAD
                        Consider years further ahead from now than this not to
                        be valid years. Defaults to 5.
  --max-years-behind MAX_YEARS_BEHIND
                        Consider years further behind from now than this not
                        to be valid years. Defaults to 30.
  --undo-log-file UNDO_LOG_FILE
                        The name of the shell script to log 'undo commands'
                        for normfn; see the instructions in the file to use.
                        Defaults to /home/runner/.local/state/normfn-
                        undo.log.sh
  --no-undo-log-file    Inverse of --undo-log-file; don't store undo commands.
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
file (once normfn has generated it) for more information. You can
configure this with the `--undo-log-file` and `--no-undo-log-file` options.

For more information on all the options available, run `normfn --help`. You can
alter or disable most `normfn` behaviour using these options.

Project hosted [on github](https://github.com/andrewferrier/normfn).
