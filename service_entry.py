import asyncio
import logging
import time
import json
from dataclasses import asdict
from backend.llm.mistral_statement_evaluator import MistralStatementEvaluator
from backend.models.speaking_state_data import SpeakingStateData
from backend.stream_generators.speaking_state_stream import stream_speaking_state_data
from backend.voice.elevenlabs_speech_generator import ElevenLabsSpeechGenerator
from elevenlabs import play
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from backend.models.spoken_language_data import SpokenLanguageData
import hashlib
import threading
from queue import Queue
from backend.models.speaking_state_data import SpeakingStateData
from dataclasses import dataclass
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
HIGH_ALERT_AUDIO_MAP = {}
TRANSCRIPTION_EVALUATION_MAP = {}
TRANSCRIPTION_TEXT_MAP = {}
SPEAKER_GLOBAL_STATE = []

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

# Initialize a task queue
high_alert_task_queue = Queue()


# If the transcript is worth alerting, then add it to the global state to be explained,
# and then generate an eleven labs audio file.
def is_alertable(evaluation):
    return (
        evaluation.factuality_idx < 0.1
        and evaluation.consequential_idx > 0.1
        and evaluation.confidence_idx > 0.8
    )


def is_warning(evaluation):
    return (
        evaluation.factuality_idx < 0.5
        and evaluation.consequential_idx > 0.3
        and evaluation.confidence_idx > 0.8
    )


def is_good(evaluation):
    return (
        evaluation.factuality_idx > 0.9
        # and evaluation.consequential_idx < 0.3
        and evaluation.confidence_idx > 0.8
    )


def get_color(evaluation):
    if is_alertable(evaluation):
        return "red"
    if is_warning(evaluation):
        return "yellow"
    if is_good(evaluation):
        return "green"
    return "black"


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
            evaluation = MISTRAL_EVALUATOR.evaluate_statement(transcript)

            # Generate a unique sentence_id by hashing the text
            hash_object = hashlib.sha256(text.encode())
            sentence_id = hash_object.hexdigest()

            # Use the first 8 characters of the hash as the sentence_id
            idx = sentence_id[:8]

            alert = is_alertable(evaluation)
            color = get_color(evaluation)

            data = SpokenLanguageData(
                sentence_id=sentence_id,
                sentence_text=text,
                speaker=speaker,
                consequential_idx=evaluation.consequential_idx,
                factuality_idx=evaluation.factuality_idx,
                controversial_idx=evaluation.controversial_idx,
                confidence_idx=evaluation.confidence_idx,
                timestamp=time.time(),
                alert=alert,
                color=color,
            )
            print(data)
            TRANSCRIPTION_GLOBAL_STATE.append(data)
            TRANSCRIPTION_EVALUATION_MAP[sentence_id] = data
            TRANSCRIPTION_TEXT_MAP[sentence_id] = transcript

            # Add task to the queue
            high_alert_task_queue.put((sentence_id, text, evaluation))

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
ELEVEN_LABS_SPEECH_GENERATOR = ElevenLabsSpeechGenerator()


@app.get("/speaking_state_data_stream")
async def speaking_language_data_stream(request: Request):
    """
    Third streaming endpoint. Sends structured JSON data (from a dataclass)
    every 5 seconds.
    """
    async def event_generator():
        idx = 0
        while True:
            if idx < len(SPEAKER_GLOBAL_STATE):
                data = SPEAKER_GLOBAL_STATE[idx]
                SPEAKER_GLOBAL_STATE.append(SpeakingStateData(is_speaking="True", is_listening="False", color="blue", is_moving="True", timestamp=time.time()))

                idx += 1

                json_str = json.dumps(asdict(data))
                SPEAKER_GLOBAL_STATE.append(SpeakingStateData(is_speaking="True", is_listening="False", color="blue", is_moving="False", timestamp=time.time()))
                yield f"data: {json_str}\n\n"
            else:
                # No new data yet, wait a bit
                await asyncio.sleep(0.2)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


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

    @app.post("/high_alert_explanation")
    async def high_alert_explanation(request: Request):
        data = await request.json()
        sentence_id = data.get("sentence_id")

        if not sentence_id:
            return {"error": "sentence_id and text are required"}

        if sentence_id in HIGH_ALERT_AUDIO_MAP:
            audio = HIGH_ALERT_AUDIO_MAP[sentence_id]
            play(audio)
        else:
            # Do it now!
            print("Wasn't in the map, generating now...")
            text = TRANSCRIPTION_TEXT_MAP.get(sentence_id)
            evaluation = TRANSCRIPTION_EVALUATION_MAP.get(sentence_id)
            explanation = MISTRAL_EVALUATOR.generate_explanation(text, evaluation)
            audio = ELEVEN_LABS_SPEECH_GENERATOR.generate_speech(explanation)
            SPEAKER_GLOBAL_STATE.append(SpeakingStateData(is_speaking="True", is_listening="False", color="red", is_moving="True", timestamp=time.time()))
            HIGH_ALERT_AUDIO_MAP[sentence_id] = audio
            play(audio)
            SPEAKER_GLOBAL_STATE.append(SpeakingStateData(is_speaking="False", is_listening="False", color="blue", is_moving="False", timestamp=time.time()))


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


def process_high_alert_task_queue():
    while True:
        sentence_id, text, evaluation = high_alert_task_queue.get()
        if is_alertable(evaluation):
            print(f"Processing high alert task queue item for text: {text}")
            explanation = MISTRAL_EVALUATOR.generate_explanation(text, evaluation)

            # Generate an audio file with that explanation and save it to the global state.
            audio = ELEVEN_LABS_SPEECH_GENERATOR.generate_speech(explanation)
            HIGH_ALERT_AUDIO_MAP[sentence_id] = audio

            print(f"Finished processing high alert for text: {text}")

        high_alert_task_queue.task_done()


# Start a thread to process the task queue
threading.Thread(target=process_high_alert_task_queue, daemon=True).start()

###############################################################################
# LAUNCH INSTRUCTIONS
###############################################################################
# You do NOT call `socketio.run()` in this scenario.
# Instead, you run via uvicorn (or hypercorn) from the command line:
#
#   uvicorn service_entry:socket_app --host 0.0.0.0 --port 8000 --reload
#
# (where `my_app` is this file's name without `.py`, and `socket_app` is
# the ASGI instance defined at the bottom).
###############################################################################
