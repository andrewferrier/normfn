# normalize-filename

[![Travis CI Status](https://travis-ci.org/andrewferrier/normalize-filename.svg?branch=master)](https://travis-ci.org/andrewferrier/normalize-filename)

`normalize-filename` is a utility designed to make it easier to get filenames
(in the broadest sense, this also includes directory names) to follow a
modified version of Mark Hurst's file naming strategy (including dates).

`normalize-filename` has an opinionated sense of what a filename should look
like. It prefers `YYYY-MM-DD-rest-of-the-filename.ext`, where `Y`, `M`, and
`D` are the year, month and day that filename corresponds to respectively. At
the moment, this pattern cannot be changed, although there is a long-term goal
to make the pattern configurable.

This is the default pattern because it is the ISO-8601 pattern, which is
[superior for many reasons](https://xkcd.com/1179/). However, in particular, with respect to filenames,
it's useful because it sorts naturally when listing files, browsing them with
a file manager, etc. In this respect, I respectfully disagree with Mark's
standard approach in his book, which is American-centric.

In general, run with the default options, `normalize-filename` will try to
locate anything that it thinks looks like a date in the filename, using some
built-in heuristics, and reformat the filename to follow the pattern above. If
it doesn't find a date, it will add one, using one of the dates/times it finds
in the filesystem that correspond to the file. On Linux/OS X (the only
supported platforms right now), there are three: the ctime, the mtime, and the
time *now* - i.e.  the time at which normalize-filename is run. Using the
`--earliest` option - the default - will pick whichever of these times is
earliest (oldest).

For safety, by default, normalize-filename keeps a log file in
`~/.normalize-file-undo.log.sh` of all the actions it takes, in shell format to
make it easier to undo them. See the comment at the head of that file (once
it's been generated) for more information.

For more information on all the options available, run `normalize-filename
--help`.

Project hosted [on
github](https://github.com/andrewferrier/normalize-filename).

## Requirements

`normalize-filename` requires at least Python 3.4.

## Hacking - Installation on OS X

* `pip3 install -r requirements_hacking.txt`
