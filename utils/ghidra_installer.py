# Save this file as ghidra_installer.py
import os
import shutil
import platform
import subprocess
import tempfile
import requests
from pathlib import Path

def install():
    """
    Downloads, unzips, and installs the latest version of Ghidra to /opt/ghidra.
    """
    print("\n--- Installing 'Ghidra' ---")

    # Define installation directory in /opt and symlink in user's home
    install_dir = Path("/opt/ghidra")
    local_bin = "usr" / "local" / "bin"
    symlink_path = local_bin / "ghidra"

    # 1. Check if Ghidra seems to be already installed
    if install_dir.exists() and symlink_path.exists():
        print(f"'Ghidra' appears to be already installed in {install_dir}. Skipping.")
        return

    # 2. Check for dependencies
    if not shutil.which('unzip') or not shutil.which('java'):
        print("ERROR: 'unzip' or 'java' command not found. Cannot install 'Ghidra'.")
        return

    try:
        # 3. Use the GitHub API to find the latest release
        print("Finding the latest Ghidra release from GitHub API...")
        api_url = "https://api.github.com/repos/NationalSecurityAgency/ghidra/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        zip_url = next((asset['browser_download_url'] for asset in data.get('assets', []) if asset.get('name', '').endswith('.zip')), None)
        
        if not zip_url:
            print("ERROR: Could not find a .zip download URL in the latest Ghidra release.")
            return
        print(f"Found download URL: {zip_url}")

        # 4. Download and unzip in a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            zip_file = tmp_path / "ghidra.zip"
            unzip_dir = tmp_path / "ghidra_unzipped"

            print(f"Downloading to {zip_file}...")
            subprocess.run(["curl", "-L", "-o", str(zip_file), zip_url], check=True)

            print(f"Unzipping to {unzip_dir}...")
            subprocess.run(["unzip", "-q", str(zip_file), "-d", str(unzip_dir)], check=True)

            ghidra_source_dir = next(unzip_dir.iterdir(), None)
            if not ghidra_source_dir:
                print("ERROR: Unzipping failed, no contents found.")
                return

            # 5. Move to the final destination using sudo
            print(f"Moving Ghidra to {install_dir} using sudo...")
            # Remove old version if it exists, with sudo
            if install_dir.exists():
                print(f"Removing old version at {install_dir}...")
                subprocess.run(["sudo", "rm", "-rf", str(install_dir)], check=True)
            
            # Move the new version into place, with sudo
            subprocess.run(["sudo", "mv", str(ghidra_source_dir), str(install_dir)], check=True)

        # 6. Create a symbolic link for easy execution (no sudo needed for this part)
        print(f"Creating symbolic link at {symlink_path}")
        local_bin.mkdir(exist_ok=True)
        
        ghidra_executable = install_dir / "ghidraRun"
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink()
        
        symlink_path.symlink_to(ghidra_executable)

        print("'Ghidra' installed successfully.")
        print(f"It is located in {install_dir}.")
        print("Launch it by typing 'ghidra' in your terminal.")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not contact GitHub API to find release. {e}")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: A command failed during 'Ghidra' installation: {e}")
        print("If it was a 'sudo' command, please check your permissions.")
    except Exception as e:
        print(f"\nAn unexpected error occurred during 'Ghidra' installation: {e}")

if __name__ == "__main__":
    install()
