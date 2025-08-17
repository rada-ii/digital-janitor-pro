"""
File operation utilities for Digital Janitor Pro
"""
import hashlib
from pathlib import Path


def get_file_size_mb(file_path):
    """Returns file size in MB"""
    size_bytes = Path(file_path).stat().st_size
    size_mb = size_bytes / (1024 * 1024)
    return size_mb


def get_file_hash(file_path):
    """Generate MD5 hash for file content"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

import datetime
import json


def create_backup_manifest(root_dir, backup_dir):
    """Create detailed backup of current directory state"""
    manifest = {
        "timestamp": datetime.datetime.now().isoformat(),
        "root_directory": str(root_dir),
        "files": [],
        "folders": []
    }

    # Scan all files and folders
    for item in root_dir.iterdir():
        if item.name.startswith('.janitor'):
            continue

        if item.is_file():
            manifest["files"].append({
                "name": item.name,
                "path": str(item),
                "size": item.stat().st_size,
                "modified": item.stat().st_mtime
            })
        elif item.is_dir():
            manifest["folders"].append({
                "name": item.name,
                "path": str(item)
            })

    # Save manifest
    manifest_file = backup_dir / 'backup_manifest.json'
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=4)

    return manifest


def generate_restore_script(backup_manifest, root_dir):
    """Generate Python script that can restore original state"""
    restore_code = f'''#!/usr/bin/env python3
"""
DIGITAL JANITOR PRO - RESTORE SCRIPT
Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Restores files to original state before Digital Janitor Pro ran.
"""

import shutil
from pathlib import Path

def restore_files():
    """Restore all files to original locations"""
    print("Starting restore process...")

    root_dir = Path("{root_dir}")
    closet_dir = root_dir / "closet"

    if not closet_dir.exists():
        print("ERROR: No closet directory found - nothing to restore!")
        return

    restored_count = 0

    # Restore files from all subdirectories
    for subdir in closet_dir.iterdir():
        if subdir.is_dir():
            print(f"Processing {{subdir.name}}/")
            for file_item in subdir.iterdir():
                if file_item.is_file():
                    # Move back to root directory
                    destination = root_dir / file_item.name

                    # Handle name conflicts
                    counter = 1
                    while destination.exists():
                        stem = file_item.stem
                        suffix = file_item.suffix
                        destination = root_dir / f"{{stem}}_restored_{{counter}}{{suffix}}"
                        counter += 1

                    try:
                        shutil.move(file_item, destination)
                        print(f"SUCCESS: Restored {{file_item.name}} -> {{destination.name}}")
                        restored_count += 1
                    except Exception as e:
                        print(f"ERROR: Failed to restore {{file_item.name}}: {{e}}")

    # Remove empty closet directory
    try:
        shutil.rmtree(closet_dir)
        print("SUCCESS: Removed closet directory")
    except Exception as e:
        print(f"WARNING: Could not remove closet directory: {{e}}")

    print(f"\\nRestore complete! Restored {{restored_count}} files.")

if __name__ == "__main__":
    confirm = input("WARNING: This will restore all files to root directory. Continue? (y/n): ")
    if confirm.lower() == 'y':
        restore_files()
    else:
        print("Restore cancelled.")
'''

    # Save restore script
    restore_script_path = root_dir / 'restore_original_structure.py'
    with open(restore_script_path, 'w') as f:
        f.write(restore_code)

    return restore_script_path