# Chrome Extension Lookup

Simple Python script that enumerates installed Chrome extensions and looks up their names in the Chrome Web Store.

Windows: supported
macOS:   supported
Linux:   unsupported

## Requirements

- Python 3.14
- uv

## Setup

Clone the repository, then run:

```bash
uv sync
```

This creates a local `.venv` and installs the exact dependency versions recorded in `uv.lock`.

To activate the environment:

```bash
source .venv/bin/activate
```

## Run

```bash
python chromeExtensionLookup.py
```

## Platform support

The current implementation looks for Chrome extensions using the Windows Chrome profile path.

On unsupported platforms such as macOS, the script exits gracefully if that path is not found.
