from pathlib import Path


data_dir = Path("Practice6/file_handling/data")
data_dir.mkdir(parents=True, exist_ok=True)

file_path = data_dir / "sample.txt"

with open(file_path, "w", encoding="utf-8") as file:
    file.write("First line\n")
    file.write("Second line\n")
    file.write("Third line\n")

print(f"File created and written successfully: {file_path}")

with open(file_path, "a", encoding="utf-8") as file:
    file.write("Fourth line (appended)\n")
    file.write("Fifth line (appended)\n")

print("New lines appended successfully.")

print("\nCurrent file content:")
with open(file_path, "r", encoding="utf-8") as file:
    print(file.read())