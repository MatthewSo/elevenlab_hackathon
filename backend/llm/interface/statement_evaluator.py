from abc import ABC
from dataclasses import dataclass

@dataclass
class StatementEvaluation:
    sentence_text: str
    consequential_idx: str
    factuality_idx: str
    controversial_idx: str
    confidence_idx: str


class StatementEvaluator(ABC):
    def evaluate_statement(self, statement: str):
        pass

    def generate_explanation(self, statement: str, evaluation: StatementEvaluation):
        pass