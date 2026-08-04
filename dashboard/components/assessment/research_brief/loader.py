from pathlib import Path


BASE_PATH = Path(__file__).resolve().parents[3] / "content" / "research_briefs"


def load_markdown(filename):

    path = BASE_PATH / filename

    if not path.exists():

        return "Research brief unavailable."

    return path.read_text(encoding="utf-8").strip()
