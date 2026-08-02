from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Organization:
    """
    Enterprise organization registered in EQMP.
    """

    organization_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    name: str = ""

    business_email: str = ""

    industry: str = ""

    country: str = ""

    website: str = ""

    created_at: datetime = field(default_factory=datetime.utcnow)

    status: str = "Registered"
