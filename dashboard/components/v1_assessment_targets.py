import streamlit as st


@st.dialog("EQMP Enterprise Edition")
def enterprise_dialog(module_name):

    st.markdown(f"""
## {module_name}

This assessment capability is available in the
**EQMP Enterprise Edition**.

### Included in Technology Preview v1.0

- ✅ Backend Source Code Assessment
- ✅ Executive Reporting
- ✅ Technical Inventory

### Enterprise Edition

- Git Repository Assessment
- API Gateway Assessment
- Cloud Infrastructure Assessment
- Network Device Assessment
- Migration Planner
""")


def chip(label, active=False):

    if active:

        st.markdown(f"""
<div style="
background:#1E293B;
border:1px solid #2563EB;
border-radius:12px;
padding:10px 16px;
text-align:center;
font-size:14px;
font-weight:600;
">

☑ {label}

</div>
""", unsafe_allow_html=True)

    else:

        if st.button(
            f"☐ {label}",
            use_container_width=True,
            key=label,
        ):

            enterprise_dialog(label)


def show():

    st.markdown(
        '<div class="eqmp-section">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="eqmp-title">Assessment Targets</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        chip("Backend Source Code", True)

    with c2:
        chip("Git Repository")

    with c3:
        chip("API Gateway")

    with c4:
        chip("Cloud Infrastructure")

    with c5:
        chip("Network Devices")

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )
