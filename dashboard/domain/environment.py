from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class EnvironmentSource:

    source_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    name: str = ""

    source_type: str = ""

    status: str = "Not Connected"

    last_sync: datetime | None = None

    provider: str = ""


@dataclass
class Environment:

    """
    Enterprise environment represented within EQMP.

    The environment is the system-of-oversight boundary.
    Discovery sources may contribute evidence to it, but
    no individual vendor owns the environment record.
    """

    environment_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    organization_id: str = ""

    name: str = "Primary Environment"

    status: str = "Not Connected"

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    last_sync: datetime | None = None

    sources: list[EnvironmentSource] = field(
        default_factory=list
    )

    systems: int = 0

    applications: int = 0

    data_assets: int = 0

    cryptographic_assets: int = 0

    certificates: int = 0

    discovery_gaps: int = 0

    def active_sources(self):

        return [
            source
            for source in self.sources
            if source.status == "Connected"
        ]

    @property
    def source_count(self):

        return len(self.active_sources())
