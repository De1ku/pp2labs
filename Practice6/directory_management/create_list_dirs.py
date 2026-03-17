from pathlib import Path

base_dir = Path("Practice6/directory_management/workspace")
nested_dir = base_dir / "projects" / "python" / "lesson6"

nested_dir.mkdir(parents=True, exist_ok=True)
print(f"Nested directories created: {nested_dir}")

(base_dir / "notes.txt").write_text("i want to play marathon", encoding="utf-8")
(base_dir / "report.pdf").write_text("Fake PDF content", encoding="utf-8")
(nested_dir / "script.py").write_text("print('halo amigo')", encoding="utf-8")
(nested_dir / "data.csv").write_text("id,name\n1,Alice\n2,Bob", encoding="utf-8")

print("\nContents of workspace:")
for item in base_dir.rglob("*"):
    if item.is_dir():
        print(f"[DIR]  {item}")
    else:
        print(f"[FILE] {item}")

extension = ".py"
print(f"\nFiles with extension {extension}:")
for file in base_dir.rglob(f"*{extension}"):
    print(file)