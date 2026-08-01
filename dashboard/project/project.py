from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AssessmentProject:
    """
    Core domain model for an enterprise cryptographic assessment.
    """

    #
    # Identity
    #

    project_id: str = ""

    name: str = ""

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    status: str = "Created"

    #
    # Assessment Target
    #

    repository: str = ""

    repository_type: str = ""

    #
    # Discovery
    #

    discoveries: list = field(default_factory=list)

    inventory: list = field(default_factory=list)

    #
    # Executive Assessment
    #

    readiness: int = 0

    overall_risk: str = "Unknown"

    #
    # Business Context
    #

    business_profile: dict = field(default_factory=dict)

    #
    # Governance Context
    #

    governance_profile: dict = field(default_factory=dict)

    #
    # Regulatory Context
    #

    regulatory_profile: dict = field(default_factory=dict)

    #
    # Migration Planning
    #

    migration_strategy: dict = field(default_factory=dict)

    #
    # Reports
    #

    reports: list = field(default_factory=list)
