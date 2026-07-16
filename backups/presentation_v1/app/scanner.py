from pathlib import Path
import re

from classifier import classify_content


#
# Cryptographic Patterns
#

CRYPTO_PATTERNS = {
    "RSA": r"\bRSA\b",
    "ECC": r"\bECC\b",
    "ECDSA": r"\bECDSA\b",
    "ECDH": r"\bECDH\b",
    "TLS": r"\bTLS\b",
    "SSL": r"\bSSL\b",
    "OpenSSL": r"\bOpenSSL\b",
    "SHA1": r"\bSHA1\b",
    "SHA-1": r"\bSHA-1\b",
    "SHA256": r"\bSHA256\b",
    "SHA-256": r"\bSHA-256\b",
}


#
# Directories ignored during assessment
#

IGNORED_DIRECTORIES = {

    ".git",
    ".github",

    "node_modules",

    "dist",
    "build",
    "coverage",

    ".next",
    ".nuxt",

    "__pycache__",

    "venv",
    ".venv",

    ".idea",
    ".vscode",

    "vendor",

}


#
# File extensions we actually want
#

SOURCE_EXTENSIONS = {

    ".py",
    ".js",
    ".ts",
    ".tsx",

    ".java",
    ".kt",

    ".cs",

    ".go",

    ".cpp",
    ".cc",
    ".c",
    ".h",

    ".php",

    ".rb",

    ".rs",

    ".swift",

    ".json",

    ".yaml",
    ".yml",

    ".xml",

    ".properties",

    ".env",

}


def should_scan(file: Path):

    #
    # Ignore folders
    #

    if any(

        part in IGNORED_DIRECTORIES

        for part in file.parts

    ):

        return False

    #
    # Ignore large binary assets
    #

    if file.suffix.lower() not in SOURCE_EXTENSIONS:

        return False

    return True


def scan_directory(

    directory,

    max_findings=None,

    callback=None,

):

    findings = {}

    finding_count = 0

    files = [

        f

        for f in Path(directory).rglob("*")

        if f.is_file()

        and should_scan(f)

    ]

    total_files = len(files)

    for index, file in enumerate(

        files,

        start=1,

    ):

        if callback:

            callback(

                event="file",

                file=str(file),

                current=index,

                total=total_files,

            )

        try:

            content = file.read_text(

                errors="ignore"

            )

            matches = []

            #
            # Keyword Detection
            #

            for keyword, pattern in CRYPTO_PATTERNS.items():

                if re.search(

                    pattern,

                    content,

                ):

                    matches.append(

                        {

                            "type": "keyword",

                            "value": keyword,

                        }

                    )

                    if callback:

                        callback(

                            event="keyword",

                            keyword=keyword,

                            file=str(file),

                        )

            #
            # Classification
            #

            for item in classify_content(

                content

            ):

                matches.append(

                    {

                        "type": "classification",

                        "value": item,

                    }

                )

                if callback:

                    callback(

                        event="classification",

                        classification=item["classification"],

                        file=str(file),

                    )

            if matches:

                findings[str(file)] = matches

                finding_count += len(matches)

            if (

                max_findings

                and finding_count >= max_findings

            ):

                break

        except Exception:

            continue

    return findings

