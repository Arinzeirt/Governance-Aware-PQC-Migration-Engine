import streamlit as st

from engine.session import session


STAGES = [
    "INITIALIZING",
    "TARGET",
    "DISCOVERY",
    "INVENTORY",
    "REPORT",
    "COMPLETED",
]


LABELS = {
    "INITIALIZING": "Initialize",
    "TARGET": "Target",
    "DISCOVERY": "Discovery",
    "INVENTORY": "Inventory",
    "REPORT": "Report",
    "COMPLETED": "Complete",
}


def colour(index, current):

    if index < current:
        return "#16A34A"

    if index == current:
        return "#2563EB"

    return "#CBD5E1"


def show():

    current = -1

    if session.state in STAGES:

        current = STAGES.index(session.state)

    html = """
<div style="
display:flex;
align-items:center;
justify-content:center;
margin:20px 0;
">
"""

    for index, stage in enumerate(STAGES):

        c = colour(index, current)

        html += f"""
<div style="
display:flex;
align-items:center;
">

<div style="
width:24px;
height:24px;
border-radius:50%;
background:{c};
display:flex;
justify-content:center;
align-items:center;
color:white;
font-size:12px;
font-weight:bold;
">

✓

</div>
"""

        if index != len(STAGES)-1:

            html += f"""
<div style="
width:70px;
height:4px;
background:{c};
">
</div>
"""

        html += "</div>"

    html += "</div>"

    #
    # Labels
    #

    html += """
<div style="
display:flex;
justify-content:space-between;
font-size:12px;
font-weight:600;
margin-top:-10px;
">
"""

    for stage in STAGES:

        html += f"""
<div style="width:90px;text-align:center;">
{LABELS[stage]}
</div>
"""

    html += "</div>"

    st.markdown(

        html,

        unsafe_allow_html=True,

    )

