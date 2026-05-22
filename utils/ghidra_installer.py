#!/usr/bin/env python3
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
import requests

def install():
    """
    Downloads, unzips, and installs the latest version of Ghidra to /opt/ghidra.
    """
    print("\n--- Installing 'Ghidra' ---")

    # Installation directories
    install_dir = Path("/opt/ghidra")
    local_bin_path = Path("/usr/local/bin")
    symlink_path = local_bin_path / "ghidra"

    # 1. Check if already installed
    if install_dir.exists() and symlink_path.exists():
        print(f"'Ghidra' appears to be already installed in {install_dir}. Skipping.")
        return

    # 2. Check required commands
    for cmd in ["unzip", "java", "curl"]:
        if not shutil.which(cmd):
            print(f"ERROR: Required command '{cmd}' not found. Please install it first.")
            return

    try:
        # 3. Get latest Ghidra release from GitHub
        print("Finding the latest Ghidra release from GitHub API...")
        api_url = "https://api.github.com/repos/NationalSecurityAgency/ghidra/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        zip_url = next(
            (asset['browser_download_url'] for asset in data.get('assets', [])
             if asset.get('name', '').endswith('.zip')),
            None
        )
        if not zip_url:
            print("ERROR: Could not find a .zip download URL in the latest Ghidra release.")
            return
        print(f"Found download URL: {zip_url}")

        # 4. Download and unzip in temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            zip_file = tmp_path / "ghidra.zip"
            unzip_dir = tmp_path / "ghidra_unzipped"

            print(f"Downloading to {zip_file}...")
            subprocess.run(["curl", "-L", "-o", str(zip_file), zip_url], check=True)

            print(f"Unzipping to {unzip_dir}...")
            unzip_dir.mkdir(exist_ok=True)
            subprocess.run(["unzip", "-q", str(zip_file), "-d", str(unzip_dir)], check=True)

            ghidra_source_dir = next(unzip_dir.iterdir(), None)
            if not ghidra_source_dir:
                print("ERROR: Unzipping failed, no contents found.")
                return

            # 5. Move to /opt/ghidra using sudo
            print(f"Moving Ghidra to {install_dir} using sudo...")
            if install_dir.exists():
                print(f"Removing old version at {install_dir}...")
                subprocess.run(["sudo", "rm", "-rf", str(install_dir)], check=True)
            subprocess.run(["sudo", "mv", str(ghidra_source_dir), str(install_dir)], check=True)

            # 6. Create symbolic link with sudo
            ghidra_executable = install_dir / "ghidraRun"
            subprocess.run(["sudo", "ln", "-sf", str(ghidra_executable), str(symlink_path)], check=True)

        print("\n'Ghidra' installed successfully!")
        print(f"Installation directory: {install_dir}")
        print("Launch Ghidra by typing 'ghidra' in your terminal.")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not contact GitHub API. {e}")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: A command failed during installation: {e}")
        print("If it was a 'sudo' command, please check your permissions.")
    except Exception as e:
        print(f"An unexpected error occurred during installation: {e}")

if __name__ == "__main__":
    install()
