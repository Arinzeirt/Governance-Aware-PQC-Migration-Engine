import streamlit as st

from utils.framework_registry import FRAMEWORK_REGISTRY


def show(
    title,
    description,
    item_id,
    button_label="View Details",
):

    framework = FRAMEWORK_REGISTRY.get(
        title,
        {
            "id": "EQMP-UNK-000",
            "status": "Research Complete",
        },
    )

    framework_id = framework["id"]
    status = framework["status"]

    disabled = status != "Research Complete"

    with st.container(border=True):

        st.markdown(
            f"""
<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:14px;
">

<div style="
display:inline-block;
padding:4px 10px;
border:1px solid #3B82F6;
border-radius:999px;
font-size:12px;
font-weight:700;
letter-spacing:0.8px;
color:#93C5FD;
background:rgba(59,130,246,0.08);
">
{framework_id}
</div>

<div style="
font-size:12px;
font-weight:600;
color:#9CA3AF;
text-transform:uppercase;
">
{status}
</div>

</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
<div style="
height:105px;
font-size:26px;
font-weight:700;
line-height:1.25;
display:flex;
align-items:flex-start;
">
{title.replace(" (Coming Soon)", "")}
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
<div style="
height:95px;
font-size:15px;
line-height:1.6;
color:#CBD5E1;
overflow:hidden;
">
{description}
</div>
""",
            unsafe_allow_html=True,
        )

        st.button(
            "View Framework" if not disabled else "Research in Progress",
            key=f"research_{item_id}",
            use_container_width=True,
            disabled=disabled,
        )

        if (
            not disabled
            and st.session_state.get(f"research_{item_id}")
        ):
            st.session_state.research_item = title
            st.session_state.page = "research_detail"
            st.rerun()
