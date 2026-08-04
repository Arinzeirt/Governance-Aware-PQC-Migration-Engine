from .loader import load_markdown
from .models import ResearchBrief


OVERVIEW = ResearchBrief(

    category="Quantum Intelligence Brief",

    headline="HARVEST NOW,\nDECRYPT LATER.",

    message=load_markdown(
        "overview.md",
    ),

    reading_time="20 seconds",

    image="assets/illustrations/research/overview.png",

)


TECHNOLOGY = ResearchBrief(

    category="Technology Intelligence Brief",

    headline="YOU CANNOT\nMIGRATE\nWHAT YOU\nCANNOT SEE.",

    message=load_markdown(
        "technology.md",
    ),

    reading_time="18 seconds",

    image="assets/illustrations/research/technology.png",

)


CRYPTOGRAPHY = ResearchBrief(

    category="Cryptography Intelligence Brief",

    headline="UNKNOWN\nCRYPTOGRAPHY\nIS YOUR\nBIGGEST RISK.",

    message=load_markdown(
        "cryptography.md",
    ),

    reading_time="18 seconds",

    image="assets/illustrations/research/cryptography.png",

)


CONFIGURATION = ResearchBrief(

    category="Governance Intelligence Brief",

    headline="GOVERNANCE\nDECIDES\nSUCCESS.",

    message=load_markdown(
        "configuration.md",
    ),

    reading_time="15 seconds",

    image="assets/illustrations/research/configuration.png",

)
