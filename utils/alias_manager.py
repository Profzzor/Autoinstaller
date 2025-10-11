from pathlib import Path

# Define all aliases to be managed here.
# The `cd -` returns you to your original directory after the command runs.
ALIASES = {
    "john": "alias john='/opt/john/john'",
    "hashcat": "alias hashcat='/opt/hashcat/hashcat'"
}

def configure():
    """
    Creates and manages the ~/.bash_aliases file.
    """
    print("\n--- Configuring Shell Aliases (~/.bash_aliases) ---")
    aliases_path = Path.home() / ".bash_aliases"
    
    # Read existing aliases if the file exists
    try:
        with open(aliases_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    lines_to_add = []

    # Check each alias we want to manage
    for name, alias_string in ALIASES.items():
        # Check if an alias for this command name already exists
        if f"alias {name}=" not in content:
            lines_to_add.append(f"\n# Alias for {name}\n")
            lines_to_add.append(alias_string + "\n")

    if lines_to_add:
        with open(aliases_path, "a") as f:
            f.writelines(lines_to_add)
        print(f"~/.bash_aliases was updated with new aliases.")
    else:
        print("All required aliases are already present in ~/.bash_aliases.")

if __name__ == "__main__":
    configure()