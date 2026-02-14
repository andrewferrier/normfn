# Screencast Script: normfn

- Open a window into the normfn repo, `cd demo/` and run `make`
- Open browser to:
  <https://github.com/andrewferrier/normfn>
  <https://bitliteracy.com/>

## Introduction

- Introducing you to a way of organizing and managing your files, and a utility I created to help you do that

- Based on Mark Hurst's file naming strategy from "Bit Literacy"

- Automatically detects dates in filenames and reformats them to YYYY-MM-DD

- Adds dates to files that don't have them

- Makes files naturally sortable

- Built-in undo capability

## Demo

- Navigate around
- Show normfn
- Show normfn --dry-run
- Explain how normfn detected the dates and reformatted them
- Normfn file without date
- Show the undo log: `cat ~/.local/state/normfn-undo.log.sh`, demonstrate
- normfn a directory: normfn -r photos/, show times
- normfn --help

## Conclusion

- normfn is a practical tool for organizing files with consistent date-based naming
- Show install mechanism, modern tools like uv
- Invite viewers to try it and contribute feedback
