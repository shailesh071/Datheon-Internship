
import os
import shutil
import logging
from pathlib import Path


# File extensions and their destination folders
FILE_TYPES = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".csv": "Documents",
    ".xlsx": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".svg": "Images",
    ".webp": "Images",

    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",

    # Code files
    ".py": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".c": "Code"
}


def setup_logging():
    logging.basicConfig(
        filename="organizer.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def get_unique_path(destination):
    if not destination.exists():
        return destination

    folder = destination.parent
    name = destination.stem
    extension = destination.suffix
    counter = 1

    while True:
        new_destination = folder / f"{name}_{counter}{extension}"

        if not new_destination.exists():
            return new_destination

        counter += 1


def organize_files(directory):

    source_folder = Path(directory).expanduser().resolve()

    if not source_folder.exists():
        print("Error: The directory does not exist.")
        logging.error("Directory does not exist: %s", source_folder)
        return

    if not source_folder.is_dir():
        print("Error: The provided path is not a directory.")
        logging.error("Path is not a directory: %s", source_folder)
        return

    moved = 0
    skipped = 0
    failed = 0

    print("\nStarting file organization...\n")

    try:
        entries = list(os.scandir(source_folder))
    except PermissionError:
        print("Error: Permission denied while accessing the directory.")
        logging.error("Permission denied: %s", source_folder)
        return
    except OSError as error:
        print(f"Error accessing directory: {error}")
        logging.error("Directory access error: %s", error)
        return

    for entry in entries:

        # Skip directories and symbolic links
        if entry.is_dir(follow_symlinks=False):
            skipped += 1
            continue

        if entry.is_symlink():
            print(f"Skipped symbolic link: {entry.name}")
            logging.warning("Skipped symbolic link: %s", entry.path)
            skipped += 1
            continue

        if not entry.is_file(follow_symlinks=False):
            skipped += 1
            continue

        source_file = Path(entry.path)

        # Avoid moving the running Python script or log file
        if source_file.resolve() == Path(__file__).resolve():
            skipped += 1
            continue

        if source_file.name == "organizer.log":
            skipped += 1
            continue

        # Find the destination folder
        extension = source_file.suffix.lower()
        category = FILE_TYPES.get(extension, "Others")

        destination_folder = source_folder / category

        try:
            # Create destination folder if it does not exist
            destination_folder.mkdir(exist_ok=True)

            destination_file = get_unique_path(
                destination_folder / source_file.name
            )

            # Move the file
            shutil.move(str(source_file), str(destination_file))

            print(f"Moved: {source_file.name} -> {category}/")
            logging.info(
                "Moved %s to %s",
                source_file,
                destination_file
            )

            moved += 1

        except PermissionError:
            print(f"Permission denied: {source_file.name}")
            logging.error("Permission denied: %s", source_file)
            failed += 1

        except OSError as error:
            print(f"Could not move {source_file.name}: {error}")
            logging.error(
                "Failed to move %s: %s",
                source_file,
                error
            )
            failed += 1

    # Display final summary
    print("\n========== ORGANIZATION SUMMARY ==========")
    print(f"Files moved successfully : {moved}")
    print(f"Files skipped            : {skipped}")
    print(f"Files failed             : {failed}")
    print("==========================================")

    logging.info(
        "Organization completed. Moved: %d, Skipped: %d, Failed: %d",
        moved,
        skipped,
        failed
    )


def main():
    setup_logging()

    print("======================================")
    print("   AUTOMATED FILE ORGANIZER")
    print("======================================")

    directory = input(
        "\nEnter the directory path to organize: "
    ).strip().strip('"').strip("'")

    if not directory:
        print("Error: Directory path cannot be empty.")
        return

    print(f"\nSelected directory: {directory}")

    confirmation = input(
        "Do you want to organize these files? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        organize_files(directory)
    else:
        print("Organization cancelled.")
        logging.info("User cancelled file organization.")


if __name__ == "__main__":
    main()
