import streamlit as st

from utils.asset_registry import get_asset
from utils.asset_router import open_asset
from utils.research_notes import load_notes


def _automatic_related(asset_id: str):

    if not asset_id.startswith("EQMP-RN-"):
        return []

    notes = sorted(
        load_notes(),
        key=lambda n: int(n["id"])
    )

    index = next(
        (
            i for i, note in enumerate(notes)
            if note["asset_id"] == asset_id
        ),
        None,
    )

    if index is None:
        return []

    related = []

    for offset in (-1, 1, -2):

        i = index + offset

        if 0 <= i < len(notes):
            related.append(notes[i]["asset_id"])

    return related


def show(asset):

    metadata = asset.get("metadata", {})

    related = metadata.get("related", [])

    if not related:
        related = _automatic_related(asset["id"])

    if not related:
        return

    st.subheader("Continue Reading")

    st.caption(
        "Explore additional research notes and knowledge assets from the Enterprise Quantum Migration Platform."
    )

    cols = st.columns(3)

    for index, asset_id in enumerate(related):

        item = get_asset(asset_id)

        if item is None:
            continue

        with cols[index]:

            with st.container(border=True):

                st.caption(
                    f"{item['type']} • {item['id']}"
                )

                st.markdown(
                    f"""
<div style="
height:110px;
font-size:18px;
font-weight:700;
line-height:1.45;
overflow:hidden;
margin-bottom:20px;
">
{item['title']}
</div>
""",
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Continue Reading →",
                    key=f"related_{asset_id}",
                    use_container_width=True,
                ):
                    open_asset(asset_id)

