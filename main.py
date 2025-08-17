#!/usr/bin/env python3
"""
DIGITAL JANITOR PRO - Main Application Entry Point
Professional file organization and automation tool
"""

import datetime
from pathlib import Path

# Import our custom modules
from utils.logger import write_to_log
from config.config_manager import load_config, interactive_config_setup
from core.organizer import FileOrganizer
from core.file_operations import create_backup_manifest, generate_restore_script


def get_target_directory():
    """Get and validate target directory from user"""
    while True:
        user_input = input('Please enter the full path to target folder: ').strip()

        # Check if empty
        if not user_input:
            print("Path cannot be empty! Please try again.")
            continue

        root_dir = Path(user_input)

        # Check if exists
        if not root_dir.exists():
            print(f"Path '{user_input}' does not exist! Please try again.")
            continue

        # Check if it's current project directory
        current_dir = Path.cwd()
        if root_dir == current_dir or root_dir in current_dir.parents:
            print(f"Cannot organize project directory! Current dir: {current_dir}")
            print("Choose a different folder outside your project.")
            continue

        # Safety confirmation
        print(f"\nWill organize folder: {root_dir}")
        print(f"Will create 'closet' directory inside this folder")
        confirm = input("Continue? (y/n): ").strip().lower()

        if confirm == 'y':
            return root_dir
        else:
            print("Operation cancelled. Choose different folder.")
            continue


def main():
    """Main application function"""
    print("DIGITAL JANITOR PRO - Professional File Organization")
    print("=" * 60)

    # Get target directory
    root_dir = get_target_directory()

    # Setup logging
    log_file = root_dir / 'digital_janitor_log.txt'
    write_to_log('=== DIGITAL JANITOR PRO STARTED ===', log_file)
    write_to_log(f"Target directory: {root_dir}", log_file)

    # Load or create configuration
    config_file_path = root_dir / 'janitor_config.json'
    config = load_config(config_file_path)
    write_to_log(f"Config loaded: {config_file_path}", log_file)

    # Optional configuration customization
    if not config_file_path.exists() or input("\nCustomize settings? (y/n): ").strip().lower() == 'y':
        config = interactive_config_setup(config_file_path)
        write_to_log("User customized configuration", log_file)

    # Create backup before processing
    print("\nCreating backup manifest...")
    backup_dir = root_dir / '.janitor_backup'
    backup_dir.mkdir(exist_ok=True)

    backup_manifest = create_backup_manifest(root_dir, backup_dir)
    write_to_log(f"Backup manifest created with {len(backup_manifest['files'])} files", log_file)

    # Initialize and run file organizer
    print("Starting file organization...")
    organizer = FileOrganizer(root_dir, config, log_file)
    organizer.organize_files()

    # Generate restore script
    print("Generating restore script...")
    restore_script_path = generate_restore_script(backup_manifest, root_dir)
    write_to_log(f"Restore script created: {restore_script_path}", log_file)

    # Final completion message
    write_to_log("=== CLEANUP COMPLETED ===", log_file)

    print("\nORGANIZATION COMPLETE!")
    print("=" * 60)
    print(f"Log file: {log_file.name}")
    print(f"Config file: {config_file_path.name}")
    print(f"Backup: {backup_dir.name}/")
    print(f"Restore script: {restore_script_path.name}")
    print("\nTO RESTORE ORIGINAL STRUCTURE:")
    print(f"   cd {root_dir}")
    print("   python3 restore_original_structure.py")
    print("   (or open the file in PyCharm and run it)")


if __name__ == "__main__":
    main()