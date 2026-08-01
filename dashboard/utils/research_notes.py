from pathlib import Path


NOTES_DIR = Path("research-notes")


def extract_title(path: Path):

    for line in path.read_text(
        encoding="utf-8",
        errors="ignore",
    ).splitlines():

        line = line.strip()

        if line.startswith("#"):

            heading = line.lstrip("#").strip()

            if heading.lower().startswith("research notes series"):
                continue

            return heading

    return path.stem


def extract_summary(path: Path):

    text = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]

    for paragraph in paragraphs:

        if paragraph.startswith("#"):
            continue

        return paragraph.replace("\n", " ")

    return ""


def load_notes():

    notes = []

    if not NOTES_DIR.exists():
        return notes

    for path in sorted(
        NOTES_DIR.glob("[0-9][0-9][0-9]-*.md")
    ):

        note_id = path.stem.split("-")[0]

        notes.append(
            {
                "id": note_id,
                "asset_id": f"EQMP-RN-{note_id}",
                "title": extract_title(path),
                "summary": extract_summary(path),
                "path": path,
            }
        )

    return notes


def get_note(note_id):

    for note in load_notes():

        if note["id"] == note_id:
            return note

    return None
