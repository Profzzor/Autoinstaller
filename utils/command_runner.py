import os
import shutil
import subprocess
from pathlib import Path

# ---------------- CONFIG ----------------

TOOLS_DIR = Path("/opt")

CARGO_PATH = os.path.expanduser("~/.cargo/bin")

COMMANDS_TO_RUN = [
    {
        "name": "Rust Toolchain (rustup)",
        "check_command": "cargo",
        "command": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
        "cwd": None
    },
    {
        "name": "SecLists Wordlists",
        "check_path": TOOLS_DIR / "SecLists-master",
        "command": "sudo sh -c 'wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecLists.zip && unzip -q SecLists.zip && rm -f SecLists.zip'",
        "cwd": str(TOOLS_DIR)
    },
    {
        "name": "Responder Install",
        "check_path": TOOLS_DIR / "Responder",
        "command": "sudo sh -c 'git clone --depth 1 https://github.com/lgandx/Responder.git'",
        "cwd": str(TOOLS_DIR)
    },
    {
        "name": "RustHound",
        "check_command": "rusthound",
        "command": "cd /tmp && git clone --depth 1 https://github.com/NH-RED-TEAM/RustHound.git && cd RustHound && make install",
        "cwd": None
    },
    {
        "name": "Wpscan",
        "check_command": "wpscan",
        "command": "sudo sh -c 'gem install wpscan'",
        "cwd": None
    },
    {
        "name": "Metasploit",
        "check_command": "msfvenom",
        "command": "curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall",
        "cwd": None
    },
    {
        "name": "Brave Browser",
        "check_command": "brave",
        "command": "curl -fsS https://dl.brave.com/install.sh | sh",
        "cwd": None
    }
    # You can add more commands here in the future
    # {
    #     "name": "Another Tool",
    #     "check_command": "another-tool",
    #     "command": "sudo apt install -y another-tool",
    #     "cwd": None
    # }
]

# ---------------- HELPERS ----------------

def refresh_cargo_path():
    """Make cargo available immediately in THIS running process."""
    global CARGO_PATH
    os.environ["PATH"] = CARGO_PATH + ":" + os.environ.get("PATH", "")

def get_env():
    """Ensure all subprocesses see updated PATH."""
    env = os.environ.copy()
    env["PATH"] = CARGO_PATH + ":" + env.get("PATH", "")
    return env

def is_installed(tool):
    if tool.get("check_path") and Path(tool["check_path"]).exists():
        return True
    if tool.get("check_command") and shutil.which(tool["check_command"]):
        return True
    return False

# ---------------- MAIN INSTALLER ----------------

def install():
    print("\n--- STARTING INSTALLATION ---")

    TOOLS_DIR.mkdir(exist_ok=True)

    for tool in COMMANDS_TO_RUN:
        name = tool["name"]
        command = tool["command"]
        cwd = tool.get("cwd")

        print(f"\n==> {name}")

        if is_installed(tool):
            print(f"[SKIP] {name} already installed.")
            continue

        try:
            subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                env=get_env()
            )

            print(f"[OK] {name} installed successfully.")

            if name == "Rust Toolchain (rustup)":
                print("[INFO] Refreshing Cargo PATH...")
                refresh_cargo_path()

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed: {name}")
            print(e.stderr)

if __name__ == "__main__":
    install()
