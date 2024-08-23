from fastapi import WebSocket
from .text_to_speech_service import TextToSpeechService
from .speech_to_text_service import SpeechToTextService
import json

class MessageProcessor:
    def __init__(self, tts_service: TextToSpeechService, stt_service: SpeechToTextService):
        self.tts_service = tts_service
        self.stt_service = stt_service

    async def process_json(self, message: str, websocket: WebSocket):
        """
        Process a JSON message received from the WebSocket. This could be a text-to-speech request
        or another command.
        """
        print(f"Received JSON message: {message}")
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            print(f"Parsed message type: {msg_type}")

            if msg_type == "text":
                text = data.get("text", "")
                if text:
                    print(f"Processing text for TTS: {text}")
                    await self.tts_service.generate_speech(text, websocket)
                else:
                    print("Text field is empty or missing.")
            else:
                print(f"Unsupported JSON message type: {msg_type}")
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
        except Exception as e:
            print(f"Error processing JSON message: {e}")

    async def process_audio(self, audio_data: bytes, websocket: WebSocket):
        """
        Process binary audio data received from the WebSocket. This data is likely
        intended for speech-to-text processing.
        """
        print("Received audio data. Passing it to STT service.")
        try:
            await self.stt_service.transcribe_speech(audio_data, websocket)
        except Exception as e:
            print(f"Error processing audio data: {e}")
