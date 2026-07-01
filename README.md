# Code Repository for CIBB 2026 Paper

Repositiory for the paper _A Computational Ethical Framework for Financial Digita Phenotyping for Mental Health_ for the _Computational Methods for Mental Health and Well-Being_ at the 21st _International Conference on Computational Intelligence methods for Bioinformatics and Biostatistics (CIBB 2026)_

## Abstract 
Ethical governance of AI-driven systems is often expressed through high-level princi-
ples and static documentation, creating a gap between regulatory requirements and system-level
verification. This challenge is particularly acute in digital phenotyping, where continuous be-
havioural data raises concerns around consent, privacy, and fairness. In this paper, we propose
a computational ethical framework for AI-driven digital phenotyping system in which ethical
requirements are formalised as deontic temporal logic constraints, alongside a conceptual ethi-
cal agent that oversees the system and ensures that any supervised system satisfies the specified
constraints. Using a case study involving financial data and mental health, we model key ethi-
cal properties and verify them using the Z3 Satisfiability Modulo Theories (SMT) solver. Our
evaluation shows that the framework is logically consistent and that violations of the specified
ethical properties are ruled out within the formal model through counterexample-based verifi-
cation. This presents early research enabling continuous, machine-verifiable ethical checking,
moving beyond retrospective compliance based on static documentation. We discuss limita-
tions, including the need for real-world verification with data, the challenge with subjectivity
and contextual sensitivity, the need for human oversight, and outline how such approaches can
support the development of AI systems with continuous and auditable ethical guarantees

## The Framework

The figure below illustrates the proposed computational ethics framework for financial digital phenotyping, where an ethical oversight agent evaluates system actions against formally specified deontic temporal logic constraints before allowing data collection or use.

<p align="center">
  <img src="images/computational-ethics-schematic.png"
       alt="Computational Ethics Framework for Financial Digital Phenotyping"
       width="900">
</p>


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

### Step 4: Updating Packages (Recommended)

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

If this works fine, skip to step 6.


### Step 5: Initialize a uv Project (If you want to install from from a fresh project)

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

### Step 6: Running the code

```bash
uv run ethics-paper.py
```
---




