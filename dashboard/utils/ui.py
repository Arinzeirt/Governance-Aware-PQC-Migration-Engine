import streamlit as st


def scroll_to_top():
    """
    Scroll the browser to the top of the page.

    Used after page navigation so every new page
    begins from the top instead of preserving the
    previous scroll position.
    """

    st.markdown(
        """
<script>
window.parent.scrollTo({
    top: 0,
    left: 0,
    behavior: "instant"
});
</script>
""",
        unsafe_allow_html=True,
    )
