import time
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

async def stream_data_1():
    """
    Generator function for the first streaming endpoint.
    Yields a new event every 5 seconds.
    """
    while True:
        yield f"data: Stream1 says hello at {time.ctime()}\n\n"
        await asyncio.sleep(5)


@app.get("/stream1")
async def stream1(request: Request):
    """
    First streaming endpoint. Returns an SSE (text/event-stream) response.
    """
    return StreamingResponse(stream_data_1(), media_type="text/event-stream")


async def stream_data_2():
    """
    Generator function for the second streaming endpoint.
    Yields a new event every 5 seconds.
    """
    while True:
        yield f"data: Stream2 says hello at {time.ctime()}\n\n"
        await asyncio.sleep(5)


@app.get("/stream2")
async def stream2(request: Request):
    """
    Second streaming endpoint. Also returns an SSE (text/event-stream) response.
    """
    return StreamingResponse(stream_data_2(), media_type="text/event-stream")