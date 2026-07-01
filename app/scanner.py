from pathlib import Path
import re

from classifier import classify_content


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
    "SHA-256": r"\bSHA-256\b"
}


def scan_directory(directory, max_findings=None):

    findings = {}

    finding_count = 0

    for file in Path(directory).rglob("*"):

        if not file.is_file():
            continue

        try:

            content = file.read_text(errors="ignore")

            matches = []

            for keyword, pattern in CRYPTO_PATTERNS.items():

                if re.search(pattern, content):

                    matches.append({

                        "type": "keyword",

                        "value": keyword

                    })

            classifications = classify_content(content)

            for item in classifications:

                matches.append({

                    "type": "classification",

                    "value": item

                })

            if matches:

                findings[str(file)] = matches

                finding_count += len(matches)

                if (
                    max_findings is not None
                    and finding_count >= max_findings
                ):
                    break

        except Exception:

            continue

    return findings
