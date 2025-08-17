# Digital Janitor Pro

Professional file organization tool with duplicate detection, backup, and restore functionality.

## Features

- **Smart File Organization** - Sorts files by type into organized directories
- **Duplicate Detection** - Uses MD5 hashing to find and handle duplicate files
- **Size-Based Sorting** - Separates large files with configurable thresholds
- **Backup & Restore** - Creates backup manifest and restore script for safety
- **Detailed Logging** - Comprehensive log of all operations
- **Configuration** - Customizable settings via JSON config file

## Quick Start

1. Clone and run:
```bash
git clone https://github.com/rada-ii/digital-janitor-pro.git
cd digital-janitor-pro
python main.py
```

2. Enter folder path when prompted
3. Optionally customize size thresholds
4. Files organized into `closet/` directory

## File Organization

Creates organized structure:
```
your_folder/
├── closet/
│   ├── images/        # .jpg, .png, .gif
│   ├── documents/     # .pdf, .docx, .xlsx
│   ├── media/         # .mp4, .mp3, .wav
│   ├── code/          # .py, .js, .html
│   ├── large_files/   # Files > threshold
│   ├── huge_files/    # Files > huge threshold
│   ├── empty_files/   # 0-byte files
│   ├── duplicates/    # Duplicate files
│   └── folders/       # Original directories
├── digital_janitor_log.txt      # Operation log
├── janitor_config.json          # Settings
├── .janitor_backup/             # Backup data
└── restore_original_structure.py # Undo script
```

## Safety Features

**Backup Before Processing:**
- Creates `.janitor_backup/` with manifest of original state
- Generates `restore_original_structure.py` to undo all changes

## Configuration

Customize thresholds in `janitor_config.json`:
```json
{
    "size_thresholds": {
        "large_mb": 100,
        "huge_mb": 1024
    },
    "features": {
        "delete_temp_folder": true,
        "sort_by_size": true
    }
}
```

## Supported File Types

- **Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`
- **Documents:** `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.rtf`
- **Media:** `.mp4`, `.avi`, `.mp3`, `.wav`, `.mov`
- **Code:** `.py`, `.js`, `.html`, `.css`, `.java`
- **Text:** `.txt`, `.csv`

## Requirements

- Python 3.6+
- No external dependencies (uses standard library only)

## Project Structure

```
digital-janitor-pro/
├── main.py              # Entry point
├── config/
│   └── config_manager.py # Settings management
├── core/
│   ├── file_operations.py # File utilities
│   └── organizer.py      # Main logic
└── utils/
    └── logger.py         # Logging
```

## Advanced Features

- **MD5 Duplicate Detection** - Finds identical files regardless of name
- **Size-Based Organization** - Handles large files intelligently  
- **Empty File Detection** - Identifies and separates 0-byte files
- **Temp Folder Cleanup** - Automatically removes temporary directories
- **Comprehensive Logging** - Detailed record of all operations
- **Safe Restoration** - One-click undo functionality

## Example Usage

**Before:**
```
messy_folder/
├── photo1.jpg
├── photo1_copy.jpg  # duplicate
├── document.pdf
├── large_video.mp4  # 2GB file
├── script.py
├── temp_downloads/  # will be deleted
└── empty_file.txt   # 0 bytes
```

**After:**
```
messy_folder/
├── closet/
│   ├── images/photo1.jpg
│   ├── documents/document.pdf
│   ├── huge_files/large_video.mp4
│   ├── code/script.py
│   ├── empty_files/empty_file.txt
│   └── duplicates/photo1_copy_duplicate_1.jpg
├── digital_janitor_log.txt
└── restore_original_structure.py
```

## Restore

To undo everything:
```bash
python restore_original_structure.py
```

**Warning**: Always test on unimportant folders first!


