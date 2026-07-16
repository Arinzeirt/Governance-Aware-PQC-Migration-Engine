from pathlib import Path
import shutil
import zipfile

import streamlit as st

from engine.runner import runner
from engine.runtime import runtime


WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

DEMO_REPOSITORY = WORKSPACE / "demo"

DEFAULT_REPOSITORY = str(
    Path.home()
    / "Downloads"
    / "streple-backend-main"
)


def prepare_uploaded_zip(uploaded_file):

    upload_dir = WORKSPACE / "uploaded_repository"

    if upload_dir.exists():
        shutil.rmtree(upload_dir)

    upload_dir.mkdir(parents=True)

    zip_path = upload_dir / uploaded_file.name

    with open(zip_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    extract_dir = upload_dir / "repository"

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    children = list(extract_dir.iterdir())

    if len(children) == 1 and children[0].is_dir():
        return str(children[0])

    return str(extract_dir)


def show():

    st.markdown("## Assessment Target")

    target_type = st.radio(

        "Assessment Source",

        [

            "Demo Repository",

            "Upload ZIP Repository",

            "GitHub Repository",

            "Local Directory",

        ],

        horizontal=False,

    )

    target = ""

    if target_type == "Demo Repository":

        st.info(
            "Run the assessment using the bundled demonstration repository."
        )

        target = str(DEMO_REPOSITORY)

    elif target_type == "Upload ZIP Repository":

        uploaded = st.file_uploader(

            "Upload Repository (.zip)",

            type=["zip"],

        )

        if uploaded is not None:

            target = prepare_uploaded_zip(uploaded)

            st.success("Repository uploaded successfully.")

    elif target_type == "GitHub Repository":

        target = st.text_input(

            "GitHub Repository URL",

            placeholder="https://github.com/owner/repository",

        )

    else:

        target = st.text_input(

            "Repository Path",

            value=DEFAULT_REPOSITORY,

        )

    st.session_state.assessment_target_type = target_type
    st.session_state.assessment_target = target

    st.write("")

    running = runtime.running

    if running:

        st.info("Assessment is currently running...")

    _, button = st.columns([3, 1])

    with button:

        disabled = running or not target

        if st.button(

            "Start Assessment",

            type="primary",

            use_container_width=True,

            disabled=disabled,

        ):

            started = runner.start(

                target_type,

                target,

            )

            if started:

                st.rerun()

