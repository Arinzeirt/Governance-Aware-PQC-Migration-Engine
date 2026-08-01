import streamlit as st


def show(*items):
    """
    Display a simple breadcrumb navigation.

    Example:
        show(
            "Research Centre",
            "Frameworks",
            "EQMP-GF-001",
        )
    """

    breadcrumb = "  /  ".join(items)

    st.markdown(
        f"""
<div style="
margin-top:10px;
margin-bottom:18px;
font-size:14px;
color:#94A3B8;
">
{breadcrumb}
</div>
""",
        unsafe_allow_html=True,
    )
