import streamlit as st


def finding(title, body, colour, divider=True):

    st.markdown(
        f"""
<div style="display:flex;align-items:flex-start;">

<div style="
width:10px;
height:10px;
border-radius:50%;
background:{colour};
margin-top:8px;
margin-right:14px;
flex-shrink:0;
"></div>

<div style="width:100%;">

<div style="
font-size:16px;
font-weight:700;
color:#F8FAFC;
margin-bottom:6px;
">
{title}
</div>

<div style="
font-size:14px;
line-height:1.75;
color:#CBD5E1;
">
{body}
</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    if divider:

        st.markdown(
            """
<hr style="
border:none;
border-top:1px solid #263244;
margin:18px 0;
">
""",
            unsafe_allow_html=True,
        )


def show():

    st.markdown(
        """
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:22px;
margin-bottom:20px;
">

<div style="
font-size:22px;
font-weight:700;
color:#F8FAFC;
margin-bottom:20px;
">

Enterprise Findings

</div>
""",
        unsafe_allow_html=True,
    )

    finding(
        "Critical Exposure",
        "Traditional public-key cryptography remains in active use across business-critical services.",
        "#DC2626",
    )

    finding(
        "Governance Impact",
        "Current cryptographic dependencies increase migration complexity and require executive planning.",
        "#F59E0B",
    )

    finding(
        "Immediate Priority",
        "Establish a cryptographic inventory baseline and begin phased migration planning for externally exposed systems.",
        "#2563EB",
        divider=False,
    )

    st.markdown("</div>", unsafe_allow_html=True)
