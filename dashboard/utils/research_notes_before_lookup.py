from pathlib import Path

NOTES_DIR = Path("research-notes")


def extract_title(file: Path) -> str:
    """
    Return the first meaningful Markdown title.

    If the document begins with
    '# Research Notes Series XXX',
    use the next level-1 heading instead.
    """

    headings = []

    try:
        for line in file.read_text(encoding="utf-8").splitlines():

            line = line.strip()

            if line.startswith("# "):
                headings.append(line[2:].strip())

    except Exception:
        pass

    for heading in headings:

        if not heading.lower().startswith("research notes series"):
            return heading

    if headings:
        return headings[0]

    title = file.stem
    _, slug = title.split("-", 1)
    return slug.replace("-", " ").title()


def extract_summary(file: Path) -> str:
    """
    Return the first paragraph after the title.
    """

    try:
        lines = file.read_text(encoding="utf-8").splitlines()

        body = []

        started = False

        for line in lines:

            text = line.strip()

            if text.startswith("# "):
                if started:
                    continue
                started = True
                continue

            if not started:
                continue

            if text.startswith("##"):
                continue

            if not text:
                if body:
                    break
                continue

            body.append(text)

        return " ".join(body[:4])

    except Exception:
        return ""



def load_notes():

    notes = []

    if not NOTES_DIR.exists():
        return notes

    for file in sorted(NOTES_DIR.glob("[0-9][0-9][0-9]-*.md")):

        number = file.stem.split("-", 1)[0]

        notes.append(
            {
                "id": number,
                "title": extract_title(file),
                "summary": extract_summary(file),
                "path": file,
            }
        )

    return notes
