import streamlit as st


def show(brief):

    with st.container(border=True):

        st.caption(
            f"◈ {brief.category.upper()}"
        )

        st.markdown(
            f"""
<div style="
font-size:1.45rem;
font-weight:800;
line-height:1.05;
margin:2px 0 8px 0;
">
{brief.headline.replace(chr(10), "<br>")}
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
<div style="
font-size:0.86rem;
line-height:1.45;
color:#BFC8D6;
max-width:900px;
margin-bottom:8px;
">
{brief.message}
</div>
""",
            unsafe_allow_html=True,
        )

        st.caption(
            f"📖 Research Brief  ·  {brief.reading_time}"
        )
