import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def install():
    """
    Clones, builds, and installs the fzf tool from source.
    """
    print("\n--- Installing 'fzf' from source ---")

    # 1. Check if fzf is already installed
    if shutil.which('fzf'):
        print("'fzf' is already installed. Skipping.")
        return

    # 2. Check for dependencies
    if not all(shutil.which(cmd) for cmd in ['git', 'go']):
        print("ERROR: 'git' or 'go' not found. Cannot build 'fzf'.")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Cloning fzf repository into temporary directory...")
        try:
            repo_url = "https://github.com/junegunn/fzf.git"
            fzf_path = Path(tmpdir) / "fzf"
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(fzf_path)], check=True, capture_output=True)

            print("Building 'fzf' with Go...")
            subprocess.run(["go", "build"], cwd=str(fzf_path), check=True, capture_output=True)

            local_bin = Path.home() / ".local" / "bin"
            local_bin.mkdir(exist_ok=True)

            print(f"Moving compiled 'fzf' binary to {local_bin}")
            shutil.move(str(fzf_path / "fzf"), str(local_bin))

            print("'fzf' binary installed successfully.")
            print("NOTE: For shell integration (key bindings, completion), you may need to run the installer script inside the cloned repo manually.")

        except subprocess.CalledProcessError as e:
            print(f"\nERROR: A command failed during 'fzf' installation: {e}")
            print(f"Stderr: {e.stderr.decode()}")
        except Exception as e:
            print(f"\nAn unexpected error occurred during 'fzf' installation: {e}")

if __name__ == "__main__":
    install()