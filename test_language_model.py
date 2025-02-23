from backend.llm.mistral_statement_evaluator import MistralStatementEvaluator

mistral_eval = MistralStatementEvaluator("No background info")

test = input("statement:")
evaluation = mistral_eval.evaluate_statement(test)
print(evaluation)

explanation = mistral_eval.generate_explanation(test, evaluation)
print(explanation)