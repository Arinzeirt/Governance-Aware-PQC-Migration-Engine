"""
EQMP temporal-risk model.

Mosca's inequality:

    X + Y > Z

X = required security / data protection lifetime
Y = estimated migration time
Z = EQMP system quantum threat horizon

Z is system-generated and is NOT entered by the
organisation during the assessment.

The threat horizon is a planning assumption used
by EQMP for migration decision-making. It should
not be interpreted as a prediction of the exact
arrival date of a cryptographically relevant
quantum computer.
"""


# ==========================================================
# EQMP SYSTEM THREAT HORIZON
# ==========================================================

# Central system planning assumption.
#
# Keep this value in one place so it can later be
# updated through the EQMP methodology / configuration
# layer without changing assessment forms.

EQMP_THREAT_HORIZON_YEARS = 15


def calculate_threat_horizon():

    return EQMP_THREAT_HORIZON_YEARS


# ==========================================================
# X — SECURITY / DATA SHELF LIFE
# ==========================================================

def calculate_shelf_life(overview):

    """
    Estimate X from organisational exposure.

    Regulatory obligations, critical infrastructure
    status and critical business services increase
    the required protection lifetime.
    """

    score = 5

    if overview.get(
        "critical_infrastructure"
    ) == "Yes":

        score += 5

    regulatory = overview.get(
        "regulatory_environment",
        [],
    )

    if regulatory:

        score += 5

    if any(
        item in regulatory
        for item in [
            "Data Protection / Privacy",
            "Banking / Financial Services",
            "Payment / Financial Infrastructure",
            "Healthcare Regulation",
        ]
    ):

        score += 5

    services = overview.get(
        "critical_business_services",
        [],
    )

    if services:

        score += 5

    if len(services) >= 3:

        score += 5

    return min(
        score,
        25,
    )


# ==========================================================
# Y — MIGRATION TIME
# ==========================================================

def calculate_migration_time(
    overview,
    technology,
    cryptography,
    governance,
):

    """
    Estimate Y from enterprise complexity,
    cryptographic visibility, agility and governance.
    """

    years = 3

    size = overview.get(
        "organisation_size"
    )

    size_factor = {

        "1–50": 0,

        "51–250": 1,

        "251–1000": 2,

        "1000+": 4,

    }

    years += size_factor.get(
        size,
        2,
    )

    deployment = technology.get(
        "deployment_model"
    )

    if deployment == "Hybrid":

        years += 2

    elif deployment == "On-Premises":

        years += 1

    systems = cryptography.get(
        "crypto_business_systems",
        [],
    )

    if len(systems) >= 5:

        years += 2

    elif len(systems) >= 3:

        years += 1

    if cryptography.get(
        "crypto_inventory"
    ) != "Yes":

        years += 2

    if cryptography.get(
        "crypto_agility"
    ) != "Yes":

        years += 2

    if cryptography.get(
        "certificate_inventory"
    ) in [
        "Partial",
        "None",
    ]:

        years += 1

    if governance.get(
        "pqc_strategy"
    ) == "No":

        years += 2

    elif governance.get(
        "pqc_strategy"
    ) == "In Development":

        years += 1

    if governance.get(
        "executive_support"
    ) == "No":

        years += 1

    return min(
        years,
        20,
    )


# ==========================================================
# MOSCA ASSESSMENT
# ==========================================================

def calculate(assessment):

    overview = assessment.get(
        "overview",
        {},
    )

    technology = assessment.get(
        "technology",
        {},
    )

    cryptography = assessment.get(
        "cryptography",
        {},
    )

    governance = assessment.get(
        "governance",
        {},
    )

    # ------------------------------------------------------
    # X
    # ------------------------------------------------------

    x = calculate_shelf_life(
        overview
    )

    # ------------------------------------------------------
    # Y
    # ------------------------------------------------------

    y = calculate_migration_time(
        overview,
        technology,
        cryptography,
        governance,
    )

    # ------------------------------------------------------
    # Z
    #
    # System generated.
    # No user input required.
    # ------------------------------------------------------

    z = calculate_threat_horizon()

    # ------------------------------------------------------
    # Temporal exposure
    # ------------------------------------------------------

    exposure = (
        x
        + y
        - z
    )

    exposed = exposure > 0

    if exposure >= 10:

        level = "Critical"

    elif exposure >= 5:

        level = "High"

    elif exposure > 0:

        level = "Elevated"

    else:

        level = "Within Migration Window"

    return {

        "x":
            x,

        "y":
            y,

        "z":
            z,

        "exposure":
            exposure,

        "exposed":
            exposed,

        "level":
            level,

        "inequality":
            (
                f"{x} + {y} "
                f"{'>' if exposed else '<='} "
                f"{z}"
            ),

        "threat_horizon_years":
            z,

        "threat_horizon_source":
            "EQMP system planning assumption",

    }
