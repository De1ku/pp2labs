from pathlib import Path
import shutil

source_file = Path("Practice6/file_handling/data/sample.txt")
backup_dir = Path("Practice6/file_handling/backup")
backup_dir.mkdir(parents=True, exist_ok=True)

backup_file = backup_dir / "sample_backup.txt"
copied_file = backup_dir / "sample_copy.txt"

if source_file.exists():
    shutil.copy(source_file, copied_file)
    print(f"Copied file to: {copied_file}")

    shutil.copy2(source_file, backup_file)
    print(f"Backup created at: {backup_file}")
else:
    print(f"Source file not found: {source_file}")

file_to_delete = copied_file

if file_to_delete.exists() and file_to_delete.is_file():
    file_to_delete.unlink()
    print(f"Deleted file safely: {file_to_delete}")
else:
    print(f"File not found or not a regular file: {file_to_delete}")