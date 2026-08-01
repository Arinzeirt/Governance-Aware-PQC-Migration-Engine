import streamlit as st

from engine.runtime import runtime


STATUS_COLOURS = {
    "Ready": "#14B8A6",
    "Running": "#2563EB",
    "Completed": "#22C55E",
    "Failed": "#EF4444",
    "Pending": "#F59E0B",
    "Waiting": "#94A3B8",
    "Scanning": "#2563EB",
    "Inventory": "#8B5CF6",
    "Reporting": "#F97316",
}


def card(title, value):

    colour = STATUS_COLOURS.get(

        value,

        "#CBD5E1",

    )

    st.markdown(

        f"""
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:18px;
height:120px;
">

<div style="
font-size:13px;
color:#94A3B8;
margin-bottom:12px;
font-weight:600;
">

{title}

</div>

<div style="
display:flex;
align-items:center;
gap:10px;
">

<div style="
width:12px;
height:12px;
border-radius:50%;
background:{colour};
box-shadow:0 0 10px {colour};
"></div>

<div style="
font-size:24px;
font-weight:700;
color:#F8FAFC;
">

{value}

</div>

</div>

</div>

""",

        unsafe_allow_html=True,

    )


def show():

    #
    # Assessment
    #

    assessment = runtime.status

    #
    # Target
    #

    target = st.session_state.get(

        "assessment_target_type",

        "Repository",

    )

    if target == "Local Directory":

        target = "Local"

    elif target == "GitHub Repository":

        target = "GitHub"

    #
    # Discovery
    #

    if runtime.stage == "Discovery":

        discovery = "Scanning"

    elif runtime.stage in [

        "Inventory",

        "Reporting",

        "Completed",

    ]:

        discovery = "Completed"

    else:

        discovery = "Pending"

    #
    # Governance
    #

    if runtime.stage == "Inventory":

        governance = "Inventory"

    elif runtime.stage == "Reporting":

        governance = "Reporting"

    elif runtime.status == "Completed":

        governance = "Completed"

    else:

        governance = "Waiting"

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        card(

            "Assessment",

            assessment,

        )

    with c2:

        card(

            "Target",

            target,

        )

    with c3:

        card(

            "Discovery",

            discovery,

        )

    with c4:

        card(

            "Governance",

            governance,

        )

