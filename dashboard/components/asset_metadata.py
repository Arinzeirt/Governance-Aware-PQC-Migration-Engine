import streamlit as st


def _format_value(value):

    if value is None:
        return "—"

    if isinstance(value, list):
        return ", ".join(str(v) for v in value)

    if value == "":
        return "—"

    return str(value)


def show(metadata: dict):

    if not metadata:
        return

    st.markdown(
        """
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:22px;
margin-top:10px;
margin-bottom:24px;
">
""",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:

        st.markdown(
            f"**Version**  \n{_format_value(metadata.get('version'))}"
        )

        st.markdown(
            f"**Status**  \n{_format_value(metadata.get('status'))}"
        )

        st.markdown(
            f"**Author**  \n{_format_value(metadata.get('author'))}"
        )

        st.markdown(
            f"**Institution**  \n{_format_value(metadata.get('institution'))}"
        )

    with right:

        st.markdown(
            f"**Research Area**  \n{_format_value(metadata.get('research_area'))}"
        )

        st.markdown(
            f"**Keywords**  \n{_format_value(metadata.get('keywords'))}"
        )

        st.markdown(
            f"**Last Updated**  \n{_format_value(metadata.get('last_updated'))}"
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )
