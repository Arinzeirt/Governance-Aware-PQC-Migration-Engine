import streamlit as st

from auth import authenticate


def show():

    st.markdown(
        """
<div style="
    max-width:460px;
    margin:70px auto 0 auto;
">

<div style="
    display:flex;
    align-items:baseline;
    gap:10px;
    margin-bottom:7px;
">

<span style="
    font-size:1.55rem;
    font-weight:750;
    color:#F5F7FA;
">
EQMP
</span>

<span style="
    font-size:1.55rem;
    font-weight:750;
    color:#F5F7FA;
">
·
</span>

<span style="
    font-size:1.55rem;
    font-weight:750;
    color:#F5F7FA;
">
Sign in
</span>

</div>

<div style="
    font-size:0.86rem;
    color:#8FA1B5;
    line-height:1.5;
    margin-bottom:24px;
">
Access your organisation's quantum migration command center.
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    left, center, right = st.columns(
        [1, 3, 1]
    )

    with center:

        identifier = st.text_input(
            "Business Email",
            placeholder="name@company.com",
            key="eqmp_login_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="eqmp_login_password",
        )

        remember = st.checkbox(
            "Remember this device",
            key="eqmp_remember_device",
        )

        if st.button(
            "Sign In",
            type="primary",
            use_container_width=True,
            key="eqmp_sign_in",
        ):

            account = authenticate(
                identifier.strip(),
                password,
            )

            if account:

                st.session_state[
                    "eqmp_authenticated"
                ] = True

                st.session_state[
                    "eqmp_user_identifier"
                ] = account["identifier"]

                st.session_state[
                    "eqmp_user_email"
                ] = account["identifier"]

                st.session_state[
                    "eqmp_user_role"
                ] = account["role"]

                st.session_state[
                    "eqmp_user_name"
                ] = account["name"]

                st.session_state.page = (
                    "command_center"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid business email or password."
                )

        st.markdown(
            """
<div style="
    margin-top:18px;
    text-align:center;
    font-size:0.76rem;
    color:#718096;
">
Account access is provisioned by EQMP.
</div>
""",
            unsafe_allow_html=True,
        )

        if st.button(
            "← Back to EQMP",
            use_container_width=True,
            key="eqmp_login_back",
        ):

            st.session_state.page = "landing"
            st.rerun()
