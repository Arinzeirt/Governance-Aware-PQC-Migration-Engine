from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Project:
    """
    Assessment project belonging to an organization.
    """

    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    organization_id: str = ""

    name: str = ""

    repository_type: str = ""

    repository: str = ""

    created_at: datetime = field(default_factory=datetime.utcnow)

    status: str = "Assessment"
