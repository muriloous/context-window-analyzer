# Context Window Analyzer

## Overview
This project studies the impact of context windows on computational models of language acquisition.

Common tasks are:

- Analysis and processing of non-adjacent dependencies in text.
- Generation of contingency tables for observed dependencies.

## Requirements
- Python >= 3.11

## Setup

### 1. Clone this repository

```bash
git clone git@github.com:muriloous/context-window-analyzer.git
cd context-window-analyzer
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
python3 setup_nltk.py
```

## Usage

* Always run the project from the repository root to ensure correct path resolution.

Folders:

* `docs/` — contains some details about the project and the code.
* `exports/` — output directory for generated files.

### Running the project

#### 1. Activate virtual environment

```bash
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

#### 2. Execute

```bash
python3 cwa [...options]
```

Or run any specific module as needed.

### Main options

- `context_window` (default): build contingency table from context window
- `sentences`: build contingency table from sentences

## License
--

## Contact
For questions or feedback, please contact [m237370@dac.unicamp.br](mailto:m237370@dac.unicamp.br).
