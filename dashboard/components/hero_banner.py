import streamlit as st


def show(
    eyebrow: str,
    title: str,
    description: str,
    metadata: list[str],
):

    metadata_html = "<br>".join(metadata)

    st.markdown(
        f"""
<div style="
background:#111827;
border:1px solid #334155;
border-radius:16px;
padding:32px;
margin-bottom:28px;
">

<div style="
font-size:13px;
font-weight:700;
letter-spacing:1px;
text-transform:uppercase;
color:#60A5FA;
margin-bottom:10px;
">
{eyebrow}
</div>

<div style="
font-size:34px;
font-weight:700;
line-height:1.25;
color:white;
margin-bottom:18px;
">
{title}
</div>

<div style="
font-size:16px;
line-height:1.7;
color:#CBD5E1;
margin-bottom:24px;
">
{description}
</div>

<div style="
font-size:14px;
line-height:1.8;
color:#94A3B8;
">
{metadata_html}
</div>

</div>
""",
        unsafe_allow_html=True,
    )
