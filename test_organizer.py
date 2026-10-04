"""
Test Suite for File Organizer
=============================
Creates a temporary sandbox environment with representative sample files,
runs the file organizer, and asserts that all files are categorized correctly,
name collisions are safely handled without data loss, and directories are preserved.
"""

import os
import shutil
import tempfile
from file_organizer import organize_folder, get_category_for_file


def run_tests():
    print("=" * 65)
    print("   RUNNING AUTOMATED UNIT & INTEGRATION TESTS")
    print("=" * 65)

    # 1. Test Category Mapping Logic
    print("\n[TEST 1] Testing Category Mapping Logic...")
    test_cases = [
        ("report.pdf", "PDF"),
        ("photo.jpg", "Images"),
        ("picture.jpeg", "Images"),
        ("icon.png", "Images"),
        ("resume.doc", "Documents"),
        ("notes.docx", "Documents"),
        ("clip.mp4", "Videos"),
        ("movie.mkv", "Videos"),
        ("song.mp3", "Audio"),
        ("podcast.wav", "Audio"),
        ("script.py", "Code"),
        ("app.js", "Code"),
        ("Main.java", "Code"),
        ("archive.zip", "Others"),
        ("random.xyz123", "Others"),
        ("NO_EXTENSION_FILE", "Others"),
        (".hidden_no_ext", "Others"),
    ]

    for filename, expected in test_cases:
        actual = get_category_for_file(filename)
        assert actual == expected, f"Failed for '{filename}': expected '{expected}', got '{actual}'"
    print("  -> Passed all 17 category mapping assertions.")

    # 2. Integration Test with Temporary Folder
    print("\n[TEST 2] Running Integration Test with Temporary Sandbox Folder...")
    temp_dir = tempfile.mkdtemp(prefix="file_organizer_test_")
    print(f"  Created temporary test directory: {temp_dir}")

    try:
        # Define files to create
        sample_files = {
            "document1.pdf": "Sample PDF content 1",
            "document2.pdf": "Sample PDF content 2",
            "vacation.jpg": "Fake image content jpg",
            "profile.png": "Fake image content png",
            "resume.docx": "Fake word doc content",
            "notes.doc": "Fake old word doc content",
            "tutorial.mp4": "Fake video content",
            "film.mkv": "Fake mkv content",
            "track.mp3": "Fake audio content mp3",
            "sound.wav": "Fake audio content wav",
            "main.py": "print('hello python')",
            "index.js": "console.log('hello js')",
            "App.java": "public class App {}",
            "data.unknown": "Unknown extension content",
            "FILE_WITHOUT_EXT": "Raw file with no extension",
        }

        # Create files
        for fname, content in sample_files.items():
            with open(os.path.join(temp_dir, fname), "w", encoding="utf-8") as f:
                f.write(content)

        # Create a pre-existing subfolder to ensure directories are NOT moved
        dummy_subdir = os.path.join(temp_dir, "ExistingSubFolder")
        os.makedirs(dummy_subdir)
        with open(os.path.join(dummy_subdir, "internal.txt"), "w") as f:
            f.write("inner file")

        # Test duplicate collision prevention:
        # Pre-create 'PDF' folder with 'document1.pdf' containing existing content
        pre_existing_pdf_dir = os.path.join(temp_dir, "PDF")
        os.makedirs(pre_existing_pdf_dir)
        pre_existing_pdf_file = os.path.join(pre_existing_pdf_dir, "document1.pdf")
        with open(pre_existing_pdf_file, "w", encoding="utf-8") as f:
            f.write("Pre-existing document 1")

        print("  Sample files and pre-existing subfolders initialized successfully.")

        # Run organizer
        summary = organize_folder(temp_dir)

        # Verify summary stats
        assert summary["files_moved"] == len(sample_files), (
            f"Expected {len(sample_files)} files moved, got {summary['files_moved']}"
        )
        assert summary["files_renamed"] == 1, (
            f"Expected 1 collision rename for document1.pdf, got {summary['files_renamed']}"
        )
        assert len(summary["errors"]) == 0, f"Expected 0 errors, got {len(summary['errors'])}"

        # Verify destination files
        expected_destinations = {
            "PDF": ["document1.pdf", "document1_1.pdf", "document2.pdf"],
            "Images": ["vacation.jpg", "profile.png"],
            "Documents": ["resume.docx", "notes.doc"],
            "Videos": ["tutorial.mp4", "film.mkv"],
            "Audio": ["track.mp3", "sound.wav"],
            "Code": ["main.py", "index.js", "App.java"],
            "Others": ["data.unknown", "FILE_WITHOUT_EXT"],
        }

        for category, expected_files in expected_destinations.items():
            cat_dir = os.path.join(temp_dir, category)
            assert os.path.isdir(cat_dir), f"Category folder '{category}' was not created!"
            actual_files = sorted(os.listdir(cat_dir))
            for ef in expected_files:
                assert ef in actual_files, f"Expected '{ef}' in '{category}/', but found: {actual_files}"
                # Verify file content is intact (no corruption / no accidental empty files)
                fpath = os.path.join(cat_dir, ef)
                assert os.path.getsize(fpath) > 0, f"File '{fpath}' is empty!"

        # Verify collision didn't overwrite pre-existing file:
        with open(os.path.join(temp_dir, "PDF", "document1.pdf"), "r", encoding="utf-8") as f:
            original_content = f.read()
        assert original_content == "Pre-existing document 1", "Collision check failed: original file was overwritten!"

        with open(os.path.join(temp_dir, "PDF", "document1_1.pdf"), "r", encoding="utf-8") as f:
            renamed_content = f.read()
        assert renamed_content == "Sample PDF content 1", "Collision check failed: renamed file content mismatch!"

        # Verify that pre-existing subfolder was NOT moved or deleted
        assert os.path.isdir(dummy_subdir), "Existing subfolder was removed or moved!"
        assert os.path.isfile(os.path.join(dummy_subdir, "internal.txt")), "Internal subfolder file was lost!"

        print("  -> Passed all integration assertions cleanly!")
        print("\n[SUCCESS] ALL TESTS COMPLETED SUCCESSFULLY!")

    finally:
        # Clean up sandbox
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"  Cleaned up sandbox folder: {temp_dir}")


if __name__ == "__main__":
    run_tests()
