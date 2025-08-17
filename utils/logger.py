"""
Logging utilities for Digital Janitor Pro
"""
import datetime
from pathlib import Path


def write_to_log(message, log_file_path):
    """Write message to log file with timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: {message}\n"

    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry)