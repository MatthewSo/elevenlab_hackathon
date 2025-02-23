from backend.llm.mistral_statement_evaluator import MistralStatementEvaluator
from backend.voice.elevenlabs_speech_generator import ElevenLabsSpeechGenerator

mistral_eval = MistralStatementEvaluator("No background info")

test = input("statement:")
evaluation = mistral_eval.evaluate_statement(test)
print(evaluation)

explanation = mistral_eval.generate_explanation(test, evaluation)
print(explanation)

speech_generator = ElevenLabsSpeechGenerator()

speech_generator.generate_speech(explanation)