# Screencast Script: normfn

- Open a window into the normfn repo, `cd demo/` and run `make`
- Open browser to:
    https://github.com/andrewferrier/normfn
    https://bitliteracy.com/

## Introduction

- Introduce normfn: a command-line utility for normalizing filenames with ISO-8601 formatted dates
- Based on Mark Hurst's file naming strategy from "Bit Literacy"
- Automatically detects dates in filenames and reformats them to YYYY-MM-DD
- Adds dates to files that don't have them
- Makes files naturally sortable
- Supports both Linux and macOS with built-in undo capability

## Basic Usage

### Show the demo files

```bash
ls -la documents/
ls -la photos/
ls
```

### Dry run to see what normfn would do

```bash
normfn --dry-run documents/meeting-notes-01-15-2024.txt
normfn --dry-run documents/annual_report_2023.pdf
```

- Explain how normfn detected the dates and reformatted them
- Show that --dry-run doesn't actually change anything

### Actually normalize some files

```bash
normfn documents/meeting-notes-01-15-2024.txt
ls documents/
```

- Show the file was renamed to 2024-01-15 format

```bash
normfn documents/annual_report_2023.pdf
ls documents/
```

### Normalize files without dates

```bash
normfn documents/project-plan.docx
ls documents/
```

- Explain that normfn added a date based on the file's timestamp (--earliest is default)
- Show the undo log: `cat ~/.local/state/normfn-undo.log.sh`

### Normalize a directory

```bash
normfn --dry-run photos/
ls photos/
normfn photos/*
ls photos/
```

- Show how multiple files can be normalized at once

### Interactive mode

```bash
normfn -i invoice-march-2024.pdf
```

- Show how interactive mode asks before each change

### Recursive normalization

```bash
normfn -r projects/
ls projects/
```

- Show how --recursive affects directory contents

## Advanced Features

### Verbose output

```bash
normfn -v backup-2024-01-01.tar.gz
```

- Show debugging output with -v flag
- Mention -vv for even more verbose output

### Undo capability

- Show the undo log file: `cat ~/.local/state/normfn-undo.log.sh`
- Explain how to use it to undo changes
- Source the file and run the mv commands to undo

### Help

```bash
normfn --help
```

- Scroll through options
- Mention key options:
  - --now, --latest, --earliest for date selection
  - --add-time to include time in filename
  - --force to overwrite existing files
  - --discard-existing-name to keep only the date prefix

## Conclusion

- normfn is a practical tool for organizing files with consistent date-based naming
- Useful for anyone who wants naturally sorted, chronologically organized files
- Built-in safety features like dry-run and undo logging
- Invite viewers to try it and contribute feedback
