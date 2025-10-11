import os
import shutil
import subprocess
import getpass

def install():
    """
    Installs Docker and adds the current user to the 'docker' group.
    """
    print("\n--- Installing Docker ---")
    if shutil.which('docker'):
        print("'docker' is already installed. Skipping package installation.")
    else:
        # The packages are handled by the main script's PACKAGE_MAP.
        # This function is primarily for the post-install step.
        print("Docker will be installed by the system package manager.")

    # Add user to the docker group
    current_user = getpass.getuser()
    try:
        print(f"Adding user '{current_user}' to the 'docker' group...")
        # Using 'gpasswd' is a reliable way to add a user to a group.
        command = ["sudo", "gpasswd", "-a", current_user, "docker"]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        print("User added to 'docker' group successfully.")
        print("\nIMPORTANT: You must LOG OUT and LOG BACK IN for the Docker group changes to take effect.")

    except subprocess.CalledProcessError as e:
        # It's common for this to fail if the user is already in the group.
        if "is already a member of group" in e.stderr:
            print(f"User '{current_user}' is already a member of the 'docker' group.")
        else:
            print(f"\nERROR: Failed to add user to 'docker' group: {e.stderr}")
    except Exception as e:
        print(f"\nAn unexpected error occurred during Docker configuration: {e}")

if __name__ == "__main__":
    install()