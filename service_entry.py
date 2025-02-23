import asyncio
import logging
import time
import json
from dataclasses import asdict
from backend.llm.mistral_statement_evaluator import MistralStatementEvaluator

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from backend.models.spoken_language_data import SpokenLanguageData
import hashlib

import socketio  # pip install "python-socketio[asgi]"
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    DeepgramClientOptions,
)

###############################################################################
# SHARED GLOBAL STATE
###############################################################################
TRANSCRIPTION_GLOBAL_STATE = []

###############################################################################
# DEEPGRAM SETUP
###############################################################################
API_KEY = "2d4bb9e32ba54186720f9ab1320076eaabd6a4c0"  # or from env
config = DeepgramClientOptions(
    verbose=logging.WARN,
    options={"keepalive": "true"},
)
deepgram = DeepgramClient(API_KEY, config)

dg_connection = None


def initialize_deepgram_connection():
    global dg_connection
    dg_connection = deepgram.listen.live.v("1")

    def on_open(this_conn, open_data, **kwargs):
        print("Deepgram connection opened:", open_data)

    def on_message(this_conn, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            speaker = result.channel.alternatives[0].words[0].speaker
            text = f"Speaker {speaker}: {transcript}"
            print(text)

            # Call mistral.
            evaluation = MISTRAL_EVALUATOR.evaluate_statement(text)

            # Generate a unique sentence_id by hashing the text
            hash_object = hashlib.sha256(text.encode())
            sentence_id = hash_object.hexdigest()

            # Use the first 8 characters of the hash as the sentence_id
            idx = sentence_id[:8]

            data = SpokenLanguageData(
                sentence_id=sentence_id,
                sentence_text=text,
                speaker=speaker,
                consequential_idx=evaluation.consequential_idx,
                factuality_idx=evaluation.factuality_idx,
                controversial_idx=evaluation.controversial_idx,
                confidence_idx=evaluation.confidence_idx,
                timestamp=time.time(),
            )
            print(data)
            TRANSCRIPTION_GLOBAL_STATE.append(data)

            # TRANSCRIPTION_GLOBAL_STATE.append(
            #     {
            #         "speaker": speaker,
            #         "transcript": transcript,
            #     }
            # )

    def on_close(this_conn, close_data, **kwargs):
        print("Deepgram connection closed:", close_data)

    def on_error(this_conn, error_data, **kwargs):
        print("Deepgram error:", error_data)

    dg_connection.on(LiveTranscriptionEvents.Open, on_open)
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Close, on_close)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)

    options = LiveOptions(
        model="nova-3",
        language="en-US",
        punctuate=True,
        diarize=True,
    )

    if dg_connection.start(options) is False:
        print("Failed to start Deepgram connection")
        exit()


###############################################################################
# SOCKET.IO (ASGI MODE) SETUP
###############################################################################
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[
        "http://localhost:9000",
        "http://localhost:8000",
        "http://127.0.0.1:9000",
        "http://127.0.0.1:8000",
    ],  # adjust as needed
)

###############################################################################
# FASTAPI APP
###############################################################################
app = FastAPI()

MISTRAL_EVALUATOR = MistralStatementEvaluator("No background info")


@app.get("/spoken_language_data_stream")
async def spoken_language_data_stream(request: Request):
    """
    SSE endpoint that streams transcripts from TRANSCRIPTION_GLOBAL_STATE
    as they arrive.
    """

    async def event_generator():
        idx = 0
        while True:
            # If there's a new transcript in the global list, yield it
            if idx < len(TRANSCRIPTION_GLOBAL_STATE):
                data = TRANSCRIPTION_GLOBAL_STATE[idx]
                idx += 1

                json_str = json.dumps(asdict(data))
                yield f"data: {json_str}\n\n"
            else:
                # No new data yet, wait a bit
                await asyncio.sleep(0.3)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


###############################################################################
# SOCKET.IO EVENT HANDLERS
###############################################################################
@sio.event
async def connect(sid, environ, auth):
    print(f"[Socket.IO] Client connected: {sid}")


@sio.on("toggle_transcription")
async def handle_toggle_transcription(sid, data):
    action = data.get("action")
    if action == "start":
        print("[Socket.IO] Starting Deepgram connection...")
        initialize_deepgram_connection()


@sio.on("audio_stream")
async def handle_audio_stream(sid, audio_data):
    """
    Called repeatedly by the client to send raw audio data chunks.
    """
    if dg_connection:
        dg_connection.send(audio_data)


@sio.event
async def disconnect(sid):
    print(f"[Socket.IO] Client disconnected: {sid}")


###############################################################################
# COMBINE FastAPI + SocketIO INTO ONE ASGI APP
###############################################################################
# This wraps our FastAPI app with Socket.IO's ASGIApp
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

###############################################################################
# LAUNCH INSTRUCTIONS
###############################################################################
# You do NOT call `socketio.run()` in this scenario.
# Instead, you run via uvicorn (or hypercorn) from the command line:
#
#   uvicorn my_app:socket_app --host 0.0.0.0 --port 8000 --reload
#
# (where `my_app` is this file's name without `.py`, and `socket_app` is
# the ASGI instance defined at the bottom).
###############################################################################
