import subprocess
import time
import sys
import os

def run_services():
    backend_cmd = ["uv", "run", "uvicorn", "src.server:app", "--reload"]
    frontend_cmd = ["uv", "run", "--with", "streamlit", "--with", "requests", "streamlit", "run", "src/app.py"]

    print("🚀 Starting Financial RAG Agent...")
    
    try:
        print("Starting Backend (localhost:8000)...")
        backend_process = subprocess.Popen(
            backend_cmd,
            cwd=os.getcwd(),
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        time.sleep(2)
        print("Starting Frontend (localhost:8501)...")
        frontend_process = subprocess.Popen(
            frontend_cmd,
            cwd=os.getcwd(),
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        backend_process.wait()
        frontend_process.wait()

    except KeyboardInterrupt:
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        if 'backend_process' in locals(): backend_process.kill()
        if 'frontend_process' in locals(): frontend_process.kill()
        sys.exit(1)

if __name__ == "__main__":
    run_services()
