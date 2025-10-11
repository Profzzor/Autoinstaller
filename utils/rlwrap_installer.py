import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def install():
    """
    Clones, builds, and installs rlwrap from source.
    """
    print("\n--- Installing 'rlwrap' from source ---")
    if shutil.which('rlwrap'):
        print("'rlwrap' is already installed. Skipping.")
        return
    if not all(shutil.which(cmd) for cmd in ['git', 'gcc', 'make', 'autoconf']):
        print("ERROR: Build tools not found. Cannot build 'rlwrap'.")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Cloning rlwrap repository...")
        try:
            repo_url = "https://github.com/hanslub42/rlwrap.git"
            rlwrap_path = Path(tmpdir) / "rlwrap"
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(rlwrap_path)], check=True, capture_output=True)
            
            print("Configuring the build...")
            subprocess.run(["autoreconf", "--install"], cwd=str(rlwrap_path), check=True, capture_output=True)
            subprocess.run(["./configure"], cwd=str(rlwrap_path), check=True, capture_output=True)

            print("Compiling and installing with 'make'...")
            subprocess.run(["make"], cwd=str(rlwrap_path), check=True, capture_output=True)
            subprocess.run(["sudo", "make", "install"], cwd=str(rlwrap_path), check=True, capture_output=True)

            print("'rlwrap' installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"\nERROR: A command failed during 'rlwrap' installation: {e}")
            print(f"Stderr: {e.stderr.decode()}")
            print("HINT: Ensure build dependencies like 'libreadline-dev' and 'autoconf' are installed.")
        except Exception as e:
            print(f"\nAn unexpected error occurred during 'rlwrap' installation: {e}")

if __name__ == "__main__":
    install()