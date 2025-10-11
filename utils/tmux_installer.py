import os
import shutil
import subprocess
import tempfile
from pathlib import Path

# THE FIX: The main function is now correctly named 'install'.
def install():
    """
    Clones, configures, builds, and installs tmux from source into the user's local directory.
    """
    print("\n--- Installing 'tmux' from source ---")

    # 1. Check if tmux is already installed
    if shutil.which('tmux'):
        print("'tmux' is already installed. Skipping.")
        return

    # 2. Check for dependencies
    if not all(shutil.which(cmd) for cmd in ['git', 'gcc', 'make']):
        print("ERROR: Build tools ('git', 'gcc', 'make') not found. Cannot build 'tmux'.")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Cloning tmux repository into temporary directory...")
        try:
            repo_url = "https://github.com/tmux/tmux.git"
            tmux_path = Path(tmpdir) / "tmux"
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(tmux_path)], check=True, capture_output=True)
            
            local_prefix = Path.home() / ".local"

            # 3. Run the build process
            print("Configuring the build (autogen, configure)...")
            subprocess.run(["sh", "autogen.sh"], cwd=str(tmux_path), check=True, capture_output=True)
            
            configure_cmd = ["./configure", f"--prefix={local_prefix}"]
            subprocess.run(configure_cmd, cwd=str(tmux_path), check=True, capture_output=True)

            print("Compiling with 'make'...")
            subprocess.run(["make"], cwd=str(tmux_path), check=True, capture_output=True)

            print(f"Installing to {local_prefix} with 'make install' (no sudo needed)...")
            subprocess.run(["make", "install"], cwd=str(tmux_path), check=True, capture_output=True)

            print("'tmux' installed successfully.")
            print(f"Binary is located in {local_prefix / 'bin'}.")

        except subprocess.CalledProcessError as e:
            print(f"\nERROR: A command failed during 'tmux' installation: {e}")
            print(f"Stderr: {e.stderr.decode()}")
            print("HINT: Ensure build dependencies like 'libevent-dev' and 'ncurses-dev' are installed.")
        except Exception as e:
            print(f"\nAn unexpected error occurred during 'tmux' installation: {e}")

if __name__ == "__main__":
    install()