from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from deepgram import Deepgram
from dotenv import load_dotenv
from typing import Dict, Callable
import os
import asyncio

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="audio_experiments/templates")

DG_API_KEY = "4b66499be18ed3768d51d5f5e4d3fbec68b003e9" # invalidated after the experiment,
# use environment variables later
dg_client = Deepgram(DG_API_KEY)

BUFFER_SIZE = 1024 * 8  # 8 KB buffer size

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/listen")
async def listen(websocket: WebSocket):
    await websocket.accept()
    try:
        deepgram_socket = await process_audio(websocket)
        buffer = bytearray()

        while True:
            data = await websocket.receive_bytes()
            buffer.extend(data)
            
            if len(buffer) >= BUFFER_SIZE:
                deepgram_socket.send(bytes(buffer))
                buffer.clear()
        
    except Exception as e:
        raise Exception(f"Error processing audio: {e}")
        await websocket.send_text(f"Error processing audio: {str(e)}")
    finally:
        await websocket.close()

async def process_audio(fast_socket: WebSocket):
    async def get_transcript(data: Dict) -> None:
        if 'channel' in data:
            transcript = data['channel']['alternatives'][0]['transcript']

            if transcript:
                await fast_socket.send_text(transcript)
    print("Connecting to Deepgram")
    deepgram_socket = await connect_to_deepgram(get_transcript)
    print("Connected to Deepgram")
    print("Conenction Type: ", type(deepgram_socket))
    return deepgram_socket

async def connect_to_deepgram(transcript_received_handler: Callable[[Dict], None]):
    try:
        socket = await dg_client.transcription.live(
            {'punctuate': True, 'interim_results': False,
             'language': 'en-US',
             'smart_format': True,
             'endpointing': 100,
             'no_delay': True,}
             
            )
        socket.registerHandler(socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
        socket.registerHandler(socket.event.TRANSCRIPT_RECEIVED, transcript_received_handler)

        return socket
    except Exception as e:
        raise Exception(f'Could not open socket: {e}')