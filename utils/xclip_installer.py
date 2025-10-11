import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def install():
    """
    Clones, builds, and installs xclip from source.
    """
    print("\n--- Installing 'xclip' from source ---")

    if shutil.which('xclip'):
        print("'xclip' is already installed. Skipping.")
        return

    if not all(shutil.which(cmd) for cmd in ['git', 'gcc', 'make', 'autoreconf']):
        print("ERROR: Build tools not found. Cannot build 'xclip'.")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Cloning xclip repository...")
        try:
            repo_url = "https://github.com/astrand/xclip.git"
            xclip_path = Path(tmpdir) / "xclip"
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(xclip_path)], check=True, capture_output=True)
            
            # 1. Generate the configure script
            print("Generating configuration script with 'autoreconf'...")
            subprocess.run(["autoreconf", "-i"], cwd=str(xclip_path), check=True, capture_output=True)

            # 2. Configure the build
            print("Configuring the build...")
            subprocess.run(["./configure"], cwd=str(xclip_path), check=True, capture_output=True)

            # 3. Compile the source
            print("Compiling with 'make'...")
            subprocess.run(["make", f"-j{os.cpu_count()}"], cwd=str(xclip_path), check=True, capture_output=True)

            # 4. Install globally
            print("Installing globally with 'sudo make install'...")
            subprocess.run(["sudo", "make", "install"], cwd=str(xclip_path), check=True, capture_output=True)

            print("'xclip' installed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"\nERROR: A command failed during 'xclip' installation: {e}")
            print(f"Stderr: {e.stderr.decode()}")
            print("HINT: Ensure build dependencies like 'libx11-dev' are installed.")
        except Exception as e:
            print(f"\nAn unexpected error occurred during 'xclip' installation: {e}")

if __name__ == "__main__":
    install()