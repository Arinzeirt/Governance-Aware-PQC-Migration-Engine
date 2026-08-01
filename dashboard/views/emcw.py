import streamlit as st


def show():

    st.title(
        "Enterprise Migration Configuration"
    )

    st.caption(
        "Configure business, governance and regulatory context before generating a migration strategy."
    )

    st.divider()

    #
    # Progress
    #

    st.progress(
        0.15,
        text="Step 1 of 7 • Enterprise Profile",
    )

    st.write("")

    #
    # Enterprise Profile
    #

    st.subheader(
        "Enterprise Profile"
    )

    organization = st.text_input(
        "Organization Name"
    )

    industry = st.selectbox(

        "Industry",

        [

            "Financial Services",

            "Government",

            "Healthcare",

            "Energy",

            "Telecommunications",

            "Manufacturing",

            "Technology",

            "Other",

        ],

    )

    country = st.text_input(
        "Country"
    )

    size = st.selectbox(

        "Organization Size",

        [

            "Small",

            "Medium",

            "Large",

            "Enterprise",

        ],

    )

    st.write("")

    left, right = st.columns(2)

    with left:

        st.button(

            "Back",

            use_container_width=True,

        )

    with right:

        st.button(

            "Save & Continue",

            type="primary",

            use_container_width=True,

        )
