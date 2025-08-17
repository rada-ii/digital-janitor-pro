# 🧹 Digital Janitor Pro

Automatically organizes messy folders by sorting files into categories with duplicate detection and restore functionality.

## Features

- **File Organization** - Sorts files by type (images, documents, media, code, etc.)
- **Duplicate Detection** - Finds and moves duplicate files using MD5 hashing
- **Size-Based Sorting** - Separates large files (configurable thresholds)
- **Backup & Restore** - Creates backup and generates restore script
- **Logging** - Detailed log of all operations

## Quick Start

1. **Clone and run**
   ```bash
   git clone https://github.com/rada-ii/digital-janitor-pro.git
   cd digital-janitor-pro
   python main.py
   ```

2. **Enter folder path** when prompted
3. **Optional**: Customize size thresholds
4. **Done!** Files organized into `closet/` directory

## How it works

Creates organized structure:
```
your_folder/
├── closet/
│   ├── images/        # .jpg, .png, .gif
│   ├── documents/     # .pdf, .docx, .xlsx  
│   ├── media/         # .mp4, .mp3, .wav
│   ├── code/          # .py, .js, .html
│   ├── large_files/   # Files > threshold
│   ├── duplicates/    # Duplicate files
│   └── folders/       # Original directories
├── digital_janitor_log.txt      # What was done
└── restore_original_structure.py  # Undo script
```

## Restore

To undo everything:
```bash
python restore_original_structure.py
```

**Warning**: Always test on unimportant folders first!

## Requirements

- Python 3.7+
- No external dependencies (uses standard library only)

## Project Structure

```
├── main.py                 # Main application
├── config/
│   └── config_manager.py   # Settings management
├── core/
│   ├── file_operations.py  # File utilities
│   └── organizer.py        # Main logic
└── utils/
    └── logger.py           # Logging
```

Built with Python automation skills.
