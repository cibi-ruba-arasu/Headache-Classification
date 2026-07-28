import os
import sys
import subprocess

# Define the folder paths
ROOT_DIR = os.getcwd()
BACKEND_DIR = os.path.join(ROOT_DIR, 'backend')
FRONTEND_DIR = os.path.join(ROOT_DIR, 'frontend')

def get_venv_python():
    """Points exactly to the manual venv you created in the backend folder."""
    if sys.platform == "win32":
        return os.path.join(BACKEND_DIR, 'venv', 'Scripts', 'python.exe')
    return os.path.join(BACKEND_DIR, 'venv', 'bin', 'python')

def start_servers():
    # Use the venv python if it exists, otherwise fallback to global python
    python_exe = get_venv_python()
    if not os.path.exists(python_exe):
        print("Warning: venv not found. Falling back to global Python.")
        python_exe = 'python'

    
    print("Backend:")
    backend_process = subprocess.Popen([python_exe, 'main.py'], cwd=BACKEND_DIR)

    
    print("Frontend:")
    npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    frontend_process = subprocess.Popen([npm_cmd, 'run', 'dev'], cwd=FRONTEND_DIR)

    
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nCaught interrupt signal. Shutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped cleanly.")

if __name__ == '__main__':
    start_servers()