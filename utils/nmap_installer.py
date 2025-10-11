import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def install():
    """
    Clones, configures, builds, and installs Nmap from source.
    """
    print("\n--- Installing 'Nmap' from source ---")

    # 1. Check if nmap is already installed
    if shutil.which('nmap'):
        print("'nmap' is already installed. Skipping.")
        return

    # 2. Check for dependencies
    if not all(shutil.which(cmd) for cmd in ['git', 'gcc', 'make']):
        print("ERROR: Build tools ('git', 'gcc', 'make') not found. Cannot build 'nmap'.")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Cloning Nmap repository...")
        try:
            repo_url = "https://github.com/nmap/nmap.git"
            nmap_path = Path(tmpdir) / "nmap"
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(nmap_path)], check=True, capture_output=True)
            
            # 3. Run the build process inside the cloned directory
            print("Configuring the build...")
            # We add --with-libssh2 to ensure it builds with SSH support for NSE
            subprocess.run(["./configure", "--with-libssh2"], cwd=str(nmap_path), check=True, capture_output=True)

            print("Compiling with 'make'...")
            make_flags = [f"-j{os.cpu_count()}"]
            subprocess.run(["make", *make_flags], cwd=str(nmap_path), check=True, capture_output=True)

            print("Installing to system directories with 'sudo make install'...")
            # Nmap is a core tool, so a system-wide install is appropriate.
            subprocess.run(["sudo", "make", "install"], cwd=str(nmap_path), check=True, capture_output=True)

            print("'Nmap' installed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"\nERROR: A command failed during 'nmap' installation: {e}")
            print(f"Stderr: {e.stderr.decode()}")
            print("HINT: Ensure build dependencies like 'libpcap-dev' and 'libssh2-1-dev' are installed.")
        except Exception as e:
            print(f"\nAn unexpected error occurred during 'nmap' installation: {e}")

if __name__ == "__main__":
    install()