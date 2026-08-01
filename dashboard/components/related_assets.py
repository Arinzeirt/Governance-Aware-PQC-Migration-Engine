import streamlit as st

from utils.asset_registry import get_asset
from utils.asset_router import open_asset


def show(metadata: dict):

    related = metadata.get("related", [])

    if not related:
        return

    st.subheader("Related Research")

    cols = st.columns(2)

    for index, asset_id in enumerate(related):

        asset = get_asset(asset_id)

        if asset is None:
            continue

        with cols[index % 2]:

            with st.container(border=True):

                st.caption(
                    f"{asset['type']} • {asset['id']}"
                )

                st.markdown(
                    f"**{asset['title']}**"
                )

                if st.button(
                    "Open",
                    key=f"related_{asset_id}",
                    use_container_width=True,
                ):
                    open_asset(asset_id)
