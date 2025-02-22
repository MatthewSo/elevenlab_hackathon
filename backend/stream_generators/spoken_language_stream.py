from backend.models.spoken_language_data import SpokenLanguageData
import time
import asyncio
import json
from dataclasses import dataclass, asdict

async def stream_spoken_language_data():
    sentence_id = 0
    while True:
        sentence_id += 1
        data = SpokenLanguageData(
            sentence_id = str(sentence_id),
            sentence_text = "Sample Text",
            consequential_idx = "Medium",
            factuality_idx = "Medium",
            controversial_idx = "Medium",
            confidence_idx = "Medium",
            timestamp=time.time()
        )

        json_str = json.dumps(asdict(data))

        yield f"data: {json_str}\n\n"
        await asyncio.sleep(3)