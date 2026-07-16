from pathlib import Path


def validate_environment(target):

    target_path = Path(target).expanduser()

    result = {
        "valid": False,
        "target": str(target_path),
        "exists": False,
        "is_directory": False,
        "file_count": 0,
        "git_repository": False,
        "languages": [],
        "estimated_size_mb": 0.0,
    }

    if not target_path.exists():
        return result

    result["exists"] = True

    if not target_path.is_dir():
        return result

    result["is_directory"] = True

    files = [f for f in target_path.rglob("*") if f.is_file()]

    result["file_count"] = len(files)

    result["git_repository"] = (target_path / ".git").exists()

    extensions = set()

    total_size = 0

    for file in files:

        total_size += file.stat().st_size

        if file.suffix:
            extensions.add(file.suffix.lower())

    language_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".java": "Java",
        ".cs": "C#",
        ".go": "Go",
        ".php": "PHP",
        ".cpp": "C++",
        ".c": "C",
        ".rs": "Rust",
    }

    result["languages"] = sorted(
        {
            language_map[ext]
            for ext in extensions
            if ext in language_map
        }
    )

    result["estimated_size_mb"] = round(
        total_size / (1024 * 1024),
        2,
    )

    result["valid"] = True

    return result
