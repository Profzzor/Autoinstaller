import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def install():
    """
    Clones, builds John the Ripper, and moves its run directory to /opt/john.
    The PATH will be handled by the shell configurator scripts.
    """
    print("\n--- Installing 'John the Ripper' from source ---")

    install_dir = Path("/opt/john")
    if install_dir.exists():
        print("'John the Ripper' appears to be already installed. Skipping.")
        return

    if not all(shutil.which(cmd) for cmd in ['git', 'gcc', 'make']):
        print("ERROR: Build tools not found. Cannot build 'john'.")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Cloning John the Ripper repository...")
        try:
            repo_url = "https://github.com/openwall/john.git"
            john_path = Path(tmpdir) / "john"
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(john_path)], check=True, capture_output=True)
            
            src_path = john_path / "src"
            print("Configuring and compiling 'john'...")
            subprocess.run(["./configure"], cwd=str(src_path), check=True, capture_output=True)
            make_flags = ["-s", f"-j{os.cpu_count()}"]
            subprocess.run(["make", *make_flags], cwd=str(src_path), check=True, capture_output=True)
            
            run_dir = john_path / "run"

            # Move the entire 'run' directory to /opt/john
            print(f"Moving compiled application to {install_dir} using sudo...")
            subprocess.run(["sudo", "mv", str(run_dir), str(install_dir)], check=True)

            print("'John the Ripper' installed successfully to /opt/john.")

        except subprocess.CalledProcessError as e:
            print(f"\nERROR: A command failed during 'john' installation: {e}")
            print(f"Stderr: {e.stderr.decode()}")
        except Exception as e:
            print(f"\nAn unexpected error occurred during 'john' installation: {e}")

if __name__ == "__main__":
    install()