import streamlit as st


def load():

    st.markdown(
        """
<style>

/* ---------- Global ---------- */

html,
body,
[data-testid="stAppViewContainer"]{

    background:#050B18;

    color:#F4F7FB;

    font-family:Inter,sans-serif;

}


/* Remove Streamlit Header */

header{

    visibility:hidden;

}

#MainMenu{

    visibility:hidden;

}

footer{

    visibility:hidden;

}


/* Main Width */

.block-container{

    max-width:1450px;

    padding-top:2rem;

    padding-bottom:3rem;

}


/* Typography */

h1{

    font-size:54px;

    font-weight:700;

}

h2{

    font-size:34px;

}

h3{

    font-size:24px;

}

p{

    color:#A8B5D0;

}


/* Divider */

hr{

    border-color:#14233C;

}

</style>
        """,
        unsafe_allow_html=True,
    )
