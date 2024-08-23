from fastapi import APIRouter, WebSocket
from ..services.websocket_handler import WebSocketHandler
from ..services.message_processor import MessageProcessor
from ..services.deepgram_api import DeepgramAPI
from ..services.text_to_speech_service import TextToSpeechService
from ..services.speech_to_text_service import SpeechToTextService
import os
from deepgram import DeepgramClient
from dotenv import load_dotenv

load_dotenv()

websocket_endpoint = APIRouter()

api_key = os.getenv("DEEPGRAM_API_KEY")
if not api_key:
    raise ValueError("Deepgram API Key is required")

# Setup services
deepgram_api = DeepgramAPI(api_key)
deepgram_client = DeepgramClient(api_key)
if not deepgram_api:
    print("Failed to initialize Deepgram API.")
    exit()
tts_service = TextToSpeechService(deepgram_client)
stt_service = SpeechToTextService(deepgram_api)
message_processor = MessageProcessor(tts_service=tts_service, stt_service=stt_service)
websocket_handler = WebSocketHandler(message_processor=message_processor)

@websocket_endpoint.websocket("/")
async def websocket_route(websocket: WebSocket):
    await websocket_handler.handle(websocket)
