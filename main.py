#!/usr/bin/env python3
"""
DIGITAL JANITOR PRO - Main Application Entry Point
DATE-FIRST organization: Year/Month/Type structure
"""

import datetime
from pathlib import Path

# Import our custom modules
from utils.logger import write_to_log
from config.config_manager import load_config, interactive_config_setup
from core.organizer import FileOrganizer


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
        print(f"Will create Year/Month/Type structure directly in this folder")
        confirm = input("Continue? (y/n): ").strip().lower()

        if confirm == 'y':
            return root_dir
        else:
            print("Operation cancelled. Choose different folder.")
            continue


def main():
    """Main application function"""
    print("DIGITAL JANITOR PRO - DATE-FIRST File Organization")
    print("=" * 60)

    # Get target directory
    root_dir = get_target_directory()

    # Setup logging
    log_file = root_dir / 'digital_janitor_log.txt'
    write_to_log('=== DIGITAL JANITOR PRO STARTED (DATE-FIRST) ===', log_file)
    write_to_log(f"Target directory: {root_dir}", log_file)

    # Load or create configuration
    config_file_path = root_dir / 'janitor_config.json'
    config = load_config(config_file_path)
    write_to_log(f"Config loaded: {config_file_path}", log_file)

    # Optional configuration customization
    if not config_file_path.exists() or input("\nCustomize settings? (y/n): ").strip().lower() == 'y':
        config = interactive_config_setup(config_file_path)
        write_to_log("User customized configuration", log_file)

    # Create simple restore script for date structure
    print("Generating restore script...")
    restore_script_path = root_dir / 'restore_date_structure.py'
    restore_code = f'''#!/usr/bin/env python3
"""
DIGITAL JANITOR PRO - DATE STRUCTURE RESTORE SCRIPT
Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Restores files from Year/Month/Type structure back to root directory.
"""

import shutil
from pathlib import Path

def restore_files():
    """Restore all files from date structure to root"""
    print("Starting restore process...")

    root_dir = Path("{root_dir}")
    restored_count = 0

    # Go through all year directories
    for year_dir in root_dir.iterdir():
        if year_dir.is_dir() and year_dir.name.isdigit() and len(year_dir.name) == 4:
            print(f"Processing year {{year_dir.name}}")

            # Go through all month directories
            for month_dir in year_dir.iterdir():
                if month_dir.is_dir():
                    print(f"  Processing month {{month_dir.name}}")

                    # Go through all type directories
                    for type_dir in month_dir.iterdir():
                        if type_dir.is_dir():
                            # Move all files back to root
                            for file_item in type_dir.iterdir():
                                if file_item.is_file():
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
                                        print(f"    Restored: {{file_item.name}}")
                                        restored_count += 1
                                    except Exception as e:
                                        print(f"    Error: {{e}}")

    # Remove empty year directories
    for year_dir in root_dir.iterdir():
        if year_dir.is_dir() and year_dir.name.isdigit() and len(year_dir.name) == 4:
            try:
                if not any(year_dir.rglob('*')):  # If empty
                    shutil.rmtree(year_dir)
                    print(f"Removed empty year directory: {{year_dir.name}}")
            except:
                pass

    print(f"\\nRestore complete! Restored {{restored_count}} files.")

if __name__ == "__main__":
    confirm = input("WARNING: This will restore all files to root directory. Continue? (y/n): ")
    if confirm.lower() == 'y':
        restore_files()
    else:
        print("Restore cancelled.")
'''

    with open(restore_script_path, 'w') as f:
        f.write(restore_code)

    write_to_log(f"Restore script created: {restore_script_path}", log_file)

    # Initialize and run file organizer
    print("\nStarting DATE-FIRST file organization...")
    organizer = FileOrganizer(root_dir, config, log_file)
    organizer.organize_files()

    # Final completion message
    write_to_log("=== DATE-FIRST ORGANIZATION COMPLETED ===", log_file)

    print("\nORGANIZATION COMPLETE!")
    print("=" * 60)
    print(f"Log file: {log_file.name}")
    print(f"Config file: {config_file_path.name}")
    print(f"Restore script: {restore_script_path.name}")
    print("\nFiles organized by: Year/Month/Type structure")
    print("Example: 2025/08/images/photo.jpg")
    print("\nTO RESTORE ORIGINAL STRUCTURE:")
    print(f"   cd {root_dir}")
    print("   python restore_date_structure.py")


if __name__ == "__main__":
    main()
