from abc import ABC

class SpeechGenerator(ABC):
    def generate_speech(self, text: str):
        pass