# File System Tricks: You could temporarily rename (e.g., .__media.json) the dotfiles to hide them from indexing, then rename them back when accessed.
    # The location of the system folder depends on the operating system you’re using:
        # Windows: %APPDATA%\\Obsidian\\
        # Linux: $XDG_CONFIG_HOME/Obsidian/ or ~/.config/Obsidian/

# Conceptual Workflow

# Runtime Clone:

# Use shutil.copy (or potentially shutil.copytree) to maintain a full, actively modified copy of your Obsidian vault.

# This clone serves as your unrestricted media manipulation playground.

# Cleanup & Diffing:

# Your Python script would implement logic to:

# Clean up unwanted changes in the clone (temporary files, etc).

# Identify the essential modifications to media files and their corresponding dotfiles.

# Selective Backport:

# Chroot: If feasible in your setup, temporarily chrooting into the original Obsidian vault location would provide a degree of isolation.

# Targeted Copying: Carefully copy only the approved changes back to the original vault, ensuring paths are adjusted if needed.