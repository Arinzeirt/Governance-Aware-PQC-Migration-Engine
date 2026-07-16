import streamlit as st


def load():

    st.markdown(
        """
<style>

/* ---------- MAIN LAYOUT ---------- */

.block-container{

    padding-top:0.45rem;

    padding-bottom:2rem;

    max-width:1500px;

}

/* Hide Streamlit's default spacing */

[data-testid="stHeader"]{

    background:transparent;

}

</style>
""",
        unsafe_allow_html=True,
    )
