import time
import asyncio
import json
import random
from dataclasses import dataclass, asdict
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

@dataclass
class SpokenLanguageData:
    sentence_id: str
    sentence_text: str
    consequential_idx: str
    factuality_idx: str
    controversial_idx: str
    confidence_idx: str
    timestamp: float

async def stream_data_1():
    """ Generator for the first streaming endpoint. """
    while True:
        yield f"data: Stream1 says hello at {time.ctime()}\n\n"
        await asyncio.sleep(5)


@app.get("/stream1")
async def stream1(request: Request):
    """ First streaming endpoint. """
    return StreamingResponse(stream_data_1(), media_type="text/event-stream")


async def stream_data_2():
    """ Generator for the second streaming endpoint. """
    while True:
        yield f"data: Stream2 says hello at {time.ctime()}\n\n"
        await asyncio.sleep(5)


@app.get("/stream2")
async def stream2(request: Request):
    """ Second streaming endpoint. """
    return StreamingResponse(stream_data_2(), media_type="text/event-stream")


async def stream_spoken_language_data():
    """
    Generator for a third streaming endpoint that sends JSON-serialized dataclass
    objects every 5 seconds.
    """
    sentence_id = 0
    while True:
        sentence_id += 1
        # Create a sample SensorReading dataclass instance
        reading = SpokenLanguageData(
            sentence_id = str(sentence_id),
            sentence_text = "Sample Text",
            consequential_idx = "Medium",
            factuality_idx = "Medium",
            controversial_idx = "Medium",
            confidence_idx = "Medium",
            timestamp=time.time()
        )

        # Convert dataclass to a dictionary, then to JSON
        json_str = json.dumps(asdict(reading))

        # SSE format: "data: <JSON string>\n\n"
        # You can also include an 'event:' line or an 'id:' if needed.
        yield f"data: {json_str}\n\n"
        await asyncio.sleep(3)


@app.get("/spoken_language_data_stream")
async def spoken_language_data_stream(request: Request):
    """
    Third streaming endpoint. Sends structured JSON data (from a dataclass)
    every 5 seconds.
    """
    return StreamingResponse(stream_spoken_language_data(), media_type="text/event-stream")