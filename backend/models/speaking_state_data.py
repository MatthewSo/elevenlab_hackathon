from dataclasses import dataclass, asdict

@dataclass
class SpeakingStateData:
    is_speaking: str
    is_listening: str
    timestamp: float
