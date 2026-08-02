from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Assessment:
    """
    Single assessment execution.
    """

    assessment_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    project_id: str = ""

    readiness_score: int = 0

    risk_level: str = "Unknown"

    inventory_path: str = ""

    report_path: str = ""

    started_at: datetime = field(default_factory=datetime.utcnow)

    completed_at: datetime | None = None
