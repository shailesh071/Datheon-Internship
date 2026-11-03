# Automated File Organizer & Cleanup Utility

<div align="center">

  <h2>Automated File Organizer & Cleanup Utility</h2>
  <p>A Python-based tool to automatically organize files into folders based on their extensions.</p>

</div>

## About

The Automated File Organizer & Cleanup Utility is a Python-based program that automatically organizes files into separate folders based on their file extensions. It helps keep directories clean and organized by sorting documents, images, videos, archives, and code files into their respective folders.

The program also handles duplicate filenames, manages permission errors, and records file operations in a log file.

## Features

- Automatically organizes files based on their extensions.
- Creates folders such as Documents, Images, Videos, Archives, Code, and Others.
- Moves files into their appropriate folders using the `shutil` module.
- Prevents filename conflicts by generating unique filenames.
- Handles permission errors and other file operation errors.
- Skips directories and symbolic links.
- Maintains an activity log in `organizer.log`.
- Displays a summary of moved, skipped, and failed files.

## Technologies Used

- **Python 3**: Main programming language.
- **OS Module**: Used to access and inspect directory contents.
- **Shutil Module**: Used to move files between folders.
- **Pathlib Module**: Used to manage file and directory paths.
- **Logging Module**: Used to record file operations and errors.