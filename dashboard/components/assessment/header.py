import streamlit as st

from content.assessment import STEPS


def show(current_step=1):

    current = next(
        (
            step
            for step in STEPS
            if step["id"] == current_step
        ),
        STEPS[0],
    )

    st.markdown(
        f"""
<div style="
margin-bottom:14px;
">

<div style="
display:flex;
align-items:baseline;
gap:12px;
margin-bottom:5px;
">

<span style="
font-size:1.85rem;
font-weight:750;
color:#F5F7FA;
letter-spacing:-0.02em;
">
Enterprise Quantum Readiness Assessment
</span>

<span style="
font-size:0.82rem;
color:#7F91A6;
">
4–6 min
</span>

</div>

<div style="
font-size:0.98rem;
line-height:1.4;
color:#AEBCCE;
margin-bottom:12px;
">
Establish your organisation's current quantum-readiness posture.
</div>

<div style="
font-size:0.86rem;
line-height:1.4;
color:#AEB8C6;
">

<span style="
color:#2F81F7;
font-weight:700;
">
Stage {current_step} of {len(STEPS)}
</span>

<span style="margin:0 8px;color:#536273;">
·
</span>

<span style="font-weight:600;color:#D5DCE5;">
{current["title"]}
</span>

<span style="margin:0 8px;color:#536273;">
·
</span>

<span>
{current["description"]}
</span>

</div>

</div>
""",
        unsafe_allow_html=True,
    )
