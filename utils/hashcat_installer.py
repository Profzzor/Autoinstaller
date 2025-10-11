import os
import shutil
import platform
import subprocess
import tempfile
from pathlib import Path

def install():
    """
    Clones, builds Hashcat, moves the entire self-contained application
    to /opt/hashcat, and creates a symlink.
    """
    print("\n--- Installing 'Hashcat' from source ---")

    install_dir = Path("/opt/hashcat")
    if install_dir.exists():
        print("'Hashcat' appears to be already installed. Skipping.")
        return

    if not all(shutil.which(cmd) for cmd in ['git', 'gcc', 'make']):
        print("ERROR: Build tools ('git', 'gcc', 'make') not found. Cannot build 'hashcat'.")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Cloning Hashcat repository...")
        try:
            repo_url = "https://github.com/hashcat/hashcat.git"
            hashcat_path = Path(tmpdir) / "hashcat"
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(hashcat_path)], check=True, capture_output=True)
            
            # 1. Compile the binary inside the directory. Do NOT install.
            print("Compiling with 'make'...")
            subprocess.run(["make"], cwd=str(hashcat_path), check=True, capture_output=True)

            # 2. The 'hashcat_path' now contains the full, self-contained application.
            #    Move the entire directory to /opt/hashcat.
            print(f"Moving compiled application to {install_dir} using sudo...")
            subprocess.run(["sudo", "mv", str(hashcat_path), str(install_dir)], check=True)
            
            print("'Hashcat' and all its modules installed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"\nERROR: A command failed during 'hashcat' installation: {e}")
            print(f"Stderr: {e.stderr.decode()}")
            print("HINT: Ensure build dependencies like 'libgmp-dev' and 'ocl-icd-opencl-dev' are installed.")
        except Exception as e:
            print(f"\nAn unexpected error occurred during 'hashcat' installation: {e}")

if __name__ == "__main__":
    install()