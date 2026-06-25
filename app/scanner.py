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

def scan_directory(directory):
    findings = {}

    for file in Path(directory).rglob("*"):
        if file.is_file():
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

            except Exception:
                pass

    return findings
