from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchBrief:

    category: str

    headline: str

    message: str

    reading_time: str

    image: str
