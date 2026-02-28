# MVSEP CLI

[English](./README.md) | [中文](./README_zh.md)

A command-line interface for [MVSEP](https://mvsep.com) music separation API.

## Features

- Upload audio files and create separation tasks
- Monitor task status in real-time
- Download separated tracks automatically
- Support for multiple separation algorithms and models
- Configurable default settings
- Support for mirror sites (China)

## Installation

### Requirements

- Python 3.8+
- pip

### From PyPI (Recommended)

```bash
pip install mvsep-cli
```

### From Source

```bash
# Clone repository
git clone https://github.com/mvsep/mvsep-cli.git
cd mvsep-cli

# Install
pip install -e .
```

### Verify Installation

```bash
mvsep --help
mvsep config show
```

## Mirror Sites

MVSEP provides mirror sites for better access in different regions:

| Mirror | URL |
|--------|-----|
| main | https://mvsep.com |
| mirror | https://mirror.mvsep.com (China) |

Set your preferred mirror:

```bash
mvsep config set-mirror mirror  # Use China mirror
mvsep config set-mirror main  # Use main site
```

## Quick Start

1. Set your API token:

```bash
mvsep config set-token YOUR_API_TOKEN
```

Get your API token from https://mvsep.com/user-api

**Test token (for testing only, please don't abuse)**:
```
0VZENEq6t0FMsoF6NYRXD021KZHKBg
```

2. Run a separation task:

```bash
mvsep run audio.wav -t 49 --add-opt1 5
```

3. Or upload and wait manually:

```bash
mvsep upload audio.wav -t 49 --add-opt1 5 --wait
```

## Configuration

```bash
# Show current config
mvsep config show

# Set default output directory
mvsep config set-output-dir /path/to/output

# Set default output format (1 = wav 16bit)
mvsep config set-output-format 1

# Set polling interval in seconds
mvsep config set-interval 5
```

## Commands

| Command | Description |
|---------|-------------|
| `mvsep run <file>` | Full workflow: upload + wait + download |
| `mvsep upload <file>` | Upload and create task |
| `mvsep status <hash>` | Check task status |
| `mvsep wait <hash>` | Wait for task completion |
| `mvsep download <hash>` | Download results |
| `mvsep list` | List available separation types |
| `mvsep list --models <type>` | Show models for a separation type |
| `mvsep history` | Show task history |
| `mvsep config` | Manage configuration |

## Options

Common options for `upload` and `run`:

- `-t, --sep-type` - Separation type (use `mvsep list` to see available types)
- `-f, --output-format` - Output format (default: 1 = wav 16bit)
- `--add-opt1` - Model option 1
- `--add-opt2` - Model option 2
- `-o, --output-dir` - Output directory
- `-i, --interval` - Polling interval in seconds
- `--wait` - Wait for completion after upload
- `--timeout` - Maximum wait time in seconds

## Examples

```bash
# List popular separation types
mvsep list --popular

# Show models for BS Roformer (type 40)
mvsep list --models 40

# Upload with specific model
mvsep upload song.wav -t 40 --add-opt1 81 --wait

# Download previous results
mvsep download 20260227153708-abc123-vocals.wav -o ./output
```

## Output Formats

| Value | Format |
|-------|--------|
| 0 | mp3 (320 kbps) |
| 1 | wav (16 bit) |
| 2 | flac (16 bit) |
| 3 | m4a (lossy) |
| 4 | wav (32 bit) |
| 5 | flac (24 bit) |

## License

Apache License 2.0

## FAQ

### Q: How to upgrade?

```bash
pip install --upgrade mvsep-cli
```

### Q: Where is the config file?

- Linux/macOS: `~/.mvsep_cli_config`
- Windows: `%USERPROFILE%\.mvsep_cli_config`

### Q: Where is task history?

- Linux/macOS: `~/.mvsep_tasks.json`
- Windows: `%USERPROFILE%\.mvsep_tasks.json`

### Q: How to uninstall?

```bash
pip uninstall mvsep-cli
```
