# normfn Demo

This directory contains files for creating a demonstration/screencast of normfn.

## Files

- **Dockerfile**: Sets up a containerized demo environment with Python 3.12, normfn, and sample files
- **Makefile**: Builds and runs the demo container
- **Script.md**: Suggested script for recording a screencast or demo

## Running the Demo

### Prerequisites

- Podman or Docker

### Usage

Using Podman (default):
```bash
cd demo/
make run
```

Using Docker:
```bash
cd demo/
make run CONTAINER=docker
```

This will build a container image and drop you into an interactive bash shell with:
- normfn installed and in PATH
- Sample files in various directories with different date formats
- A clean environment for demonstrating normfn features

## Demo Files

The demo environment includes:

- `documents/` - Files with various date formats (MM-DD-YYYY, YYYY)
- `photos/` - Image files with and without dates
- `projects/` - Project files without dates
- Root directory files - Various formats including backup files

All files are designed to showcase different normfn features like:
- Detecting and reformatting existing dates
- Adding dates to files without them
- Dry-run mode
- Interactive mode
- Recursive directory processing

## Customization

To refresh the demo with the latest normfn code, run:

```bash
make run CACHE_BUST=$(date +%s)
```

The CACHE_BUST argument forces a fresh git clone of normfn.
