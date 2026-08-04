import streamlit as st

from content.assessment import STEPS


def _status(step_id, current):

    if step_id < current:
        return "✓", "#18A558"

    if step_id == current:
        return str(step_id), "#2F81F7"

    return str(step_id), "#4A5568"


def show(current_step):

    st.markdown(
        """
<div style="margin-bottom:10px;">
<h3 style="margin-bottom:4px;color:white;">
Assessment Journey
</h3>

<div style="color:#9FB3C8;font-size:15px;">
Complete the four stages to configure your
enterprise post-quantum readiness assessment.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    cols = st.columns(len(STEPS))

    for col, step in zip(cols, STEPS):

        icon, colour = _status(step["id"], current_step)

        with col:

            st.markdown(
                f"""
<div style="text-align:center;">

<div style="
width:42px;
height:42px;
margin:auto;
border-radius:50%;
background:{colour};
display:flex;
align-items:center;
justify-content:center;
font-weight:700;
color:white;
font-size:18px;
">

{icon}

</div>

<div style="
margin-top:12px;
font-weight:600;
color:white;
font-size:16px;
">

{step["title"]}

</div>

<div style="
margin-top:4px;
font-size:13px;
color:#93A4B7;
">

{step["description"]}

</div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)

    st.divider()
