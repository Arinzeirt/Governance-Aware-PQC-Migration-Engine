from pathlib import Path
import shutil
import subprocess
import tempfile


class TargetManager:

    def __init__(self):

        self.workspace = Path("workspace")

        self.workspace.mkdir(exist_ok=True)

    def prepare_local(self, directory):

        directory = Path(directory)

        if not directory.exists():

            raise FileNotFoundError(
                f"Directory not found: {directory}"
            )

        return directory

    def prepare_github(self, url):

        repo_name = url.rstrip("/").split("/")[-1]

        target = self.workspace / repo_name

        if target.exists():

            shutil.rmtree(target)

        subprocess.run(
            [
                "git",
                "clone",
                url,
                str(target)
            ],
            check=True,
        )

        return target

    def cleanup(self):

        if self.workspace.exists():

            shutil.rmtree(self.workspace)

            self.workspace.mkdir(exist_ok=True)


manager = TargetManager()

