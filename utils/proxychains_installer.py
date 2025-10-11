import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def install():
    """
    Clones, builds, and installs ProxyChains-NG from source.
    """
    print("\n--- Installing 'ProxyChains-NG' from source ---")

    # The executable is often named 'proxychains4'
    if shutil.which('proxychains4'):
        print("'ProxyChains' appears to be already installed. Skipping.")
        return

    if not all(shutil.which(cmd) for cmd in ['git', 'gcc', 'make']):
        print("ERROR: Build tools not found. Cannot build 'ProxyChains'.")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Cloning ProxyChains-NG repository...")
        try:
            repo_url = "https://github.com/rofl0r/proxychains-ng.git"
            proxychains_path = Path(tmpdir) / "proxychains-ng"
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(proxychains_path)], check=True, capture_output=True)
            
            print("Configuring the build...")
            subprocess.run(["./configure"], cwd=str(proxychains_path), check=True, capture_output=True)

            print("Compiling with 'make'...")
            subprocess.run(["make"], cwd=str(proxychains_path), check=True, capture_output=True)

            print("Installing to system directories with 'sudo make install'...")
            subprocess.run(["sudo", "make", "install"], cwd=str(proxychains_path), check=True, capture_output=True)
            
            # Create a default config file if one doesn't exist
            config_path = Path("/etc/proxychains.conf")
            if not config_path.exists():
                print("Creating default configuration file...")
                sample_config_path = proxychains_path / "src" / "proxychains.conf"
                subprocess.run(["sudo", "cp", str(sample_config_path), str(config_path)], check=True)

            print("'ProxyChains-NG' installed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"\nERROR: A command failed during 'ProxyChains' installation: {e}")
            print(f"Stderr: {e.stderr.decode()}")
        except Exception as e:
            print(f"\nAn unexpected error occurred during 'ProxyChains' installation: {e}")

if __name__ == "__main__":
    install()