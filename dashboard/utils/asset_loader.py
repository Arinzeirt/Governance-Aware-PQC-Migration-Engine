from pathlib import Path

import yaml

from utils.asset_registry import get_asset


def split_front_matter(text: str):
    """
    Split a Markdown document into YAML metadata
    and Markdown content.
    """

    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)

    if len(parts) < 3:
        return {}, text

    metadata = yaml.safe_load(parts[1]) or {}

    content = parts[2].lstrip()

    return metadata, content


def strip_first_heading(markdown: str):

    lines = markdown.splitlines()

    found = False

    output = []

    for line in lines:

        if not found and line.startswith("# "):
            found = True
            continue

        output.append(line)

    return "\n".join(output).lstrip()


def load_asset(asset_id: str):

    asset = get_asset(asset_id)

    if asset is None:
        return None

    path = Path(asset["path"])

    if not path.exists():

        asset["metadata"] = {}

        asset["content"] = (
            "## Coming Soon\n\n"
            "This research asset has not yet been published."
        )

        return asset

    raw = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    metadata, markdown = split_front_matter(raw)

    asset["metadata"] = metadata

    asset["content"] = strip_first_heading(markdown)

    return asset
