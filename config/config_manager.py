"""
Configuration management for Digital Janitor Pro
"""
import json
import datetime
from pathlib import Path


def create_default_config(config_path):
    """Create default config file"""
    default_config = {
        "folder_names": {
            "text_files": "text_files",
            "images": "images",
            "documents": "documents",
            "media": "media",
            "code": "code",
        },
        "size_thresholds": {
            "large_mb": 2,
            "huge_mb": 10,
        },
        "features": {
            "delete_temp_folder": True,
            "sort_by_size": True,
        }
    }

    with open(config_path, "w") as config_file:
        json.dump(default_config, config_file, indent=4)

    return default_config


def load_config(config_path):
    """Load configuration from file or create default"""
    if config_path.exists():
        try:
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
                return config
        except json.JSONDecodeError:
            print("Configuration file corrupted, creating new default config")
            return create_default_config(config_path)
    else:
        print("No config file found, creating new default config")
        return create_default_config(config_path)


def interactive_config_setup(config_path):
    """Interactive configuration setup for users"""
    print("\n=== CUSTOMIZE DIGITAL JANITOR SETTINGS ===")

    large_mb = input("Large file threshold in MB (default 100): ").strip()
    large_mb = int(large_mb) if large_mb else 100

    huge_mb = input("Huge file threshold in MB (default 1024): ").strip()
    huge_mb = int(huge_mb) if huge_mb else 1024

    custom_config = {
        "folder_names": {
            "text_files": "text_files",
            "images": "images",
            "documents": "documents",
            "media": "media",
            "code": "code"
        },
        "size_thresholds": {
            "large_mb": large_mb,
            "huge_mb": huge_mb
        },
        "features": {
            "delete_temp_folder": True,
            "sort_by_size": True
        }
    }

    with open(config_path, 'w') as config_file:
        json.dump(custom_config, config_file, indent=4)

    print(f"Custom configuration saved!")
    return custom_config