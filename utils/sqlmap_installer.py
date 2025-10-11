import os
import shutil
import subprocess
from pathlib import Path

def install():
    """
    Clones sqlmap to /opt/sqlmap and creates a symbolic link.
    """
    print("\n--- Installing 'sqlmap' ---")
    
    install_dir = Path("/opt/sqlmap")
    local_bin = Path.home() / ".local" / "bin"
    symlink_path = local_bin / "sqlmap"
    
    if install_dir.exists() and symlink_path.exists():
        print("'sqlmap' appears to be already installed. Skipping.")
        return

    if not shutil.which('git'):
        print("ERROR: 'git' not found. Cannot install 'sqlmap'.")
        return

    try:
        print(f"Cloning sqlmap repository to {install_dir} using sudo...")
        repo_url = "https://github.com/sqlmapproject/sqlmap.git"
        # We need to clone as root directly into the final directory
        command = ["sudo", "git", "clone", "--depth", "1", repo_url, str(install_dir)]
        subprocess.run(command, check=True)

        # Create a symbolic link to the main script
        sqlmap_executable = install_dir / "sqlmap.py"
        print(f"Creating symbolic link at {symlink_path}")
        local_bin.mkdir(exist_ok=True)
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink()
        symlink_path.symlink_to(sqlmap_executable)
        
        print("'sqlmap' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: A command failed during 'sqlmap' installation: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred during 'sqlmap' installation: {e}")

if __name__ == "__main__":
    install()