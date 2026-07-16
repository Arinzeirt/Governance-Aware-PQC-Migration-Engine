import streamlit as st


def begin(

    title,

    subtitle=None,

):

    html = f"""

<div class="eqmp-panel">

<div class="eqmp-panel-title">

{title}

</div>

"""

    if subtitle:

        html += f"""

<div class="eqmp-panel-subtitle">

{subtitle}

</div>

"""

    st.markdown(

        html,

        unsafe_allow_html=True,

    )


def end():

    st.markdown(

        "</div>",

        unsafe_allow_html=True,

    )


def section(

    title,

    subtitle=None,

):

    begin(

        title,

        subtitle,

    )

