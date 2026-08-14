from components.assessment.store import load


SECTIONS = [

    "overview",

    "technology",

    "cryptography",

    "governance",

]


def load_assessment():
    """
    Load the complete enterprise assessment.

    Returns a dictionary containing every completed
    assessment section.

    This repository becomes the single source of truth
    for Executive Review, reporting, AI analysis and
    PDF generation.
    """

    assessment = {}

    for section in SECTIONS:

        assessment[section] = load(section)

    return assessment


def load_section(name):

    return load(name)

