import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def install():
    """
    Clones, configures, builds, and installs tmux GLOBALLY from source,
    then creates a default user-specific configuration.
    """
    print("\n--- Installing 'tmux' from source (globally) ---")

    # 1. Check if tmux is already installed
    if shutil.which('tmux'):
        print("'tmux' is already installed. Skipping build process.")
    else:
        # 2. Check for dependencies
        if not all(shutil.which(cmd) for cmd in ['git', 'gcc', 'make']):
            print("ERROR: Build tools ('git', 'gcc', 'make') not found. Cannot build 'tmux'.")
            return

        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"Cloning tmux repository into temporary directory...")
            try:
                repo_url = "https://github.com/tmux/tmux.git"
                tmux_path = Path(tmpdir) / "tmux"
                subprocess.run(["git", "clone", "--depth", "1", repo_url, str(tmux_path)], check=True, capture_output=True)
                
                # THE CHANGE: Define the standard global installation prefix
                global_prefix = "/usr/local"

                # 3. Run the build process
                print("Configuring the build (autogen, configure)...")
                subprocess.run(["sh", "autogen.sh"], cwd=str(tmux_path), check=True, capture_output=True)
                
                # THE CHANGE: Use the global prefix in the configure command
                configure_cmd = ["./configure", f"--prefix={global_prefix}"]
                subprocess.run(configure_cmd, cwd=str(tmux_path), check=True, capture_output=True)

                print("Compiling with 'make'...")
                subprocess.run(["make"], cwd=str(tmux_path), check=True, capture_output=True)

                # THE CHANGE: Use 'sudo' for the install step
                print(f"Installing globally to {global_prefix} with 'sudo make install'...")
                subprocess.run(["sudo", "make", "install"], cwd=str(tmux_path), check=True, capture_output=True)

                print("'tmux' binary installed successfully.")
                print(f"It should be available in {global_prefix}/bin.")

            except subprocess.CalledProcessError as e:
                print(f"\nERROR: A command failed during 'tmux' installation: {e}")
                print(f"Stderr: {e.stderr.decode()}")
                return
            except Exception as e:
                print(f"\nAn unexpected error occurred during 'tmux' installation: {e}")
                return

    # --- Step 4: Create the configuration file for the CURRENT USER ---
    # This part remains user-specific, which is correct.
    print("Configuring tmux for the current user...")
    
    config_content = """
# Unbind the default prefix and Set new prefix to Ctrl+z
unbind C-b
set-option -g prefix C-x

bind c new-window -c '#{pane_current_path}'

# set -g mouse on

set -g history-limit 5000

setw -g mode-keys vi
bind -T copy-mode-vi v send -X begin-selection
bind -T copy-mode-vi C-v send -X rectangle-toggle
bind -T copy-mode-vi y send -X copy-pipe-and-cancel "xclip -selection clipboard -in"
bind -T copy-mode-vi Escape send -X cancel

bind | split-window -h
"""
    
    config_dir = Path.home() / ".config" / "tmux"
    config_file = config_dir / "tmux.conf"

    try:
        if config_file.exists():
            print(f"'{config_file}' already exists. Skipping configuration to avoid overwriting.")
        else:
            print(f"Creating default configuration at '{config_file}'...")
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file.write_text(config_content)
            print("tmux configuration created successfully.")
            
    except Exception as e:
        print(f"\nAn error occurred during tmux configuration: {e}")

if __name__ == "__main__":
    install()