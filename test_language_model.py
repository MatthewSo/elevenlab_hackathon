from backend.llm.mistral_statement_evaluator import MistralStatementEvaluator

mistral_eval = MistralStatementEvaluator("No background info")

test = input("statement:")
mistral_eval.evaluate_statement(test)