import asyncio
import json
from fastapi import WebSocket
from deepgram import LiveTranscriptionEvents, LiveOptions
from .deepgram_api import DeepgramAPI

class SpeechToTextService:
    def __init__(self, api: DeepgramAPI, model="nova-2", language="en-US"):
        self.api = api
        self.model = model
        self.language = language
        self.dg_connection = None
        self.keep_alive_interval = 5  # Interval in seconds for sending KeepAlive messages

    async def start_transcription(self, websocket: WebSocket):
        """
        Initializes the connection to Deepgram and sets up event handlers.
        """
        self.dg_connection = self.api.create_connection()

        async def on_message(results, **kwargs):
            result = kwargs.get('result') or results
            if not result:
                return

            sentence = result.channel.alternatives[0].transcript
            if sentence:
                print(f"Transcribed text: {sentence}")
                try:
                    await websocket.send_text(sentence)
                except Exception as e:
                    print(f"WebSocket connection error: {e}")

        async def on_open(*args, **kwargs):
            print("Deepgram connection opened.")
            asyncio.create_task(self.send_keep_alive())  # Start sending KeepAlive messages

        async def on_close(*args, **kwargs):
            print("Deepgram connection closed.")

        async def on_error(error, **kwargs):
            print(f"Error: {error}")

        async def on_unhandled(unhandled, **kwargs):
            print(f"Unhandled event: {unhandled}")

        # Register event handlers
        self.dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        self.dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        self.dg_connection.on(LiveTranscriptionEvents.Close, on_close)
        self.dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        self.dg_connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)

        # Setup live transcription options
        options = LiveOptions(
            model=self.model,
            language=self.language,
        )

        print("Connecting to Deepgram for speech-to-text...")
        if not await self.dg_connection.start(options):
            print("Failed to connect to Deepgram")
            return False

        return True

    async def transcribe_speech(self, audio_data: bytes, websocket: WebSocket):
        """
        Sends audio data to Deepgram for transcription and sends the
        transcription back through the WebSocket connection.
        """
        if not self.dg_connection:
            print("No active Deepgram connection. Attempting to start a new transcription session.")
            if not await self.start_transcription(websocket):
                return

        try:
            print("Sending audio data to Deepgram...")
            await self.dg_connection.send(audio_data)
            self.dg_connection = None
        except Exception as e:
            print(f"Error sending data to Deepgram: {e}")
            await self.stop_transcription()

    async def stop_transcription(self):
        if self.dg_connection:
            await self.dg_connection.finish()
            self.dg_connection = None
            print("Finished transcribing speech.")

    async def send_keep_alive(self):
        """
        Periodically sends a KeepAlive message to keep the WebSocket connection alive.
        """
        pass
        # while self.dg_connection:
        #     try:
        #         await asyncio.sleep(self.keep_alive_interval)
        #         keep_alive_msg = json.dumps({"type": "KeepAlive"})
        #         await self.dg_connection.send(keep_alive_msg)
        #         print("Sent KeepAlive message to Deepgram.")
        #     except Exception as e:
        #         print(f"KeepAlive failed: {e}")
        #         break
