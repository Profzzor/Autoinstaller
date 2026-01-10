import subprocess
import sys
import platform
import os
import shutil
import tempfile

# All modules from the 'utils' package.
import utils.bash_configurator, utils.zsh_configurator, utils.alias_manager, utils.ghidra_installer
import utils.vscode_installer, utils.fzf_installer, utils.tmux_installer, utils.john_installer
import utils.hashcat_installer, utils.uv_tools_installer, utils.nmap_installer, utils.rlwrap_installer
import utils.sqlmap_installer, utils.docker_installer, utils.service_manager, utils.proxychains_installer
import utils.command_runner, utils.xclip_installer

# --- SCRIPT CONFIGURATION ---
# Final update with all dependencies
PACKAGE_MAP = {
    "debian": {
        "manager": "apt",
        "packages": [
            "build-essential", "default-jdk", "golang", "curl", "git", "unzip", "gpg", "python3-dev",
            "libevent-dev", "ncurses-dev", "automake", "bison", "pkg-config", "libssl-dev",
            "p7zip-full", "ocl-icd-opencl-dev", "libgmp-dev", "libxxhash-dev", "libpcap-dev",
            "libssh2-1-dev", "libreadline-dev", "autoconf", "libptytty-dev", "docker.io",
            "docker-compose", "default-mysql-server", "sqlite3", "php", "apache2", "gdb",
            "openvpn", "krb5-user", "libkrb5-dev", "wget", "vim", "android-tools-adb", "binutils",
            "libx11-dev", "libxmu-dev", "libxext-dev", "ldap-utils", "ruby", "ruby-dev", "wireshark",
            "tshark", "jq", "faketime", "mingw-w64"
        ],
        "update_cmd": ["apt", "update"]
    },
    "fedora": {
        "manager": "dnf",
        "packages": [
            "@development-tools", "java-latest-openjdk-devel", "golang", "curl", "git", "unzip", "gpg", "python3-devel",
            "libevent-devel", "ncurses-devel", "automake", "bison", "pkgconf-pkg-config", "openssl-devel", "p7zip",
            "ocl-icd-devel", "gmp-devel", "xxhash-devel", "libpcap-devel", "libssh2-devel", "readline-devel", "autoconf",
            "libptytty-devel", "docker", "docker-compose", "mariadb-server", "sqlite", "php", "openvpn",
            "krb5-workstation", "krb5-devel", "wget", "vim", "android-tools", "binutils", "gdb",
            "libX11-devel", "libXmu-devel", "libXext-devel", "openldap-clients", "ruby", "ruby-dev",
            "wireshark-qt", "wireshark-cli", "jq", "faketime", "mingw64-gcc"
        ], "update_cmd": []
    },
    "arch": {
        "manager": "pacman",
        "packages": [
            "base-devel", "jdk-openjdk", "go", "curl", "git", "unzip", "gnupg", "libevent", "ncurses", "automake", "bison",
            "pkg-config", "openssl", "p7zip", "opencl-icd-loader", "gmp", "xxhash", "libpcap", "libssh2", "readline",
            "libptytty", "docker", "docker-compose", "mariadb", "sqlite", "php", "openvpn", "krb5", "wget",
            "libx11", "libxmu", "libxext", "vim", "android-tools", "binutils", "gdb", "openldap",
            "ruby", "ruby", "wireshark-qt", "wireshark-cli", "jq", "mingw-w64-gcc"
        ], "update_cmd": ["pacman", "-Syu", "--noconfirm"]
    },
}

# (All other functions remain unchanged)
def ensure_pip_is_available():
    print("--- Ensuring 'pip' is available ---")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True); print("'pip' is already installed."); return
    except (subprocess.CalledProcessError, FileNotFoundError): pass
    print("Trying to bootstrap pip using 'ensurepip'...")
    if subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"]).returncode == 0:
        print("'ensurepip' succeeded."); return
    print("'ensurepip' failed. Falling back to downloading 'get-pip.py'...")
    getpip_path = "/tmp/get-pip.py"
    try:
        subprocess.run(["curl", "-sS", "https://bootstrap.pypa.io/get-pip.py", "-o", getpip_path], check=True)
        subprocess.run([sys.executable, getpip_path, "--break-system-packages"], check=True)
        print("'pip' installation successful.")
    except Exception as e: print(f"\nFATAL: All methods to install pip have failed. Reason: {e}"); sys.exit(1)
    finally:
        if os.path.exists(getpip_path): os.remove(getpip_path)

