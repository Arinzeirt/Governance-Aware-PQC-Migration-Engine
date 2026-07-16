import streamlit as st


def load_theme():

    st.markdown(
        """
<style>

.block-container{
    padding-top:2rem;
    max-width:1400px;
}

.executive-card{

    min-height:360px;

}

.hero-card{

    min-height:520px;

}

.status-high{

    color:#dc2626;

    font-weight:700;

}

.status-medium{

    color:#d97706;

    font-weight:700;

}

.status-low{

    color:#16a34a;

    font-weight:700;

}

</style>
""",
        unsafe_allow_html=True,
    )

