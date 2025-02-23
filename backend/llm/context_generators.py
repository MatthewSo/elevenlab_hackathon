from backend.llm.interface.statement_evaluator import StatementEvaluation


def get_evaluation_context(background_info: str, statement: str):
    context = """You are an intelligent system that must evaluate how correct/true facts are based on a given background of knowledge.
You will be given a bunch of background information on a topic and a statement that you must evaluate.
The statement might not be at all relevant to the background information, but you must still evaluate it.
You may use your own knowledge to evaluate a statement, but should defer to the background information if it contradicts your knowledge.

You will be asked to rank the statement on the following scales, with each criterion rated on a numerical scale from 0 to 1:
- Consequentiality: How important is the statement in the context of the background information? [0.0 to 1.0]
- Factualness: How true is the statement in the context of the background information? [0.0 to 1.0]
- Controversiality: How controversial is the statement in the context of the background information? [0.0 to 1.0]
- Confidence: How confident are you in your evaluation of the statement? [0.0 to 1.0]

You must ONLY provide your response in valid JSON format. Your answer will be immediately parsed as JSON. Here are some examples:
- {"consequential_idx": 0.2, "factuality_idx": 0.5, "controversial_idx": 0.9, "confidence_idx": 0.2}
- {"consequential_idx": 1.0, "factuality_idx": 1.0, "controversial_idx": 0.1, "confidence_idx": 1.0}
- {"consequential_idx": 0.5, "factuality_idx": 0.0, "controversial_idx": 0.5, "confidence_idx": 0.5}

Qualifiers, like "I think" or "I believe" in the statement can be ignored. You should evaluate the statement as if it were a fact.
Here are some examples of statements you might be asked to evaluate with the scores you might give:
- "The sky is blue" - {"consequential_idx": 0.2, "factuality_idx": 1.0, "controversial_idx": 0.1, "confidence_idx": 1.0}
- "The sky is green" - {"consequential_idx": 0.2, "factuality_idx": 0.0, "controversial_idx": 0.9, "confidence_idx": 0.2}
- "I think the sky is green" - {"consequential_idx": 0.2, "factuality_idx": 0.0, "controversial_idx": 0.9, "confidence_idx": 0.2}
- "Pizza was invented in Italy" - {"consequential_idx": 0.2, "factuality_idx": 1.0, "controversial_idx": 0.1, "confidence_idx": 1.0}
- "Pizza was invented in China" - {"consequential_idx": 0.2, "factuality_idx": 0.0, "controversial_idx": 0.9, "confidence_idx": 0.2}
- "The Government is run by aliens" - {"consequential_idx": 0.2, "factuality_idx": 0.0, "controversial_idx": 0.9, "confidence_idx": 1.0}
- "The COVID-19 vaccine is safe" - {"consequential_idx": 1.0, "factuality_idx": 1.0, "controversial_idx": 0.1, "confidence_idx": 1.0}
- "The COVID-19 vaccine gives you autism" - {"consequential_idx": 1.0, "factuality_idx": 0.0, "controversial_idx": 0.9, "confidence_idx": 1.0}
"""

    context += f"""
Below is the background information you will be given:
----------
{background_info}
----------

You must evaluate the following statement:
----------
{statement}
----------

Your response must be raw JSON. DO NOT INCLUDE STRING CHARACTERS OUTSIDE OF THE JSON OBJECT.
"""
    return context


def get_explanation_context(
    background_info: str, statement: str, evaluation: StatementEvaluation
):
    context = """You are part of an intelligent system that must evaluate how correct/true facts are based on a given background of knowledge.
You will be given a bunch of background information on a topic and a statement that you must evaluate.
You have already evaluated the statement based on the background information and must now provide an explanation for why you think it is or is not factual.
You may use your own knowledge to evaluate a statement, but should defer to the background information if it contradicts your knowledge.

You have already ranked the statement on the following scales, with each criterion rated on a numerical scale from 0 to 1:
- Consequentiality: How important is the statement in the context of the background information? [0.0 to 1.0]
- Factualness: How true is the statement in the context of the background information? [0.0 to 1.0]
- Controversiality: How controversial is the statement in the context of the background information? [0.0 to 1.0]
- Confidence: How confident are you in your evaluation of the statement? [0.0 to 1.0]

Now you must provide an explanation of why you think the statement is or is not factual.  

Here are some examples of explanations you might give:
    - Example 1:
        - Statement: "The sky is blue"
        - Evaluation: {"consequential_idx": 0.2, "factuality_idx": 1.0, "controversial_idx": 0.1, "confidence_idx": 1.0}
        - Explanation: "It is a well-known fact that the sky is blue. The sky appears blue because of the way the Earth's atmosphere scatters sunlight."
    - Example 2:
        - Statement: "The sky is green"
        - Evaluation: {"consequential_idx": 0.2, "factuality_idx": 0.0, "controversial_idx": 0.9, "confidence_idx": 0.2}
        - Explanation: "The sky is not green. The sky appears blue because of the way the Earth's atmosphere scatters sunlight. Green is not a color that the sky can appear."
    - Example 3:
        - Statement: "I think the sky is green"
        - Evaluation: {"consequential_idx": 0.2, "factuality_idx": 0.0, "controversial_idx": 0.9, "confidence_idx": 0.2}
        - Explanation: "The sky is not green. The sky appears blue because of the way the Earth's atmosphere scatters sunlight. Green is not a color that the sky can appear."
    - Example 4:
        - Statement: "Pizza was invented in Italy"
        - Evaluation: {"consequential_idx": 0.2, "factuality_idx": 1.0, "controversial_idx": 0.1, "confidence_idx": 1.0}
        - Explanation: "Pizza was invented in Italy. The modern pizza was invented in Naples, Italy, in the 18th century."
    - Example 5:
        - Statement: "Pizza was invented in China"
        - Evaluation: {"consequential_idx": 0.2, "factuality_idx": 0.0, "controversial_idx": 0.9, "confidence_idx": 0.2}
        - Explanation: "Pizza was not invented in China. The modern pizza was invented in Naples, Italy, in the 18th century."
        """
    context += f"""
Below is the background information you were given:
----------
{background_info}
----------
"""
    context += f"""
You evaluated the following statement:
----------
{statement}
----------
"""
    context += f"""
You evaluated the statement as follows:
- Consequentiality: {evaluation.consequential_idx}
- Factualness: {evaluation.factuality_idx}
- Controversiality: {evaluation.controversial_idx}
- Confidence: {evaluation.confidence_idx}
"""
    context += """
Your explanation must be raw text. DO NOT INCLUDE STRING CHARACTERS OUTSIDE OF THE TEXT.
Your response should be no longer than 2 sentences.
Provide your answer now.
    """
    return context
