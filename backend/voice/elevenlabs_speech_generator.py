from elevenlabs.client import ElevenLabs
from elevenlabs import play

from backend.constants.vals import ELEVEN_LABS_API_KEY
from backend.voice.interface.speech_generator import SpeechGenerator


class ElevenLabsSpeechGenerator(SpeechGenerator):
    def __init__(self):
        self._client = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)

    def generate_speech(self, text: str) -> str:
        audio = self._client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_128",
        )

        play(audio)