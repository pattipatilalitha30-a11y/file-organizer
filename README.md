# Project 4: Python File Organizer

An automated command-line utility built in Python that scans any target directory and organizes messy files into categorized sub-folders based on their file extensions.

---

## 📌 Project Description

Cluttered download folders, desktop directories, and unorganized storage spaces can make locating files difficult. The **Python File Organizer** solves this problem by automatically inspecting the extension of each file in a specified folder, creating designated category sub-folders (such as `PDF`, `Images`, `Documents`, `Videos`, `Audio`, `Code`, and `Others`), and moving files into their corresponding destinations safely.

The tool incorporates safety guardrails: it protects system roots and project source files, skips nested directories, safely handles files without extensions, and prevents data overwrites by automatically resolving duplicate filename collisions.

---

## 🚀 Features

- **Automated Extension Categorization**: Accurately maps file extensions to designated category sub-folders.
- **Overwriting Prevention & Safe Renaming**: If a file with the same name already exists in the destination folder, it automatically appends an incrementing numeric suffix (e.g., `document.pdf` -> `document_1.pdf`) to ensure zero data loss.
- **Handles Files Without Extension**: Safely routes extensionless files and unrecognized formats into the `Others/` sub-folder.
- **Directory Preservation**: Moves files only; existing sub-folders within the target directory are preserved and never relocated.
- **Safety Restrictions**:
  - Refuses to organize root drives (e.g., `C:\`, `/`).
  - Blocks accidental organization of the project's own source folder.
  - Skips protected project files (`file_organizer.py`, `README.md`, etc.).
- **User Confirmation Prompt**: Asks for explicit confirmation (`y/n`) before moving any files.
- **Detailed Operation Log & Summary**: Displays real-time file moves and outputs an end-of-run summary with item counts and category breakdowns.
- **Robust Error Handling**: Safely catches permission issues, invalid paths, and I/O exceptions without crashing.
- **Zero Third-Party Dependencies**: Uses 100% Python standard library (`os`, `shutil`, `sys`).

---

## 🛠 Technologies Used

- **Language**: Python 3.7+ (compatible with Python 3.10+)
- **Standard Library Modules**:
  - `os`: File path operations, directory scanning, and folder creation.
  - `shutil`: Safe, high-level file moving operations.
  - `sys`: Command-line arguments and process management.
  - `tempfile`: Isolated sandbox generation for automated testing.

---

## 📂 Folder Organization Rules

Files are organized according to the following category mapping:

| Category Folder | Target File Extensions |
| :--- | :--- |
| **PDF/** | `.pdf` |
| **Images/** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg`, `.tiff`, `.ico` |
| **Documents/** | `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.csv`, `.tsv` |
| **Videos/** | `.mp4`, `.mkv`, `.avi`, `.mov`, `.flv`, `.wmv`, `.webm`, `.m4v` |
| **Audio/** | `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.m4a`, `.wma` |
| **Code/** | `.py`, `.js`, `.java`, `.c`, `.cpp`, `.cs`, `.html`, `.css`, `.json`, `.xml`, `.sh`, `.ts`, `.php`, `.rb`, `.sql`, `.go`, `.rs` |
| **Others/** | Any unmapped extension (e.g., `.zip`, `.iso`, `.xyz`) and files without any extension (e.g., `LICENSE`, `data`) |

---

## 💻 Installation

1. **Prerequisites**: Ensure Python 3.7 or newer is installed on your computer.
   To check your Python version, run:
   ```bash
   python --version
   ```

2. **Clone / Download the Repository**:
   ```bash
   git clone <your-repository-url>
   cd "file organizer"
   ```

3. **No External Packages Required**:
   This project relies solely on the Python Standard Library. No `pip install` commands are needed.

---

## 🏃 How to Run

### Interactive Mode (Recommended)
Run the script directly. You will be prompted to enter the target folder path:

```bash
python file_organizer.py
```

### Direct Argument Mode
You can also pass the folder path directly as a command-line argument:

```bash
python file_organizer.py "C:\path\to\target_folder"
```

---

## 📋 Example Input & Output

### 1. Before Organization (Input Directory)
```text
C:\SampleFolder\
├── annual_report.pdf
├── photo.jpg
├── screenshot.png
├── notes.docx
├── script.py
├── demo.mp4
├── song.mp3
├── data_file (no extension)
└── pre_existing_folder/
```

### 2. Execution Log
```text
=================================================================
        PYTHON FILE ORGANIZER APPLICATION (Project 4)
=================================================================
This utility organizes messy folders by sorting files into
sub-folders based on extension (PDF, Images, Documents, etc.).
=================================================================

Enter target folder path to organize (or 'q' to quit): C:\SampleFolder

Target Folder: C:\SampleFolder
Are you sure you want to organize this folder? (y/n): y

=================================================================
  Starting File Organization on:
  C:\SampleFolder
=================================================================
[MOVED] 'annual_report.pdf' -> 'PDF/annual_report.pdf'
[MOVED] 'photo.jpg' -> 'Images/photo.jpg'
[MOVED] 'screenshot.png' -> 'Images/screenshot.png'
[MOVED] 'notes.docx' -> 'Documents/notes.docx'
[MOVED] 'script.py' -> 'Code/script.py'
[MOVED] 'demo.mp4' -> 'Videos/demo.mp4'
[MOVED] 'song.mp3' -> 'Audio/song.mp3'
[MOVED] 'data_file' -> 'Others/data_file'

=================================================================
                ORGANIZATION SUMMARY REPORT
=================================================================
Target Directory:      C:\SampleFolder
Total Items Scanned:   9
Sub-folders Skipped:   1
Files Moved:           8
Files Renamed (dup):   0
Errors Encountered:    0
-----------------------------------------------------------------
Breakdown by Category:
  - Audio           : 1 file(s)
  - Code            : 1 file(s)
  - Documents       : 1 file(s)
  - Images          : 2 file(s)
  - Others          : 1 file(s)
  - PDF             : 1 file(s)
  - Videos          : 1 file(s)
=================================================================
Operation complete!
```

### 3. After Organization (Output Directory)
```text
C:\SampleFolder\
├── Audio/
│   └── song.mp3
├── Code/
│   └── script.py
├── Documents/
│   └── notes.docx
├── Images/
│   ├── photo.jpg
│   └── screenshot.png
├── Others/
│   └── data_file
├── PDF/
│   └── annual_report.pdf
├── Videos/
│   └── demo.mp4
└── pre_existing_folder/
```

---

## 🧪 Testing Instructions

The project comes with an automated integration test script (`test_organizer.py`) that uses a temporary sandbox directory without altering your personal files.

To run the test suite:
```bash
python test_organizer.py
```

The test suite automatically tests and asserts:
1. **Extension Mapping**: Verifies that 17+ extension types map to the proper categories.
2. **File Relocation**: Verifies files are correctly moved into corresponding category folders.
3. **Collision Handling**: Tests if a duplicate filename generates a safe incremented filename (e.g., `document1_1.pdf`) without overwriting.
4. **Data Integrity**: Checks file sizes and content before and after moves to ensure zero data loss.
5. **Sub-folder Protection**: Verifies existing directories are not moved or modified.
6. **Automatic Cleanup**: Deletes the temporary sandbox once testing is complete.

---

## 🔒 Safety Notes

- **No Deletion**: The script only executes `move` operations. No files are ever deleted.
- **No Overwriting**: If a target file already exists in the destination category, the incoming file is automatically renamed with a numeric suffix (`_1`, `_2`, etc.).
- **Self-Protection**: The organizer detects and prevents running directly against the project source code directory.
- **Root Protection**: Restricts root drives like `C:\` or `/` from being inadvertently reorganized.
- **User Confirmation**: Requires confirmation before taking action.
