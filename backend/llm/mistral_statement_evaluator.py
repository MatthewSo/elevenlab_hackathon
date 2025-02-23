from backend.constants.vals import MISTRAL_API_KEY, MISTRAL_MODEL
from backend.llm.context_generators import (
    get_evaluation_context,
    get_explanation_context,
)
from backend.llm.interface.statement_evaluator import (
    StatementEvaluator,
    StatementEvaluation,
)
from mistralai import Mistral
import json

import dotenv

dotenv.load_dotenv()


class MistralStatementEvaluator(StatementEvaluator):
    def __init__(self, background_info: str):
        self.client = Mistral(api_key=MISTRAL_API_KEY)
        self.model = MISTRAL_MODEL
        self.background_info = background_info

    def evaluate_statement(self, statement: str):
        content_str = get_evaluation_context(self.background_info, statement)
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": content_str,
                },
            ],
        )
        response = chat_response.choices[0].message.content
        response_dict = json.loads(response)
        return StatementEvaluation(
            sentence_text=statement,
            consequential_idx=response_dict["consequential_idx"],
            factuality_idx=response_dict["factuality_idx"],
            controversial_idx=response_dict["controversial_idx"],
            confidence_idx=response_dict["confidence_idx"],
        )

    def generate_explanation(self, statement: str, evaluation: StatementEvaluation):
        content_str = get_explanation_context(
            self.background_info, statement, evaluation
        )
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": content_str,
                },
            ],
        )
        return chat_response.choices[0].message.content
