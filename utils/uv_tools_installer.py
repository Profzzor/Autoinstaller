# Save this file as uv_tools_installer.py
import sys
import shutil
import subprocess

# The list now uses a dictionary to be more explicit.
# We check for a REAL impacket executable, like 'secretsdump.py'.
UV_TOOLS = [
    {
        "check_name": "netexec",
        "display_name": "NetExec",
        "url": "https://github.com/Pennyw0rth/NetExec",
        "extra": None
    },
    {
        "check_name": "bloodyAD",
        "display_name": "BloodyAD",
        "url": "https://github.com/CravateRouge/bloodyAD",
        "extra": None
    },
    {
        "check_name": "certipy",
        "display_name": "Certipy",
        "url": "https://github.com/ly4k/Certipy",
        "extra": None
    },
    {
        "check_name": "vol",
        "display_name": "Volatility3",
        "url": "https://github.com/volatilityfoundation/volatility3",
        "extra": None
    },
    {
        "check_name": "mitmproxy",
        "display_name": "mitmproxy",
        "url": "https://github.com/mitmproxy/mitmproxy",
        "extra": None
    },
    {
        "check_name": "powerview",
        "display_name": "powerview.py",
        "url": "https://github.com/aniqfakhrul/powerview.py",
        "extra": None
    },
    {
        "check_name": "evil-winrm-py",
        "display_name": "evil-winrm",
        "url": "https://github.com/adityatelange/evil-winrm-py",
        "extra": "kerberos"
    },
    {
        "check_name": "secretsdump.py",
        "display_name": "Impacket Suite",
        "url": "https://github.com/fortra/impacket",
        "extra": None
    },
    {
        "check_name": "oleid",
        "display_name": "Ole Tools",
        "url": "https://github.com/decalage2/oletools",
        "extra": None
    }
]

def install():
    """
    Installs a list of Python tools using 'uv tool install', checking for
    a specific executable to determine if the tool is already installed.
    """
    print("\n--- Installing Python tools with 'uv tool' ---")
    if not shutil.which('uv'):
        print("ERROR: 'uv' command not found."); return

    for tool in UV_TOOLS:
        check_name = tool["check_name"]
        display_name = tool["display_name"]
        url = tool["url"]
        extra = tool["extra"]

        print(f"\nProcessing tool: {display_name}")
        
        # This is now the one, correct way to check for all tools.
        if shutil.which(check_name):
            print(f"Executable '{check_name}' found. Skipping installation of {display_name}.")
            continue
        
        # Construct the source URL with the optional extra
        source_url = f"git+{url}"
        if extra:
            source_url += f"[{extra}]"
            print(f"Installing '{display_name}' from {url} with '{extra}' support...")
        else:
            print(f"Installing '{display_name}' from {url}...")
            
        try:
            command = [sys.executable, "-m", "uv", "tool", "install", source_url]
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"'{display_name}' installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"\nERROR: Failed to install '{display_name}': {e}\nStderr: {e.stderr}")
        except Exception as e:
            print(f"\nAn unexpected error occurred while installing '{display_name}': {e}")

if __name__ == "__main__":
    install()
