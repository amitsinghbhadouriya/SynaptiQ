# Debugging & Troubleshooting Guide

This guide provides fast, practical solutions to common issues, error messages, and questions encountered while running or developing **SynaptiQ**.

---

## Quick Diagnostic Index

| Issue / Error Message | Quick Summary Solution |
|---|---|
| `pip install` fails or wheels missing | Use Python 3.11 or 3.12 instead of 3.13+. |
| "Another SynaptiQ process is already using ./storage" | Stop the background process or delete stale `storage/synaptiq.lock`. |
| Port 8501 or 8000 is already in use | Kill the existing process or run on a custom port (`--server.port 8502`). |
| "The web UI build is missing" | Run `npm --prefix frontend run build`. |
| "Execution of scripts is disabled on this system" | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`. |
| First run stalls on "Loading embedding model..." | Initial run needs internet once to download the 90 MB Sentence Transformer model. |
| Vector dimension mismatch in ChromaDB | Clear `./storage/chroma/` or change the model name in `.env`. |
| Ragas raises import errors | Reinstall pinned dependencies via `pip install -r requirements.txt`. |

---

## 1. Python Interpreter Incompatibility (Python 3.13+)

### Symptom:
When running `pip install -r requirements.txt`, packages like `torch` or `chromadb` fail to build, or Python throws `ConnectionResetError` or C-extension compilation errors.

### Cause:
Brand new Python versions (such as Python 3.13, 3.14, or 3.15) often do not have pre-compiled binary wheels available on PyPI for heavy machine learning libraries like PyTorch or ChromaDB.

### Solution:
Install Python 3.11 or 3.12 and create a fresh virtual environment:

**Windows (PowerShell)**:
```powershell
# Remove the old venv
Remove-Item -Recurse -Force .venv

# Create a clean venv using Python 3.12
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux**:
```bash
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. "Another SynaptiQ process is already using ./storage"

### Symptom:
Starting Streamlit or FastAPI crashes with:
`StorageInUse: Another SynaptiQ process is already using ./storage. Stop it or configure a separate DB_PATH and CHROMA_PATH.`

### Cause:
SQLite and ChromaDB do not support concurrent multi-process writes. SynaptiQ places a lock file at `./storage/synaptiq.lock` to prevent data corruption. This error occurs if another terminal is already running SynaptiQ, or if a previous instance was terminated abruptly.

### Solution:
1. **Check for running instances**: Look for other open terminal windows running `streamlit run app.py` or `uvicorn` and stop them with `Ctrl + C`.
2. **If no process is running (stale lock file)**: Delete the lock file manually:
   - On Windows: `Remove-Item .\storage\synaptiq.lock`
   - On Mac/Linux: `rm storage/synaptiq.lock`
3. **Running two instances simultaneously**: If you genuinely want to run both Streamlit and FastAPI simultaneously, point the second server to a different storage directory:
   ```bash
   export DB_PATH="./storage/api/synaptiq.db"
   export CHROMA_PATH="./storage/api/chroma"
   uvicorn backend.api:app --port 8000
   ```

---

## 3. Port 8501 or 8000 Already in Use

### Symptom:
`OSError: [Errno 98] Address already in use` or Streamlit automatically jumps to `http://localhost:8502`.

### Solution:
- **To find and stop the process using port 8501 (Windows PowerShell)**:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess | Stop-Process -Force
  ```
- **To find and stop the process using port 8501 (macOS / Linux)**:
  ```bash
  lsof -ti:8501 | xargs kill -9
  ```
- **Alternatively, specify a different port**:
  ```bash
  streamlit run app.py --server.port 8505
  ```

---

## 4. First Run Stalls on "Loading Embedding Model..."

### Symptom:
The terminal or dashboard shows:
`Starting SynaptiQ — loading the embedding model…` for several minutes.

### Cause:
On the very first launch, the `sentence-transformers/all-MiniLM-L6-v2` embedding model (~90 MB) is downloaded from Hugging Face and cached locally in `~/.cache/huggingface/`. On slower internet connections, this download takes 1–3 minutes. Subsequent launches load the model in under 2 seconds.

### Solution:
- Ensure your internet connection is active during the initial startup.
- If you are permanently offline, SynaptiQ will automatically timeout and fall back to the built-in **Hashing Embedding Backend** with zero crashes.

---

## 5. "The Web UI Build is Missing"

### Symptom:
When visiting `http://localhost:8501` or `http://localhost:8000`, the page displays a blank screen or a message saying the web UI build is missing.

### Cause:
The `frontend/dist/` directory has not been compiled or was deleted.

### Solution:
Rebuild the frontend bundle using Node.js:
```bash
cd frontend
npm install
npm run build
```
Verify that `frontend/dist/index.html` exists. Then refresh your browser.

---

## 6. Vector Dimension Mismatch in ChromaDB

### Symptom:
`ValueError: Embedding dimension 768 does not match collection dimension 384.`

### Cause:
You previously indexed documents using a 384-dimensional embedding model (`all-MiniLM-L6-v2`), and then switched `.env` to a 768-dimensional model (`all-mpnet-base-v2`) on the same collection.

### Solution:
Clear the old Chroma collection cache:
```bash
# On Windows PowerShell:
Remove-Item -Recurse -Force .\storage\chroma

# On macOS / Linux:
rm -rf storage/chroma
```
Restart SynaptiQ. The system will cleanly regenerate the vectors with the new dimension size.
