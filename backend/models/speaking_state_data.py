from dataclasses import dataclass, asdict

@dataclass
class SpeakingStateData:
    is_speaking: str
    timestamp: float
