from dataclasses import dataclass, asdict


@dataclass
class SpokenLanguageData:
    sentence_id: str
    sentence_text: str
    consequential_idx: str
    factuality_idx: str
    controversial_idx: str
    confidence_idx: str
    timestamp: float
    speaker: str
