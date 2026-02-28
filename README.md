# MVSEP CLI

[English](./README.md) | [中文](./README_zh.md)

A command-line interface for [MVSEP](https://mvsep.com) music separation API.

## Features

- Upload audio files and create separation tasks
- Monitor task status in real-time
- Download separated tracks automatically
- Support for multiple separation algorithms and models (dynamically fetched from API)
- Configurable default settings
- Support for mirror sites (China)
- Retry mechanism for rate limits and server errors
- Debug mode for troubleshooting

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
mvsep config set-token```

Get your API YOUR_API_TOKEN
 token from https://mvsep.com/user-api

**Test token (for testing only, please don't abuse)**:
```
0VZENEq6t0FMsoF6NYRXD021KZHKBg
```

2. Find available algorithms:

```bash
# List all algorithms
mvsep list

# Search for specific algorithm
mvsep list -s karaoke

# Show models for a specific algorithm
mvsep list --models 49

# Or use the algorithms command
mvsep algorithms
mvsep algorithms -i 20
```

3. Run a separation task:

```bash
mvsep run audio.wav -t 49 --add-opt1 5
```

4. Or upload and wait manually:

```bash
mvsep upload audio.wav -t 49 --add-opt1 5 --wait
```

## Configuration

```bash
# Show current config
mvsep config show

# Set API token
mvsep config set-token YOUR_TOKEN

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
| `mvsep list` | List available algorithms (from API) |
| `mvsep list --models <type>` | Show models for a separation type |
| `mvsep list --search <keyword>` | Search algorithms by keyword |
| `mvsep list --popular` | Show popular algorithms |
| `mvsep algorithms` | List all algorithms with detailed options |
| `mvsep algorithms -i <id>` | Show detailed options for specific algorithm |
| `mvsep history` | Show task history |
| `mvsep config` | Manage configuration |

## Options

Common options for `upload` and `run`:

- `-t, --sep-type` - Separation type (use `mvsep list` to see available types)
- `-f, --output-format` - Output format (default: 1 = wav 16bit)
- `--add-opt1` - Model option 1
- `--add-opt2` - Model option 2
- `--add-opt3` - Model option 3
- `-o, --output-dir` - Output directory
- `-i, --interval` - Polling interval in seconds
- `--wait` - Wait for completion after upload
- `--timeout` - Maximum wait time in seconds
- `--demo` - Publish to demo page

## Examples

```bash
# List popular separation types
mvsep list --popular

# Search for karaoke models
mvsep list -s karaoke

# Show models for MVSep Karaoke (type 49)
mvsep list --models 49
mvsep algorithms -i 49

# Show models for Demucs4 HT (type 20)
mvsep list --models 20

# Upload with specific model (type 49, model 5 = BS Roformer by frazer and becruily)
mvsep upload song.wav -t 49 --add-opt1 5 --wait

# Run full workflow with custom output
mvsep run song.wav -t 49 --add-opt1 5 -f 2 -o ./output

# Download previous results
mvsep download 20260227153708-abc123-vocals.wav -o ./output

# Check task status
mvsep status 20260227153708-abc123-vocals.wav

# Show task history
mvsep history
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

## Advanced Usage

### Using Remote URLs

You can process audio from remote URLs (requires API support):

```python
from mvsep_cli.api import MVSEP_API

api = MVSEP_API("YOUR_TOKEN")
result = api.create_task(
    remote_url="https://example.com/audio.wav",
    sep_type=49,
    add_opt1="5"
)
```

### Debug Mode

Enable debug logging for troubleshooting:

```python
api = MVSEP_API("YOUR_TOKEN", debug=True)
```

### Custom Retry Settings

Adjust retry behavior for rate limits:

```python
api = MVSEP_API("YOUR_TOKEN", retries=30, retry_interval=20)
```

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

### Q: How to find the right model?

1. Search for your desired algorithm type:
   ```bash
   mvsep list -s demucs
   ```

2. Check available models for that algorithm:
   ```bash
   mvsep list --models 20  # For Demucs4 HT
   ```

3. The model with highest SDR (Signal to Distortion Ratio) is generally better

### Q: How to uninstall?

```bash
pip uninstall mvsep-cli
```
