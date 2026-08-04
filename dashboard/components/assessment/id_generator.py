from datetime import datetime


COUNTRY_CODES = {
    "Nigeria": "NGA",
    "United Kingdom": "GBR",
    "United States": "USA",
    "Canada": "CAN",
    "Ghana": "GHA",
    "Kenya": "KEN",
    "South Africa": "ZAF",
}


INDUSTRY_CODES = {
    "Banking": "BANK",
    "Financial Services": "FSI",
    "Government": "GOV",
    "Healthcare": "HEALTH",
    "Education": "EDU",
    "Technology": "TECH",
    "Telecommunications": "TELCO",
    "Manufacturing": "MFG",
    "Energy": "ENERGY",
    "Retail": "RETAIL",
}


def generate(country, industry, sequence="000001"):

    year = datetime.now().year

    country_code = COUNTRY_CODES.get(country, "INT")

    industry_code = INDUSTRY_CODES.get(industry, "OTHER")

    return (
        f"EQMP-"
        f"{country_code}-"
        f"{industry_code}-"
        f"{year}-"
        f"{sequence}"
    )
