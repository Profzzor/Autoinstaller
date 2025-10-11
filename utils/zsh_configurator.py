# Save this file as zsh_configurator.py
import os
import shutil
from pathlib import Path

def configure():
    """
    Configures ~/.zshrc by replacing existing settings or appending them if they don't exist.
    """
    print("\n--- Configuring Zsh (~/.zshrc) ---")
    zshrc_path = Path.home() / ".zshrc"
    if not zshrc_path.exists():
        print("No .zshrc file found. Skipping."); return

    with open(zshrc_path, "r") as f:
        lines = f.readlines()
    original_content = "".join(lines)

    # --- Pass 1: Replace existing settings ---
    hist_found = False
    for i, line in enumerate(lines):
        if line.strip().startswith("HISTFILESIZE="):
            lines[i] = "HISTFILESIZE=0\n"
            hist_found = True
            break
            
    # --- Pass 2: Append settings that were not found ---
    current_content = "".join(lines)
    lines_to_append = []

    # Idempotent PATH check for Hashcat
    hashcat_block = """
# Add Hashcat to PATH if not already added
if [[ ":$PATH:" != *":/opt/hashcat/tools:"* ]]; then
  export PATH="/opt/hashcat/tools:$PATH"
fi
"""
    if "/opt/hashcat/tools" not in current_content:
        lines_to_append.append(hashcat_block)
        
    # Idempotent PATH check for John the Ripper
    john_block = """
# Add John the Ripper to PATH if not already added
if [[ ":$PATH:" != *":/opt/john:"* ]]; then
  export PATH="/opt/john:$PATH"
fi
"""
    if "/opt/john" not in current_content:
        lines_to_append.append(john_block)

    # Add HISTFILESIZE=0 if it was never found
    if not hist_found:
        lines_to_append.append("\n# Disable zsh history file\n")
        lines_to_append.append("HISTFILESIZE=0\n")

    # Add case-insensitive completion if missing
    if "zstyle ':completion:*' matcher-list" not in current_content:
        lines_to_append.append("\n# Enable case-insensitive tab completion\n")
        lines_to_append.append("zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'\n")
		
		# --- ADD FZF INTEGRATION ---
    fzf_zsh_line = 'source <(fzf --zsh)'
    if fzf_zsh_line not in current_content:
        lines_to_append.append("\n# FZF integration for shell history search (CTRL+R)\n")
        lines_to_append.append(fzf_zsh_line + '\n')
        
    # --- Final Write Operation ---
    final_content = "".join(lines) + "".join(lines_to_append)
    
    if final_content != original_content:
        backup_path = zshrc_path.with_suffix(".zshrc.bak")
        if not backup_path.exists():
            shutil.copy(zshrc_path, backup_path); print(f"Backup created: {backup_path}")
        
        with open(zshrc_path, "w") as f:
            f.write(final_content)
        print("~/.zshrc was updated successfully.")
        print("\nRun 'source ~/.zshrc' to apply changes.")
    else:
        print("~/.zshrc already contains all required settings. No changes made.")

if __name__ == "__main__":
    configure()
