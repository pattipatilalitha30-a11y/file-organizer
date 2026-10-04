"""
File Organizer Application
==========================
Internship Project 4: File Organizer
Organizes files inside a target folder into category sub-folders based on their extensions.

Modules Used:
- os: File system path handling, directory scanning, and creation.
- shutil: High-level file moving operations.
- sys: System-level argument parsing and exit handling.

Features:
- Categorizes files by extension (PDF, Images, Documents, Videos, Audio, Code, Others).
- Handles files without extensions safely.
- Never overwrites existing files; generates collision-free unique names (e.g., file_1.pdf).
- Protects the project folder and system directories from accidental organization.
- Ignores existing subdirectories (moves files only).
- Robust error handling for invalid paths, permission errors, and I/O failures.
- Detailed operation log and final execution summary.
"""

import os
import shutil
import sys
from typing import Dict, List, Tuple


# Extension to category mapping
EXTENSION_CATEGORIES: Dict[str, List[str]] = {
    "PDF": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff", ".ico"],
    "Documents": [".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".tsv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".m4v"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"],
    "Code": [".py", ".js", ".java", ".c", ".cpp", ".cs", ".html", ".css", ".json", ".xml", ".sh", ".ts", ".php", ".rb", ".sql", ".go", ".rs"],
}

# Reverse lookup table: extension -> category
EXT_TO_CATEGORY: Dict[str, str] = {}
for category, extensions in EXTENSION_CATEGORIES.items():
    for ext in extensions:
        EXT_TO_CATEGORY[ext.lower()] = category

DEFAULT_CATEGORY = "Others"

# Protected project files to never move even if located in the target directory
PROTECTED_PROJECT_FILES = {
    "file_organizer.py",
    "requirements.txt",
    "README.md",
    ".gitignore",
    "test_organizer.py",
}


def get_category_for_file(filename: str) -> str:
    """
    Determines the category folder name based on the file extension.
    Files without extensions or unknown extensions are assigned to 'Others'.
    
    Args:
        filename: Name of the file (e.g., 'report.pdf')
        
    Returns:
        Category name string (e.g., 'PDF', 'Images', 'Others')
    """
    _, ext = os.path.splitext(filename)
    if not ext:
        # File has no extension (e.g., 'Makefile', 'LICENSE', 'data')
        return DEFAULT_CATEGORY
    return EXT_TO_CATEGORY.get(ext.lower(), DEFAULT_CATEGORY)


def get_unique_destination_path(dest_folder: str, filename: str) -> Tuple[str, bool]:
    """
    Generates a unique destination path to prevent overwriting existing files.
    If 'file.pdf' exists in dest_folder, generates 'file_1.pdf', 'file_2.pdf', etc.
    
    Args:
        dest_folder: Target directory path
        filename: Original file name
        
    Returns:
        Tuple of (unique_destination_path, was_renamed_boolean)
    """
    dest_path = os.path.join(dest_folder, filename)
    if not os.path.exists(dest_path):
        return dest_path, False

    name, ext = os.path.splitext(filename)
    counter = 1
    while True:
        new_filename = f"{name}_{counter}{ext}"
        new_dest_path = os.path.join(dest_folder, new_filename)
        if not os.path.exists(new_dest_path):
            return new_dest_path, True
        counter += 1


def is_safe_target_directory(target_path: str) -> Tuple[bool, str]:
    """
    Validates the target path for existence, directory type, and safety.
    Prevents running directly on the project's own directory or system roots.
    
    Args:
        target_path: Absolute or relative directory path to validate
        
    Returns:
        Tuple of (is_safe, error_or_warning_message)
    """
    if not target_path or not target_path.strip():
        return False, "Target folder path cannot be empty."

    norm_path = os.path.abspath(os.path.expanduser(target_path.strip().strip('"').strip("'")))

    if not os.path.exists(norm_path):
        return False, f"The path '{norm_path}' does not exist."

    if not os.path.isdir(norm_path):
        return False, f"The path '{norm_path}' is not a directory."

    # Prevent organizing root drives (e.g., C:\ or /)
    parent = os.path.dirname(norm_path)
    if parent == norm_path or norm_path.rstrip("\\/") in ("C:", "c:", "/"):
        return False, f"Safety restriction: Cannot organize the root drive '{norm_path}'."

    # Prevent accidental organization of current project script directory
    script_dir = os.path.abspath(os.path.dirname(__file__))
    if norm_path == script_dir:
        return False, (
            f"Safety restriction: The selected folder is the File Organizer project directory "
            f"('{norm_path}').\nPlease select an external target folder or a dedicated test folder."
        )

    return True, norm_path


def organize_folder(target_folder: str) -> Dict[str, any]:
    """
    Scans the target directory, categorizes files by extension, creates
    category sub-folders, and moves files into them safely.
    
    Args:
        target_folder: Validated path of directory to organize
        
    Returns:
        Dictionary containing summary statistics
    """
    target_folder = os.path.abspath(target_folder)
    
    summary = {
        "target_folder": target_folder,
        "scanned_items": 0,
        "directories_skipped": 0,
        "protected_skipped": 0,
        "files_moved": 0,
        "files_renamed": 0,
        "errors": [],
        "category_counts": {},
    }

    print("\n" + "=" * 65)
    print(f"  Starting File Organization on:")
    print(f"  {target_folder}")
    print("=" * 65)

    try:
        entries = os.listdir(target_folder)
    except PermissionError as e:
        error_msg = f"Permission denied while reading '{target_folder}': {e}"
        print(f"\n[ERROR] {error_msg}")
        summary["errors"].append(error_msg)
        return summary
    except OSError as e:
        error_msg = f"OS error while accessing '{target_folder}': {e}"
        print(f"\n[ERROR] {error_msg}")
        summary["errors"].append(error_msg)
        return summary

    summary["scanned_items"] = len(entries)

    for item in entries:
        item_path = os.path.join(target_folder, item)

        # Requirement: Do not move folders, only files
        if os.path.isdir(item_path):
            summary["directories_skipped"] += 1
            continue

        # Requirement: Do not organize project files if encountered
        if item in PROTECTED_PROJECT_FILES:
            print(f"[PROTECTED] Skipping project file: {item}")
            summary["protected_skipped"] += 1
            continue

        # Determine category based on extension
        category = get_category_for_file(item)
        dest_category_dir = os.path.join(target_folder, category)

        # Create category sub-folder if not existing
        try:
            os.makedirs(dest_category_dir, exist_ok=True)
        except OSError as e:
            error_msg = f"Could not create category folder '{dest_category_dir}': {e}"
            print(f"[ERROR] {error_msg}")
            summary["errors"].append(error_msg)
            continue

        # Generate unique destination path without overwriting
        dest_file_path, was_renamed = get_unique_destination_path(dest_category_dir, item)
        final_filename = os.path.basename(dest_file_path)

        # Move file safely
        try:
            shutil.move(item_path, dest_file_path)
            summary["files_moved"] += 1
            summary["category_counts"][category] = summary["category_counts"].get(category, 0) + 1

            if was_renamed:
                summary["files_renamed"] += 1
                print(f"[MOVED & RENAMED] '{item}' -> '{category}/{final_filename}' (name collision resolved)")
            else:
                print(f"[MOVED] '{item}' -> '{category}/{final_filename}'")

        except PermissionError as e:
            error_msg = f"Permission denied while moving '{item}': {e}"
            print(f"[ERROR] {error_msg}")
            summary["errors"].append(error_msg)
        except shutil.Error as e:
            error_msg = f"Shutil error moving '{item}': {e}"
            print(f"[ERROR] {error_msg}")
            summary["errors"].append(error_msg)
        except OSError as e:
            error_msg = f"OS error moving '{item}': {e}"
            print(f"[ERROR] {error_msg}")
            summary["errors"].append(error_msg)

    print_summary(summary)
    return summary


def print_summary(summary: Dict[str, any]) -> None:
    """
    Displays a structured and easy-to-read summary of the organization process.
    """
    print("\n" + "=" * 65)
    print("                ORGANIZATION SUMMARY REPORT")
    print("=" * 65)
    print(f"Target Directory:      {summary['target_folder']}")
    print(f"Total Items Scanned:   {summary['scanned_items']}")
    print(f"Sub-folders Skipped:   {summary['directories_skipped']}")
    if summary["protected_skipped"] > 0:
        print(f"Protected Files:       {summary['protected_skipped']}")
    print(f"Files Moved:           {summary['files_moved']}")
    print(f"Files Renamed (dup):   {summary['files_renamed']}")
    print(f"Errors Encountered:    {len(summary['errors'])}")
    print("-" * 65)

    if summary["category_counts"]:
        print("Breakdown by Category:")
        for category, count in sorted(summary["category_counts"].items()):
            print(f"  - {category:<15} : {count} file(s)")
    else:
        print("No files were moved.")

    if summary["errors"]:
        print("-" * 65)
        print("Error Details:")
        for err in summary["errors"]:
            print(f"  * {err}")

    print("=" * 65)
    print("Operation complete!\n")


def main() -> None:
    """
    Main entry point for the File Organizer CLI application.
    Prompts the user for target folder path and executes file organization.
    """
    print("=" * 65)
    print("        PYTHON FILE ORGANIZER APPLICATION (Project 4)")
    print("=" * 65)
    print("This utility organizes messy folders by sorting files into")
    print("sub-folders based on extension (PDF, Images, Documents, etc.).")
    print("=" * 65 + "\n")

    # Support optional command line argument: python file_organizer.py <target_path>
    if len(sys.argv) > 1:
        raw_path = sys.argv[1].strip()
        print(f"Folder path provided via arguments: {raw_path}")
    else:
        try:
            raw_path = input("Enter target folder path to organize (or 'q' to quit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            sys.exit(0)

    if raw_path.lower() in ("q", "quit", "exit", ""):
        print("Exiting application. No files were modified.")
        sys.exit(0)

    # Validate target directory
    is_safe, message_or_path = is_safe_target_directory(raw_path)
    if not is_safe:
        print(f"\n[VALIDATION ERROR] {message_or_path}")
        sys.exit(1)

    target_dir = message_or_path

    # User confirmation before proceeding
    print(f"\nTarget Folder: {target_dir}")
    try:
        confirm = input("Are you sure you want to organize this folder? (y/n): ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled by user.")
        sys.exit(0)

    if confirm not in ("y", "yes"):
        print("Organization cancelled. No files were modified.")
        sys.exit(0)

    organize_folder(target_dir)


if __name__ == "__main__":
    main()
