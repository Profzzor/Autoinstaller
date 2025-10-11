import subprocess
import shutil

def install():
    """
    Installs Visual Studio Code by adding the official Microsoft APT repository.
    This is the recommended method for Debian/Ubuntu-based systems.
    """
    print("\n--- Installing Visual Studio Code ---")

    # 1. Check if 'code' is already installed
    if shutil.which('code'):
        print("'code' is already installed. Skipping.")
        return

    print("Setting up the official Microsoft APT repository for VS Code...")
    try:
        # 2. Download and add Microsoft's GPG key
        print("Adding Microsoft GPG key...")
        keyring_path = "/etc/apt/keyrings/packages.microsoft.gpg"
        # Download key to a temporary location
        curl_cmd = ["curl", "-sSL", "https://packages.microsoft.com/keys/microsoft.asc"]
        # De-armor and save to final location
        gpg_cmd = ["sudo", "gpg", "--dearmor", "-o", keyring_path]
        
        # Pipe curl output to gpg command
        p1 = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(gpg_cmd, stdin=p1.stdout)
        p1.stdout.close() # Allow p1 to receive a SIGPIPE if p2 exits.
        p2.communicate()
        if p2.returncode != 0:
            raise subprocess.CalledProcessError(p2.returncode, gpg_cmd)

        # 3. Add the VS Code repository source list
        print("Adding VS Code to APT sources...")
        repo_string = f"deb [arch=amd64 signed-by={keyring_path}] https://packages.microsoft.com/repos/code stable main"
        add_repo_cmd = ["sudo", "sh", "-c", f'echo "{repo_string}" > /etc/apt/sources.list.d/vscode.list']
        subprocess.run(add_repo_cmd, check=True)

        # 4. Update package list and install 'code'
        print("Updating package list...")
        subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True)
        
        print("Installing 'code' package...")
        subprocess.run(["sudo", "apt", "install", "-y", "code"], check=True)

        print("Visual Studio Code installed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"\nERROR: A command failed during VS Code installation: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred during VS Code installation: {e}")

if __name__ == "__main__":
    install()