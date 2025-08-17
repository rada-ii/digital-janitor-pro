"""
Main organization logic for Digital Janitor Pro
"""
import shutil
from pathlib import Path
from utils.logger import write_to_log
from core.file_operations import get_file_size_mb, get_file_hash


class FileOrganizer:
    """Main class that handles file organization logic"""

    def __init__(self, root_dir, config, log_file):
        self.root_dir = Path(root_dir)
        self.config = config
        self.log_file = log_file
        self.closet_dir = self.root_dir / 'closet'
        self.file_hashes = {}
        self.duplicate_count = 0

        # Create all directories
        self._create_directory_structure()

    def _create_directory_structure(self):
        """Create all needed directories"""
        # Main closet
        self.closet_dir.mkdir(exist_ok=True)

        # Type-based directories
        self.text_dir = self.closet_dir / 'text_files'
        self.text_dir.mkdir(exist_ok=True)

        self.csv_dir = self.closet_dir / 'csv_files'
        self.csv_dir.mkdir(exist_ok=True)

        self.folders_dir = self.closet_dir / 'folders'
        self.folders_dir.mkdir(exist_ok=True)

        self.images_dir = self.closet_dir / 'images'
        self.images_dir.mkdir(exist_ok=True)

        self.documents_dir = self.closet_dir / 'documents'
        self.documents_dir.mkdir(exist_ok=True)

        self.media_dir = self.closet_dir / 'media'
        self.media_dir.mkdir(exist_ok=True)

        self.code_dir = self.closet_dir / 'code'
        self.code_dir.mkdir(exist_ok=True)

        # Size-based directories
        self.large_files_dir = self.closet_dir / 'large_files'
        self.large_files_dir.mkdir(exist_ok=True)

        self.huge_files_dir = self.closet_dir / 'huge_files'
        self.huge_files_dir.mkdir(exist_ok=True)

        self.empty_files_dir = self.closet_dir / 'empty_files'
        self.empty_files_dir.mkdir(exist_ok=True)

        # Special directories
        self.duplicates_dir = self.closet_dir / 'duplicates'
        self.duplicates_dir.mkdir(exist_ok=True)

    def organize_files(self):
        """Main method to organize all files"""
        write_to_log("Starting file organization...", self.log_file)

        large_threshold = self.config['size_thresholds']['large_mb']
        huge_threshold = self.config['size_thresholds']['huge_mb']

        for item in self.root_dir.iterdir():
            if item == self.closet_dir:
                continue
            elif item.is_file():
                self._process_file(item, large_threshold, huge_threshold)
            elif item.is_dir() and 'temp' in item.name:
                self._delete_temp_folder(item)
            elif item.is_dir():
                self._move_folder(item)

        # Log final statistics
        write_to_log(f"Organization complete. Found {self.duplicate_count} duplicates", self.log_file)

    def _process_file(self, file_path, large_threshold, huge_threshold):
        """Process a single file - check duplicates and organize"""
        # Get file hash
        file_hash = get_file_hash(file_path)
        if file_hash is None:
            write_to_log(f"SKIPPED file (hash error): {file_path.name}", self.log_file)
            return

        # Check for duplicates
        if file_hash in self.file_hashes:
            self._move_duplicate(file_path, file_hash)
            return

        # Add to hash tracker
        self.file_hashes[file_hash] = str(file_path)

        # Get file size and organize
        file_size = get_file_size_mb(file_path)

        if file_size == 0:
            self._move_file(file_path, self.empty_files_dir, "empty file")
        elif file_size > huge_threshold:
            self._move_file(file_path, self.huge_files_dir, f"huge file ({file_size:.1f}MB)")
        elif file_size > large_threshold:
            self._move_file(file_path, self.large_files_dir, f"large file ({file_size:.1f}MB)")
        else:
            self._organize_by_type(file_path)

    def _move_duplicate(self, file_path, file_hash):
        """Handle duplicate file"""
        self.duplicate_count += 1
        duplicate_name = f"{file_path.stem}_duplicate_{self.duplicate_count}{file_path.suffix}"
        shutil.move(file_path, self.duplicates_dir / duplicate_name)
        write_to_log(f"MOVED duplicate: {file_path.name} -> duplicates/{duplicate_name}", self.log_file)

    def _organize_by_type(self, file_path):
        """Organize file by its type/extension"""
        suffix = file_path.suffix.lower()

        if suffix == '.txt':
            self._move_file(file_path, self.text_dir, ".txt file")
        elif suffix == '.csv':
            self._move_file(file_path, self.csv_dir, ".csv file")
        elif suffix in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            self._move_file(file_path, self.images_dir, "image")
        elif suffix in ['.pdf', '.docx', '.xlsx', '.pptx', '.rtf']:
            self._move_file(file_path, self.documents_dir, "document")
        elif suffix in ['.mp4', '.avi', '.mp3', '.wav', '.mov']:
            self._move_file(file_path, self.media_dir, "media")
        elif suffix in ['.py', '.js', '.html', '.css', '.java']:
            self._move_file(file_path, self.code_dir, "code file")
        else:
            self._move_file(file_path, self.closet_dir, "other file")

    def _move_file(self, file_path, destination_dir, file_type):
        """Move file to destination and log"""
        shutil.move(file_path, destination_dir / file_path.name)
        write_to_log(f"MOVED {file_type}: {file_path.name} -> {destination_dir.name}/", self.log_file)

    def _delete_temp_folder(self, folder_path):
        """Delete temporary folder"""
        shutil.rmtree(folder_path)
        write_to_log(f"DELETED temp folder: {folder_path.name}", self.log_file)

    def _move_folder(self, folder_path):
        """Move regular folder to folders directory"""
        shutil.move(folder_path, self.folders_dir / folder_path.name)
        write_to_log(f"MOVED folder: {folder_path.name} -> folders/", self.log_file)