# Setup & Installation Guide

This guide walks you through setting up and running **SynaptiQ** on your local computer from scratch.

---

## 1. System Requirements

- **Operating System**: Windows 10/11, macOS (Intel or Apple Silicon), or Linux (Ubuntu, Debian, Fedora, etc.).
- **Python Version**: **Python 3.11 or 3.12** is strongly recommended.
  > **Note**: Very new Python versions (such as 3.13+) may lack pre-built binary wheels for deep learning libraries like `torch` or `chromadb`. Check your version with: `python --version`.
- **Memory (RAM)**: 4 GB minimum (8 GB recommended).
- **Disk Space**: ~500 MB for Python libraries and the default embedding model.
- **Node.js (Optional)**: Node.js 18+ is **only** needed if you intend to modify and rebuild the React frontend. The repository already includes a pre-built frontend in `frontend/dist/`.

---

## 2. Installation on Windows (PowerShell)

Open PowerShell and navigate to the project folder:

```powershell
# 1. Navigate to the project root
cd synaptiq

# 2. Create a virtual environment with Python 3.11 or 3.12
py -3.12 -m venv .venv
# (or if you use Python 3.11: py -3.11 -m venv .venv)

# 3. Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# If PowerShell says "Execution of scripts is disabled on this system", run:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# and try activating again.

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install all dependencies
pip install -r requirements.txt

# 6. (Optional) Create your local environment configuration file
copy .env.example .env

# 7. Start the SynaptiQ application
streamlit run app.py
```

---

## 3. Installation on macOS or Linux

Open your terminal and run:

```bash
# 1. Navigate to the project root
cd synaptiq

# 2. Create a virtual environment with Python 3.11 or 3.12
python3.12 -m venv .venv
# (or: python3.11 -m venv .venv)

# 3. Activate the virtual environment
source .venv/bin/activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install all dependencies
pip install -r requirements.txt

# 6. (Optional) Create your local environment configuration file
cp .env.example .env

# 7. Start the SynaptiQ application
streamlit run app.py
```

---

## 4. Saving Disk Space (CPU-Only PyTorch)

By default, installing PyTorch can download extra GPU drivers (CUDA). If you are running on a standard laptop or CPU-only machine, you can save ~1 GB of download size by installing the CPU wheel first:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

---

## 5. How to Launch SynaptiQ

You can run SynaptiQ using either of two commands:
