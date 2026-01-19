# Image Tools

A collection of simple image tools for renaming and converting images.
Designed for personal need, not for a common usage.

## Requirements

Python > 3.10

uv

## Installation

1. Clone this repository or download the code.

2. Use uv tool

```bash
uv tool install .
```

## Tools

### 1. Convert HEIC images to JPG

Convert HEIC files to JPG in a directory.

**Usage:**
```bash
convert-heic-images-to-jpg /path/to/directory -q 90 -m True
```

**Arguments:**
- `path`: The path of the directory.
- `-q, --quality`: Quality of the output JPG (1-100). Default is 90.
- `-m, --multithread`: Multithread the treatment. True by default.

### 2. Rename images by date

Rename files in a directory based on creation date.

**Usage:**
```bash
rename-images-by-date /path/to/directory -f "%Y-%m-%dT%H:%M:%S" -d 0 -m True
```

**Arguments:**
- `path`: The path of the directory.
- `-f, --format`: Datetime format used to rename the files. Default is `%Y-%m-%dT%H:%M:%S`.
- `-d, --delta`: An optional datetime delta (applied in each file) in seconds. Use to fix wrong hours or timezone. Default is 0.
- `-m, --multithread`: Multithread the treatment. True by default.

## Development

### Install dependencies

1. Create and activate a virtual environment with `uv`:

```bash
uv venv
source .venv/bin/activate  # On Linux/Mac
# .\.venv\Scripts\activate  # On Windows
```

2. Install the dependencies:

```bash
uv pip install -e .
```

3. (Optional) Install development dependencies:

```bash
uv pip install --dev
```

### Formatting and Linting

This project uses `black` for code formatting and `flake8` for linting. To ensure your code is compliant:

```bash
# Format code with black
black .

# Lint code with flake8
flake8 .
```

### Running Tests

To run tests, use `pytest`:

```bash
pytest
```

### Configuration

- `.flake8`: Configuration for `flake8` to align with `black` (max line length: 88).
- `pyproject.toml`: Project configuration and dependencies.

## License

This project is licensed under the MIT License.
