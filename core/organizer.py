"""
Main organization logic for Digital Janitor Pro
PURE DATE-FIRST ORGANIZATION: Year/Month/Type structure
"""
import shutil
import datetime
from pathlib import Path
from utils.logger import write_to_log
from core.file_operations import get_file_size_mb, get_file_hash


class FileOrganizer:
    """Main class that handles file organization logic"""

    def __init__(self, root_dir, config, log_file):
        self.root_dir = Path(root_dir)
        self.config = config
        self.log_file = log_file
        self.file_hashes = {}
        self.duplicate_count = 0

        # NO pre-created structure - everything is dynamic based on file dates!

    def _get_date_structure_for_file(self, file_path):
        """Get year/month structure for file based on its date"""
        # Get file modification time
        mod_time = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
        year = str(mod_time.year)
        month = f"{mod_time.month:02d}"  # 01, 02, 03... 12

        # Base directory: root/2025/05/
        date_base = self.root_dir / year / month

        return date_base, year, month

    def _create_type_directories_in_month(self, month_dir):
        """Create all type subdirectories within a month directory"""
        type_dirs = {
            'text_files': month_dir / 'text_files',
            'csv_files': month_dir / 'csv_files',
            'images': month_dir / 'images',
            'documents': month_dir / 'documents',
            'media': month_dir / 'media',
            'code': month_dir / 'code',
            'large_files': month_dir / 'large_files',
            'huge_files': month_dir / 'huge_files',
            'empty_files': month_dir / 'empty_files',
            'duplicates': month_dir / 'duplicates',
            'folders': month_dir / 'folders',
            'other_files': month_dir / 'other_files'
        }

        # Create month directory first
        month_dir.mkdir(parents=True, exist_ok=True)

        # Create type directories on demand
        for dir_path in type_dirs.values():
            dir_path.mkdir(exist_ok=True)

        return type_dirs

    def organize_files(self):
        """Main method to organize all files"""
        write_to_log("Starting DATE-FIRST organization (Year/Month/Type)...", self.log_file)

        large_threshold = self.config['size_thresholds']['large_mb']
        huge_threshold = self.config['size_thresholds']['huge_mb']

        for item in self.root_dir.iterdir():
            # Skip already organized year directories
            if item.is_dir() and item.name.isdigit() and len(item.name) == 4:
                continue
            # Skip system files AND Python cache
            elif (item.name.startswith('.janitor') or
                  item.name == 'digital_janitor_log.txt' or
                  item.name == 'janitor_config.json' or
                  item.name.startswith('restore_') or
                  item.name == '__pycache__'):
                continue
            elif item.is_file():
                self._process_file(item, large_threshold, huge_threshold)
            elif item.is_dir() and 'temp' in item.name:
                self._delete_temp_folder(item)
            elif item.is_dir():
                self._move_folder(item)

        # Log final statistics
        write_to_log(f"DATE-FIRST organization complete. Found {self.duplicate_count} duplicates", self.log_file)

    def _process_file(self, file_path, large_threshold, huge_threshold):
        """Process a single file - organize by date then type"""

        # Get file hash for duplicate detection
        file_hash = get_file_hash(file_path)
        if file_hash is None:
            write_to_log(f"SKIPPED file (hash error): {file_path.name}", self.log_file)
            return

        # Get date structure for this file
        month_dir, year, month = self._get_date_structure_for_file(file_path)

        # Create type directories within this month
        type_dirs = self._create_type_directories_in_month(month_dir)

        # Check for duplicates
        if file_hash in self.file_hashes:
            self._move_duplicate_to_month(file_path, type_dirs['duplicates'], year, month)
            return

        # Add to hash tracker
        self.file_hashes[file_hash] = str(file_path)

        # Organize by size first, then by type
        file_size = get_file_size_mb(file_path)

        if file_size == 0:
            self._move_file_to_month(file_path, type_dirs['empty_files'], "empty file", year, month)
        elif file_size > huge_threshold:
            self._move_file_to_month(file_path, type_dirs['huge_files'], f"huge file ({file_size:.1f}MB)", year, month)
        elif file_size > large_threshold:
            self._move_file_to_month(file_path, type_dirs['large_files'], f"large file ({file_size:.1f}MB)", year, month)
        else:
            self._organize_by_type_in_month(file_path, type_dirs, year, month)

    def _move_duplicate_to_month(self, file_path, destination_dir, year, month):
        """Handle duplicate file in month structure"""
        self.duplicate_count += 1
        duplicate_name = f"{file_path.stem}_duplicate_{self.duplicate_count}{file_path.suffix}"
        shutil.move(file_path, destination_dir / duplicate_name)

        write_to_log(f"MOVED duplicate: {file_path.name} -> {year}/{month}/duplicates/{duplicate_name}", self.log_file)

    def _organize_by_type_in_month(self, file_path, type_dirs, year, month):
        """Organize file by type within month structure"""
        suffix = file_path.suffix.lower()

        if suffix == '.txt':
            self._move_file_to_month(file_path, type_dirs['text_files'], ".txt file", year, month)
        elif suffix == '.csv':
            self._move_file_to_month(file_path, type_dirs['csv_files'], ".csv file", year, month)
        elif suffix in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            self._move_file_to_month(file_path, type_dirs['images'], "image", year, month)
        elif suffix in ['.pdf', '.docx', '.xlsx', '.pptx', '.rtf']:
            self._move_file_to_month(file_path, type_dirs['documents'], "document", year, month)
        elif suffix in ['.mp4', '.avi', '.mp3', '.wav', '.mov']:
            self._move_file_to_month(file_path, type_dirs['media'], "media", year, month)
        elif suffix in ['.py', '.js', '.html', '.css', '.java']:
            self._move_file_to_month(file_path, type_dirs['code'], "code file", year, month)
        else:
            self._move_file_to_month(file_path, type_dirs['other_files'], "other file", year, month)

    def _move_file_to_month(self, file_path, destination_dir, file_type, year, month):
        """Move file to month-based destination and log"""
        shutil.move(file_path, destination_dir / file_path.name)

        # Create readable path for logging
        folder_name = destination_dir.name
        write_to_log(f"MOVED {file_type}: {file_path.name} -> {year}/{month}/{folder_name}/", self.log_file)

    def _delete_temp_folder(self, folder_path):
        """Delete temporary folder"""
        shutil.rmtree(folder_path)
        write_to_log(f"DELETED temp folder: {folder_path.name}", self.log_file)

    def _move_folder(self, folder_path):
        """Move regular folder to appropriate month structure"""
        # Get folder modification time
        mod_time = datetime.datetime.fromtimestamp(folder_path.stat().st_mtime)
        year = str(mod_time.year)
        month = f"{mod_time.month:02d}"

        # Create month structure
        month_base = self.root_dir / year / month
        folders_dir = month_base / 'folders'
        folders_dir.mkdir(parents=True, exist_ok=True)

        # Move folder
        shutil.move(folder_path, folders_dir / folder_path.name)
        write_to_log(f"MOVED folder: {folder_path.name} -> {year}/{month}/folders/", self.log_file)
