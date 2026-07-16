from pathlib import Path
import json
import zipfile
from datetime import datetime


def build_package():

    reports = Path("reports")
    reports.mkdir(exist_ok=True)

    metadata = {
        "generated": datetime.now().isoformat(),
        "platform": "Enterprise Quantum Migration Platform",
        "version": "1.0",
        "assessment": "Post-Quantum Readiness Assessment",
    }

    metadata_file = reports / "assessment_metadata.json"

    metadata_file.write_text(
        json.dumps(metadata, indent=4)
    )

    package = reports / "EQMP_Assessment_Package.zip"

    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as z:

        files = [
            reports / "pqc_executive_report.pdf",
            reports / "pqc_report.txt",
            Path("inventory.json"),
            metadata_file,
        ]

        for file in files:

            if file.exists():

                z.write(file, arcname=file.name)

    return package


if __name__ == "__main__":

    print(build_package())
