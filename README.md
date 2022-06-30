# normalize-filename

`normalize-filename` is a utility designed to rename files and directories to
follow a normalized pattern including a leading date. This is a modified version
of Mark Hurst's file naming strategy from the book [Bit
Literacy](https://bitliteracy.com/), but based on the international standard,
ISO-8601. It also makes other modifications to filenames, listed below.

`normalize-filename` has an opinionated sense of what a filename should look
like. It prefers `YYYY-MM-DD-rest-of-the-filename.ext`, where `Y`, `M`, and
`D` are the year, month and day that filename corresponds to respectively. At
the moment, you cannot change this pattern, although there is a long-term goal
to make the pattern configurable.

This default pattern is the ISO-8601 pattern, which is
[superior](https://xkcd.com/1179/). In particular, it's useful because it sorts
naturally when listing files, browsing them with a file manager, etc.

In general, run with the default options, `normalize-filename` will try to
locate anything that it thinks looks like a date in the filename, using some
built-in heuristics, and reformat the filename to follow the pattern above. If
it doesn't find a date, it will add one, using one of the dates/times it finds
in the filesystem that correspond to the file. On Linux and OS X (the only
supported platforms right now), there are three: the ctime, the mtime, and the
time *now* - i.e.  the time when you run normalize-filename. Using the
`--earliest` option - the default - will pick whichever of these times is
earliest (oldest).

`normalize-filename` will also:

*   Lowercase filename extensions (I'm not aware of any good reasons for
    uppercase ones, and they look ugly).

## Installation

`normalize-filename` requires at least Python 3.4.

## More Information on How to Use normalize-filename

*   Run `normalize-filename --help`.

## Logging and Other Information

For safety, by default, normalize-filename keeps a log file in
`~/.local/state/normalize-file-undo.log.sh` of all the actions it takes, in
shell format to make it easier to undo them. See the comment at the head of that
file (once normalize-filename has generated it) for more information. You can
configure this with the `--undo-log-file` and `--no-undo-log-file` options.

For more information on all the options available, run `normalize-filename
--help`. You can alter or disable most `normalize-filename` behaviour using
these options.

Project hosted [on github](https://github.com/andrewferrier/normalize-filename).
