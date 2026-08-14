from components.assessment.engine.mosca import (
    calculate as calculate_mosca,
)


def _score(value, mapping):
    return mapping.get(value, 0)


def _cap(score, maximum):
    return max(0, min(round(score), maximum))


def calculate(assessment):

    overview = assessment.get(
        "overview",
        {},
    )

    technology = assessment.get(
        "technology",
        {},
    )

    crypto = assessment.get(
        "cryptography",
        {},
    )

    governance = assessment.get(
        "governance",
        {},
    )

    # ======================================================
    # 1. GOVERNANCE & RISK
    #
    # Readiness requires demonstrated governance.
    # Positive answers do not automatically imply maturity.
    # ======================================================

    governance_score = sum([

        _score(
            governance.get("security_governance"),
            {
                "Yes": 20,
                "No": 0,
            },
        ),

        _score(
            governance.get("pqc_strategy"),
            {
                "Yes": 25,
                "In Development": 12,
                "No": 0,
            },
        ),

        _score(
            governance.get("crypto_policy"),
            {
                "Documented": 20,
                "Partial": 8,
                "None": 0,
            },
        ),

        _score(
            governance.get("risk_register"),
            {
                "Yes": 15,
                "No": 0,
            },
        ),

        _score(
            governance.get("compliance_program"),
            {
                "Yes": 10,
                "No": 0,
            },
        ),

        _score(
            governance.get("executive_support"),
            {
                "Yes": 10,
                "No": 0,
            },
        ),

    ])

    governance_score = _cap(
        governance_score,
        100,
    )

    # ======================================================
    # 2. CRYPTOGRAPHIC MANAGEMENT POSTURE
    #
    # This measures organisational ability to manage
    # cryptography — NOT discovered cryptographic exposure.
    #
    # No scanner has been run at this stage.
    # ======================================================

    crypto_score = sum([

        _score(
            crypto.get("pki_maturity"),
            {
                "Fully Managed": 25,
                "Partially Managed": 12,
                "Limited Visibility": 4,
                "Unknown": 0,
            },
        ),

        _score(
            crypto.get("certificate_inventory"),
            {
                "Complete": 25,
                "Partial": 10,
                "None": 0,
                "Unknown": 0,
            },
        ),

        _score(
            crypto.get("crypto_inventory"),
            {
                "Yes": 30,
                "In Progress": 12,
                "No": 0,
            },
        ),

        _score(
            crypto.get("crypto_agility"),
            {
                "Yes": 20,
                "No": 0,
                "Unknown": 0,
            },
        ),

    ])

    crypto_score = _cap(
        crypto_score,
        100,
    )

    # ======================================================
    # 3. TECHNOLOGY READINESS
    #
    # Technology presence itself is NOT readiness.
    # We give limited credit for supporting capabilities.
    # ======================================================

    technology_score = sum([

        _score(
            technology.get("pki"),
            {
                "Yes": 20,
                "Unknown": 0,
                "No": 0,
            },
        ),

        _score(
            technology.get("hsm"),
            {
                "Yes": 20,
                "Unknown": 0,
                "No": 0,
            },
        ),

        _score(
            technology.get("customer_apps"),
            {
                "Yes": 10,
                "No": 0,
            },
        ),

        _score(
            technology.get("public_api"),
            {
                "Yes": 10,
                "No": 0,
            },
        ),

        _score(
            technology.get("third_party_dependencies"),
            {
                "Yes": 5,
                "Unknown": 0,
                "No": 5,
            },
        ),

    ])

    technology_score = _cap(
        technology_score,
        65,
    )

    # Normalise the deliberately conservative technology
    # capability score to a 100-point dimension.
    technology_score = round(
        technology_score / 65 * 100
    )

    # ======================================================
    # 4. MOSCA TEMPORAL RISK
    #
    # Internal decision model.
    # The X + Y > Z mechanics remain hidden from executives.
    # ======================================================

    mosca = calculate_mosca(
        assessment
    )

    if mosca["level"] == "Critical":
        migration_penalty = 25

    elif mosca["level"] == "High":
        migration_penalty = 15

    elif mosca["level"] == "Elevated":
        migration_penalty = 7

    else:
        migration_penalty = 0

    # ======================================================
    # 5. MIGRATION READINESS
    #
    # Migration readiness is primarily determined by whether
    # governance and cryptographic management foundations exist.
    # ======================================================

    base_migration_score = round(
        (
            governance_score * 0.45
            + crypto_score * 0.45
            + technology_score * 0.10
        )
    )

    migration_score = max(
        0,
        base_migration_score - migration_penalty,
    )

    # ======================================================
    # 6. OVERALL READINESS
    #
    # Conservative weighting:
    #
    # Governance       30%
    # Cryptography     40%
    # Technology       10%
    # Migration        20%
    #
    # This makes structural cryptographic readiness central.
    # ======================================================

    overall_score = round(
        (
            governance_score * 0.30
            + crypto_score * 0.40
            + technology_score * 0.10
            + migration_score * 0.20
        )
    )

    # ======================================================
    # 7. READINESS GATES
    #
    # A company cannot reach advanced readiness while
    # fundamental migration capabilities are absent.
    # ======================================================

    readiness_ceiling = 100

    if crypto.get("crypto_inventory") != "Yes":
        readiness_ceiling = min(
            readiness_ceiling,
            69,
        )

    if crypto.get("crypto_agility") != "Yes":
        readiness_ceiling = min(
            readiness_ceiling,
            74,
        )

    if governance.get("pqc_strategy") != "Yes":
        readiness_ceiling = min(
            readiness_ceiling,
            69,
        )

    if governance.get("security_governance") != "Yes":
        readiness_ceiling = min(
            readiness_ceiling,
            64,
        )

    if governance.get("executive_support") != "Yes":
        readiness_ceiling = min(
            readiness_ceiling,
            74,
        )

    overall_score = min(
        overall_score,
        readiness_ceiling,
    )

    # Mosca temporal exposure also prevents a high score
    # from masking an insufficient migration window.

    if mosca["level"] == "Critical":

        overall_score = min(
            overall_score,
            59,
        )

    elif mosca["level"] == "High":

        overall_score = min(
            overall_score,
            74,
        )

    overall_score = _cap(
        overall_score,
        100,
    )

    # ======================================================
    # 8. READINESS LABEL
    # ======================================================

    if overall_score >= 85:

        label = "Advanced Readiness"

    elif overall_score >= 70:

        label = "Established Readiness"

    elif overall_score >= 50:

        label = "Developing Readiness"

    elif overall_score >= 30:

        label = "Limited Readiness"

    else:

        label = "Significant Readiness Gap"

    # ======================================================
    # 9. ASSESSMENT-LEVEL THREAT SIGNAL
    #
    # IMPORTANT:
    # This does NOT claim cryptographic vulnerabilities were
    # discovered. It reflects the organisational information
    # supplied through the assessment.
    # ======================================================

    long_term_data = crypto.get(
        "long_term_data"
    )

    critical_infrastructure = overview.get(
        "critical_infrastructure"
    )

    threat_score = 0

    if long_term_data == "Yes":
        threat_score += 30

    if critical_infrastructure == "Yes":
        threat_score += 20

    if crypto.get("crypto_inventory") != "Yes":
        threat_score += 20

    if governance.get("pqc_strategy") != "Yes":
        threat_score += 15

    if crypto.get("crypto_agility") != "Yes":
        threat_score += 10

    if mosca["level"] == "Critical":
        threat_score += 20

    elif mosca["level"] == "High":
        threat_score += 15

    elif mosca["level"] == "Elevated":
        threat_score += 8

    threat_score = _cap(
        threat_score,
        100,
    )

    if threat_score >= 70:

        threat_level = "High"

    elif threat_score >= 40:

        threat_level = "Elevated"

    else:

        threat_level = "Developing"

    # ======================================================
    # 10. EXECUTIVE FINDINGS
    #
    # These findings are based ONLY on assessment responses.
    # No cryptographic discovery claims are made.
    # ======================================================

    findings = []

    if crypto.get("crypto_inventory") != "Yes":

        findings.append(
            "Cryptographic asset visibility is currently "
            "limited, reducing the organisation's ability "
            "to establish a complete migration baseline."
        )

    if crypto.get("crypto_agility") != "Yes":

        findings.append(
            "Cryptographic agility is not yet demonstrated, "
            "which may increase the effort required to "
            "transition cryptographic controls."
        )

    if governance.get("pqc_strategy") != "Yes":

        findings.append(
            "A formal post-quantum migration strategy has "
            "not yet been fully established."
        )

    if governance.get("crypto_policy") != "Documented":

        findings.append(
            "Cryptographic governance and policy require "
            "further structural development."
        )

    if governance.get("risk_register") != "Yes":

        findings.append(
            "Cryptographic risk is not yet demonstrated as "
            "being consistently incorporated into enterprise "
            "risk management."
        )

    if governance.get("executive_support") != "Yes":

        findings.append(
            "Executive sponsorship for post-quantum "
            "transformation is not yet established."
        )

    if long_term_data == "Yes":

        findings.append(
            "Long-lived sensitive information increases the "
            "importance of early post-quantum planning."
        )

    if critical_infrastructure == "Yes":

        findings.append(
            "Critical infrastructure responsibilities "
            "increase the importance of structured "
            "cryptographic transition planning."
        )

    if mosca["exposed"]:

        findings.append(
            "The assessment indicates that the current "
            "migration planning window may be insufficient "
            "relative to the assessed threat horizon."
        )

    # Keep the executive page concise.
    if not findings:

        findings.append(
            "The organisation demonstrates established "
            "foundations for post-quantum readiness. "
            "Evidence-based discovery is required to "
            "validate the underlying cryptographic estate."
        )

    # ======================================================
    # 11. NEXT ACTIONS
    #
    # These remain available to the underlying engine but
    # are not required to be displayed on the executive page.
    # ======================================================

    actions = []

    if crypto.get("crypto_inventory") != "Yes":

        actions.append(
            "Establish a complete cryptographic asset inventory."
        )

    if crypto.get("crypto_agility") != "Yes":

        actions.append(
            "Develop cryptographic agility capabilities "
            "to support future algorithm transitions."
        )

    if governance.get("pqc_strategy") != "Yes":

        actions.append(
            "Develop a governance-aware post-quantum "
            "migration strategy."
        )

    if governance.get("crypto_policy") != "Documented":

        actions.append(
            "Strengthen enterprise cryptographic governance "
            "and policy controls."
        )

    if mosca["exposed"]:

        actions.append(
            "Prioritise migration planning because the "
            "assessed protection and migration window "
            "may exceed the quantum threat horizon."
        )

    if not actions:

        actions.append(
            "Proceed to evidence-based cryptographic discovery "
            "and migration planning."
        )

    # ======================================================
    # 12. RESULT
    # ======================================================

    return {

        "overall_score":
            overall_score,

        "overall_label":
            label,

        "governance":
            governance_score,

        "cryptography":
            crypto_score,

        "technology":
            technology_score,

        "migration":
            migration_score,

        "base_migration":
            base_migration_score,

        "threat_score":
            threat_score,

        "threat_level":
            threat_level,

        # No cryptographic scan has been performed.
        # Keep this field for compatibility without
        # claiming discovered vulnerable algorithms.
        "vulnerable_algorithms":
            0,

        "findings":
            findings,

        "actions":
            actions,

        # ==================================================
        # Mosca result
        #
        # Retained for internal/report use.
        # ==================================================

        "mosca":
            mosca,

        "mosca_x":
            mosca["x"],

        "mosca_y":
            mosca["y"],

        "mosca_z":
            mosca["z"],

        "mosca_exposure":
            mosca["exposure"],

        "mosca_level":
            mosca["level"],

        "mosca_exposed":
            mosca["exposed"],

        "mosca_inequality":
            mosca["inequality"],
    }
