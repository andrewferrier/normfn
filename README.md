# normalize-filename

`normalize-filename` is a utility designed to make it easier to get filenames
(in the broadest sense, this also includes directory names) to follow a
modified version of Mark Hurst's file naming strategy (including dates). It
also makes other modifications to filenames, listed below.

## Modifications to Filenames to Prefix with Normalized Dates

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

## Other Modifications to Filenames

`normalize-filename` will also:

* Lowercase filename extensions (I'm not aware of any good reasons for
  uppercase ones, and they look ugly).

## Logging and Other Information

For safety, by default, normalize-filename keeps a log file in
`~/.normalize-file-undo.log.sh` of all the actions it takes, in shell format to
make it easier to undo them. See the comment at the head of that file (once
it's been generated) for more information.

For more information on all the options available, run `normalize-filename
--help`. Most `normalize-filename` behavior can be altered or disabled using
these options.

Project hosted [on
github](https://github.com/andrewferrier/normalize-filename).

## Installation Requirements

`normalize-filename` requires at least Python 3.4.

`normalize-filename` requires the `coloredlogs` python module. On OS X, this
can be installed using `pip3 install -r requirements.txt`. For Debian/Ubuntu,
there is support in my sister project
[python-deb](https://github.com/andrewferrier/python-deb) for building the
`coloredlogs` module as a Debian package.
