import os
import dotenv

dotenv.load_dotenv()

MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MISTRAL_MODEL = "mistral-small-latest"
ELEVEN_LABS_API_KEY = os.environ["ELEVEN_LABS_API_KEY"]
