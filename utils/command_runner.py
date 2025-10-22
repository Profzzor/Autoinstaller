import os
import shutil
import subprocess
from pathlib import Path

# --- CONFIGURATION ---
# Add any simple, one-off installation commands to this list.
#
# "name": A friendly name for logging.
# "check_path" OR "check_command": 
#   - Use "check_path" to see if a file/directory exists (e.g., "/opt/SecLists-master").
#   - Use "check_command" to see if a command is in the PATH (e.g., "cargo").
# "command": The full shell command to execute.
# "cwd": (Optional) The directory to run the command in. Defaults to the user's tools directory.

TOOLS_DIR = Path("/opt")

COMMANDS_TO_RUN = [
    {
        "name": "Rust Toolchain (rustup)",
        "check_command": "cargo",
        "command": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
        "cwd": None # This command doesn't need a specific directory
    },
    {
        "name": "SecLists Wordlists",
        "check_path": TOOLS_DIR / "SecLists-master",
        "command": "sudo sh -c 'wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecLists.zip && unzip -q SecLists.zip && rm -f SecLists.zip'",
        "cwd": str(TOOLS_DIR) # Run this inside the /opt directory
    },
    {
        "name": "Responder Install",
        "check_path": TOOLS_DIR / "Responder",
        "command": "sudo sh -c 'git clone --depth 1 https://github.com/lgandx/Responder.git'",
        "cwd": str(TOOLS_DIR) # Run this inside the /opt directory
    },
    {
        "name": "RustHound",
        "check_command": "rusthound",
        "command": "cd /tmp && git clone --depth 1 https://github.com/NH-RED-TEAM/RustHound.git && cd RustHound && make install",
        "cwd": None # This command doesn't need a specific directory
    },
    # You can add more commands here in the future
    # {
    #     "name": "Another Tool",
    #     "check_command": "another-tool",
    #     "command": "sudo apt install -y another-tool",
    #     "cwd": None
    # }
]

def install():
    """
    Runs a series of arbitrary shell commands for simple installations.
    """
    print("\n--- Running Custom Installation Commands ---")

    # Ensure the main tools directory exists
    TOOLS_DIR.mkdir(exist_ok=True)

    for tool in COMMANDS_TO_RUN:
        name = tool["name"]
        command = tool["command"]
        check_path = tool.get("check_path")
        check_command = tool.get("check_command")
        cwd = tool.get("cwd")

        print(f"\nProcessing: {name}")

        # 1. Check if the tool is already installed
        is_installed = False
        if check_path and Path(check_path).expanduser().exists():
            is_installed = True
        elif check_command and shutil.which(check_command):
            is_installed = True

        if is_installed:
            print(f"'{name}' appears to be already installed. Skipping.")
            continue

        # 2. Run the installation command
        print(f"Installing {name}...")
        try:
            # We use shell=True to handle pipes '|' and chains '&&'.
            # This is safe as we are defining the commands ourselves.
            subprocess.run(
                command, 
                shell=True, 
                check=True, 
                capture_output=True, 
                text=True,
                cwd=cwd # Run in the specified directory
            )
            print(f"'{name}' installed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"\nERROR: Failed to install '{name}': {e}")
            print(f"Stderr: {e.stderr}")
        except Exception as e:
            print(f"\nAn unexpected error occurred while installing '{name}': {e}")

if __name__ == "__main__":
    install()
