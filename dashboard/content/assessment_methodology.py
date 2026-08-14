"""
EQMP / EQRAF assessment methodology parameters.

These values are controlled by EQMP and are not supplied
by the organisation completing the assessment.
"""

ASSESSMENT_METHODOLOGY = {
    "name": "Enterprise Quantum Readiness Assessment Framework",
    "short_name": "EQRAF",
    "version": "1.0",
}

#
# Quantum threat horizon used by EQMP for temporal
# exposure analysis.
#
# This is a methodology assumption / assessment horizon,
# not a prediction of the arrival date of a CRQC.
#

QUANTUM_THREAT_HORIZON_YEAR = 2035


def quantum_threat_horizon():

    return QUANTUM_THREAT_HORIZON_YEAR


def methodology_name():

    return ASSESSMENT_METHODOLOGY["name"]


def methodology_version():

    return ASSESSMENT_METHODOLOGY["version"]
