import streamlit as st


PAGES = [
    ("Dashboard", "dashboard"),
    ("Enterprise Discovery", "assessment"),
    ("Migration", "repository"),
    ("Research Centre", "research"),
    ("About", "about"),
]


def show():

    cols = st.columns(len(PAGES))

    current = st.session_state.get(
        "page",
        "dashboard",
    )

    for col, (title, page) in zip(cols, PAGES):

        with col:

            if current == page:

                st.markdown(
                    f"""
<div style="
text-align:center;
font-weight:700;
color:#2563EB;
padding-bottom:8px;
border-bottom:3px solid #2563EB;
font-size:15px;
">
{title}
</div>
""",
                    unsafe_allow_html=True,
                )

            else:

                if st.button(
                    title,
                    key=f"topnav_{page}",
                    use_container_width=True,
                ):

                    st.session_state.page = page
                    st.rerun()

    st.divider()
