from datetime import datetime

import streamlit as st


def show():

    today = datetime.now().strftime("%d %b %Y")

    st.markdown(
        f"""
<div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #334155;padding:8px 0 12px 0;margin-bottom:12px;">

<div style="font-size:36px;font-weight:900;letter-spacing:.6px;color:#F8FAFC;">
EQMP COMMAND CENTER
</div>

<div style="text-align:right;">

<span style="display:inline-block;width:10px;height:10px;background:#22C55E;border-radius:50%;box-shadow:0 0 10px #22C55E;margin-right:6px;"></span>

<span style="color:#22C55E;font-weight:800;font-size:14px;">
LIVE
</span>

<br>

<span style="color:#CBD5E1;font-size:12px;">
{today}
</span>

</div>

</div>
""",
        unsafe_allow_html=True,
    )
