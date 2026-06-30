## Code Repository for CIBB 2026 Paper

Repositiory for the paper _A Computational Ethical Framework for Financial Digita Phenotyping for Mental Health_ for the _Computational Methods for Mental Health and Well-Being_ at the 21st _International Conference on Computational Intelligence methods for Bioinformatics and Biostatistics (CIBB 2026)_

## Setup

---

### Step 1: Install Python

Ensure Python 3.10 or newer is installed.

Check:

```bash
python --version
```

or

```bash
python3 --version
```

If Python is not installed:

- Windows: https://www.python.org/downloads/
- macOS:

```bash
brew install python
```

- Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

### Step 2: Install uv

#### macOS

```bash
brew install uv
```

Restart your terminal afterwards.

Verify:

```bash
uv --version
```
uv 0.9.5 

---

#### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```powershell
uv --version
```

---

### Step 3: Create a New Project

```bash
mkdir cibb-2026
cd cibb-2026
```

---

### Updating Packages (Recommended)

```bash
uv sync
```
Ensure the environment is using python 3.12
i.e.
```bash
uv venv --python 3.12
source .venv/bin/activate
uv sync
```


### Initialize a uv Project (If you want to install from from a fresh project)

Instead of manually creating files, you can initialize a project with

```bash
uv init
```

This creates

```
cibb-2026/
│
├── pyproject.toml
├── .python-version
├── README.md
└── src/
```
Run to remove the main.py
```bash
rm main.py
```

Then install Z3:

```bash
uv add z3-solver
```

This automatically updates your `pyproject.toml`.

---

### Project Structure

```text
cibb-2026/
├── .venv/              # Virtual environment
├── .python-version     # Python version used by uv
├── ethics-paper.py     # Main application/script
├── pyproject.toml      # Project metadata and dependencies
├── README.md           # Project documentation
└── uv.lock             # Locked dependency versions
```

---

### Running the code

```bash
uv run ethics-paper.py
```
---



You are now ready to build formal verification systems using the Z3 SMT solver in Python.




