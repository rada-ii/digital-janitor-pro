# Digital Janitor Pro

Professional file organization tool with **date-first structure** and duplicate detection.

## Features

- **Date-First Organization** - Organizes files by year/month, then by type
- **Hybrid Structure** - Combines chronological and categorical organization
- **Duplicate Detection** - Uses MD5 hashing to find and handle duplicate files
- **Size-Based Sorting** - Separates large files with configurable thresholds
- **Smart Restore** - Creates restore script to undo all changes
- **Detailed Logging** - Comprehensive log of all operations
- **Configuration** - Customizable settings via JSON config file

## Quick Start

1. **Clone and run:**
   ```bash
   git clone https://github.com/rada-ii/digital-janitor-pro.git
   cd digital-janitor-pro
   python main.py
   ```

2. **Enter folder path** when prompted
3. **Optionally customize** size thresholds
4. **Files organized** by date, then type

## Date-First Organization Structure

Creates year/month/type hierarchy:
```
your_folder/
├── 2025/
│   ├── 01/  (January)
│   │   ├── text_files/     # .txt files
│   │   ├── images/         # .jpg, .png, .gif
│   │   ├── documents/      # .pdf, .docx, .xlsx
│   │   ├── media/          # .mp4, .mp3, .wav
│   │   ├── code/           # .py, .js, .html
│   │   ├── large_files/    # Files > threshold
│   │   ├── duplicates/     # Duplicate files
│   │   ├── empty_files/    # 0-byte files
│   │   └── folders/        # Original directories
│   ├── 08/  (August)
│   │   ├── text_files/
│   │   ├── images/
│   │   └── documents/
│   └── 12/  (December)
├── 2024/
│   ├── 03/  (March)
│   └── 11/  (November)
├── 2023/
├── digital_janitor_log.txt      # Operation log
├── janitor_config.json          # Settings
└── restore_date_structure.py    # Restore script
```

## Why Date-First?

**Benefits:**
- ✅ **Reduced root folder load** - Only year directories in root
- ✅ **Faster indexing** - Hierarchical structure improves performance
- ✅ **Logical time organization** - Find files by when they were created
- ✅ **Cloud-friendly** - Flat structure works well with cloud storage
- ✅ **Scalable** - Handles thousands of files efficiently

**Perfect for:**
- Large file collections
- Photo libraries
- Document archives
- Development projects
- Any time-sensitive organization

## Configuration

Customize settings when prompted or edit `janitor_config.json`:
```json
{
    "size_thresholds": {
        "large_mb": 100,
        "huge_mb": 1024
    },
    "features": {
        "delete_temp_folder": true,
        "sort_by_size": true,
        "sort_by_date": true
    }
}
```

## Supported File Types

| Category | Extensions |
|----------|------------|
| **Text Files** | `.txt`, `.csv` |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp` |
| **Documents** | `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.rtf` |
| **Media** | `.mp4`, `.avi`, `.mp3`, `.wav`, `.mov` |
| **Code** | `.py`, `.js`, `.html`, `.css`, `.java` |
| **Other** | Any other file type → `other_files/` |

## Example Organization

**Before:**
```
messy_folder/
├── vacation_2025.jpg      # Modified: Aug 2025
├── report_draft.pdf       # Modified: Jan 2025
├── old_photo.jpg          # Modified: Mar 2024
├── script.py              # Modified: Aug 2025
├── duplicate_photo.jpg    # Same as vacation_2025.jpg
├── large_video.mp4        # 2GB file, Aug 2025
└── temp_downloads/        # Will be deleted
```

**After:**
```
messy_folder/
├── 2025/
│   ├── 01/
│   │   └── documents/
│   │       └── report_draft.pdf
│   └── 08/
│       ├── images/
│       │   └── vacation_2025.jpg
│       ├── code/
│       │   └── script.py
│       ├── huge_files/
│       │   └── large_video.mp4
│       └── duplicates/
│           └── duplicate_photo_duplicate_1.jpg
├── 2024/
│   └── 03/
│       └── images/
│           └── old_photo.jpg
├── digital_janitor_log.txt
└── restore_date_structure.py
```

## Safety Features

**Automatic Restore Script:**
- Generates `restore_date_structure.py` before processing
- One-click restoration to original flat structure
- Handles file name conflicts automatically

**System File Protection:**
- Skips log files, config files, and restore scripts
- Never organizes Python cache folders
- Preserves already organized year directories

## Restore Process

To undo the date organization:
```bash
cd your_organized_folder
python3 restore_date_structure.py
```

**Warning:** Always test on unimportant folders first!

## Requirements

- Python 3.7+
- No external dependencies (uses standard library only)

## Project Structure

```
digital-janitor-pro/
├── main.py                 # Application entry point
├── config/
│   └── config_manager.py   # Settings management
├── core/
│   ├── file_operations.py  # File utilities & backup
│   └── organizer.py        # Date-first organization logic
└── utils/
    └── logger.py           # Logging utilities
```

## Advanced Features

- **Date-Based File Sorting** - Uses file modification time for organization
- **MD5 Duplicate Detection** - Finds identical files regardless of name or location
- **Intelligent Size Handling** - Separates large files for better performance
- **Empty File Detection** - Identifies and isolates 0-byte files
- **Temp Folder Cleanup** - Automatically removes directories with "temp" in name
- **Comprehensive Logging** - Detailed record with timestamps
- **Dynamic Structure Creation** - Creates directories only when needed

Built for efficient file management with chronological organization priority.
