from pathlib import Path

file_path = Path("Practice6/file_handling/data/sample.txt")

if file_path.exists():
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    print("File content:")
    print(content)
else:
    print(f"File does not exist: {file_path}")