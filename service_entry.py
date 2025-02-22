from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from backend.stream_generators.speaking_state_stream import stream_speaking_state_data
from backend.stream_generators.spoken_language_stream import stream_spoken_language_data

app = FastAPI()

@app.get("/spoken_language_data_stream")
async def spoken_language_data_stream(request: Request):
    """
    Third streaming endpoint. Sends structured JSON data (from a dataclass)
    every 5 seconds.
    """
    return StreamingResponse(stream_spoken_language_data(), media_type="text/event-stream")

@app.get("/speaking_state_data_stream")
async def spoken_language_data_stream(request: Request):
    """
    Third streaming endpoint. Sends structured JSON data (from a dataclass)
    every 5 seconds.
    """
    return StreamingResponse(stream_speaking_state_data(), media_type="text/event-stream")