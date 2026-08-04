import os
import streamlit as st
from PIL import UnidentifiedImageError


def show(brief):

    with st.container(border=True):

        left, right = st.columns([2, 3], gap="large")

        #
        # Illustration
        #

        with left:

            try:

                if (
                    brief.image
                    and os.path.exists(brief.image)
                    and os.path.getsize(brief.image) > 0
                ):

                    st.image(
                        brief.image,
                        width="stretch",
                    )

                else:

                    raise FileNotFoundError

            except (
                FileNotFoundError,
                UnidentifiedImageError,
                OSError,
            ):

                st.markdown(
                    """
<div style="
height:260px;
display:flex;
align-items:center;
justify-content:center;
background:linear-gradient(135deg,#0B2447,#19376D);
border-radius:18px;
font-size:82px;
">
🛡️
</div>
""",
                    unsafe_allow_html=True,
                )

        #
        # Content
        #

        with right:

            st.caption(brief.category.upper())

            st.markdown(
                f"""
<h1 style="
font-size:3rem;
font-weight:800;
line-height:1.0;
margin-bottom:18px;
">
{brief.headline.replace(chr(10), "<br>")}
</h1>
""",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
<div style="
font-size:1.08rem;
line-height:1.8;
color:#BFC8D6;
max-width:640px;
margin-bottom:30px;
">
{brief.message}
</div>
""",
                unsafe_allow_html=True,
            )

            st.markdown("---")

            c1, c2 = st.columns([1, 2])

            with c1:
                st.caption("📖 Research Brief")

            with c2:
                st.caption(
                    f"Estimated Reading Time: {brief.reading_time}"
                )
