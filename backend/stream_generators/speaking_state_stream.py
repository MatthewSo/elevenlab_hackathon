from backend.models.speaking_state_data import SpeakingStateData
import time
import asyncio
import json
from dataclasses import dataclass, asdict

async def stream_speaking_state_data():
    sentence_id = 0
    while True:
        sentence_id += 1
        reading = SpeakingStateData(
            is_speaking = "True" if sentence_id % 2 == 0 else "False",
            timestamp=time.time()
        )

        json_str = json.dumps(asdict(reading))

        yield f"data: {json_str}\n\n"
        await asyncio.sleep(3)