def ensure_uv():
    print("\n--- Ensuring 'uv' is installed and up-to-date ---")
    try:
        subprocess.run([sys.executable, "-m", "uv", "--version"], check=True, capture_output=True)
        command = [sys.executable, "-m", "pip", "install", "--upgrade", "uv", "--break-system-packages"]
    except (subprocess.CalledProcessError, FileNotFoundError):
        command = [sys.executable, "-m", "pip", "install", "uv", "--break-system-packages"]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("'uv' is now installed and up-to-date.")
    except Exception as e: print(f"\nFATAL: Failed to install 'uv' using pip. Reason: {e}"); sys.exit(1)

def install_script_dependencies_with_pip():
    print("\n--- Installing script dependencies (requests, distro) with pip ---")
    packages = ["requests", "distro"]
    try:
        command = [sys.executable, "-m", "pip", "install", *packages, "--break-system-packages"]
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("Script dependencies installed successfully.")
    except Exception as e: print(f"\nFATAL: Failed to install script dependencies using pip. Reason: {e}"); sys.exit(1)

def get_system_info():
    if platform.system().lower() == "linux":
        try:
            import distro; return distro.id()
        except ImportError: print("FATAL: 'distro' package not available."); sys.exit(1)
    return platform.system().lower()

def install_system_packages():
    print("\n--- Installing System Packages ---")
    system_id = get_system_info()
    if system_id in ["linuxmint", "ubuntu"]: system_id = "debian"
    if not system_id or system_id not in PACKAGE_MAP:
        print(f"ERROR: System ('{system_id}') not supported."); return False
    config = PACKAGE_MAP[system_id]
    manager = config["manager"]
    is_linux = platform.system().lower() == "linux"
    try:
        if config["update_cmd"]:
            subprocess.run((["sudo"] if is_linux else []) + config["update_cmd"], check=True, capture_output=True, text=True)
        command = (["sudo"] if is_linux else []) + [manager]
        if manager in ["apt", "dnf"]: command.extend(["install", "-y"])
        elif manager == "pacman": command.extend(["-S", "--noconfirm"])
        else: command.append("install")
        command.extend(config["packages"])
        print(f"Running installation: {' '.join(command)}")
        subprocess.run(command, check=True)
        print("\nSystem packages installed successfully!"); return True
    except Exception as e: print(f"\nERROR: Package installation failed. Reason: {e}"); return False

def install_ffuf():
    print("\n--- Installing 'ffuf' from source ---")
    if shutil.which('ffuf'): print("'ffuf' is already installed. Skipping."); return
    if not all(shutil.which(cmd) for cmd in ['git', 'go']): return
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            ffuf_path = os.path.join(tmpdir, "ffuf")
            subprocess.run(["git", "clone", "--depth", "1", "https://github.com/ffuf/ffuf", ffuf_path], check=True, capture_output=True)
            subprocess.run(["go", "build"], cwd=ffuf_path, check=True, capture_output=True)
            local_bin = os.path.expanduser("~/.local/bin")
            os.makedirs(local_bin, exist_ok=True)
            shutil.move(os.path.join(ffuf_path, "ffuf"), local_bin)
            print("'ffuf' installed successfully.")
        except Exception as e: print(f"\nAn error occurred during 'ffuf' installation: {e}")

def configure_shells():
    utils.bash_configurator.configure()
    utils.zsh_configurator.configure()


if __name__ == "__main__":
    ensure_pip_is_available()
    ensure_uv()
    install_script_dependencies_with_pip()
    
    if not install_system_packages():
        sys.exit(1)
        
    # Run all the individual installers
    utils.vscode_installer.install()
    utils.docker_installer.install()
    utils.nmap_installer.install()
    utils.rlwrap_installer.install()
    utils.sqlmap_installer.install()
    utils.proxychains_installer.install()
    utils.command_runner.install()
    install_ffuf()
    utils.fzf_installer.install()
    utils.tmux_installer.install()
    utils.xclip_installer.install()
    utils.ghidra_installer.install()
    utils.john_installer.install()
    utils.hashcat_installer.install()
    utils.uv_tools_installer.install()
    
    # Configure shells and services at the very end
    configure_shells()
    utils.alias_manager.configure()
    utils.service_manager.disable_startup_services()
    
    print("\nAutomation script finished!")
