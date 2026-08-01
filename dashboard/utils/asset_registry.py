from pathlib import Path

from utils.framework_registry import FRAMEWORK_REGISTRY
from utils.research_notes import load_notes


KNOWLEDGE_ROOT = Path("knowledge")


def load_assets():
    """
    Unified registry for every EQMP knowledge asset.

    Every framework, research note, publication,
    case study and white paper will eventually
    be registered here.
    """

    assets = {}

    # =====================================================
    # Frameworks
    # =====================================================

    for title, framework in FRAMEWORK_REGISTRY.items():

        asset_id = framework["id"]

        # Example:
        # EQMP-GF-001
        # ->
        # knowledge/frameworks/GF-001.md

        framework_file = (
            asset_id.replace("EQMP-", "") + ".md"
        )

        assets[asset_id] = {

            "id": asset_id,

            "type": framework["type"],

            "title": title.replace(
                " (Coming Soon)",
                "",
            ),

            "description": "",

            "path": (
                KNOWLEDGE_ROOT
                / "frameworks"
                / framework_file
            ),

        }

    # =====================================================
    # Research Notes
    # =====================================================

    for note in load_notes():

        assets[note["asset_id"]] = {

            "id": note["asset_id"],

            "type": "Research Note",

            "title": note["title"],

            "description": note.get(
                "summary",
                "",
            ),

            "path": note["path"],

        }

    # =====================================================
    # Future Asset Types
    # =====================================================

    # Publications
    # White Papers
    # Case Studies
    # Architectures
    # Datasets

    return assets


def get_asset(asset_id: str):

    return load_assets().get(asset_id)


def get_assets_by_type(asset_type: str):

    return [

        asset

        for asset in load_assets().values()

        if asset["type"] == asset_type

    ]
