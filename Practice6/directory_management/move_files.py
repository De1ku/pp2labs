from pathlib import Path
import shutil

source_dir = Path("Practice6/directory_management/source")
destination_dir = Path("Practice6/directory_management/destination")

source_dir.mkdir(parents=True, exist_ok=True)
destination_dir.mkdir(parents=True, exist_ok=True)

file1 = source_dir / "example1.txt"
file2 = source_dir / "example2.txt"

file1.write_text("first file", encoding="utf-8")
file2.write_text("second file", encoding="utf-8")

copied_file = destination_dir / "example1_copy.txt"
shutil.copy(file1, copied_file)
print(f"Copied {file1} to {copied_file}")

moved_file = destination_dir / "example2_moved.txt"
shutil.move(str(file2), str(moved_file))
print(f"Moved {file2} to {moved_file}")

print("\nSource directory contents:")
for item in source_dir.iterdir():
    print(item)

print("\nDestination directory contents:")
for item in destination_dir.iterdir():
    print(item)