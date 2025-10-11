# Save this file as bash_configurator.py
import os
import shutil
from pathlib import Path

def configure():
    """
    Configures ~/.bashrc by replacing existing settings or appending them if they don't exist.
    """
    print("\n--- Configuring Bash (~/.bashrc) ---")
    bashrc_path = Path.home() / ".bashrc"
    if not bashrc_path.exists():
        print("No .bashrc file found. Skipping."); return

    with open(bashrc_path, "r") as f:
        lines = f.readlines()
    original_content = "".join(lines)

    # --- Pass 1: Replace existing settings ---
    hist_found = False
    for i, line in enumerate(lines):
        # Find the line and replace its value
        if line.strip().startswith("HISTFILESIZE="):
            lines[i] = "HISTFILESIZE=0\n"
            hist_found = True
            break
            
    # --- Pass 2: Append settings that were not found ---
    # Convert back to a single string for easy 'in' checking of multi-line blocks
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

    # Add HISTFILESIZE=0 if it was never found to be replaced
    if not hist_found:
        lines_to_append.append("\n# Disable bash history file\n")
        lines_to_append.append("HISTFILESIZE=0\n")

    # Add case-insensitive completion if missing
    if 'bind "set completion-ignore-case on"' not in current_content:
        lines_to_append.append("\n# Enable case-insensitive tab completion\n")
        lines_to_append.append('bind "set completion-ignore-case on"\n')
        
    # --- ADD FZF INTEGRATION ---
    fzf_bash_line = 'eval "$(fzf --bash)"'
    if fzf_bash_line not in current_content:
        lines_to_append.append("\n# FZF integration for shell history search (CTRL+R)\n")
        lines_to_append.append(fzf_bash_line + '\n')

    # --- Final Write Operation ---
    final_content = "".join(lines) + "".join(lines_to_append)
    
    if final_content != original_content:
        backup_path = bashrc_path.with_suffix(".bashrc.bak")
        if not backup_path.exists():
            shutil.copy(bashrc_path, backup_path); print(f"Backup created: {backup_path}")
        
        with open(bashrc_path, "w") as f:
            f.write(final_content)
        print("~/.bashrc was updated successfully.")
        print("\nRun 'source ~/.bashrc' to apply changes.")
    else:
        print("~/.bashrc already contains all required settings. No changes made.")

if __name__ == "__main__":
    configure()
