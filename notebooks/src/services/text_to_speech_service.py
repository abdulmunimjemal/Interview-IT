from fastapi import WebSocket
from deepgram import DeepgramClient, ClientOptionsFromEnv, SpeakOptions

class TextToSpeechService:
    def __init__(self, dg_client: DeepgramClient):
        self.deepgram = dg_client

    async def generate_speech(self, text: str, websocket: WebSocket):
        print("Establishing connection to Deepgram TTS service...")
        try:
            # Print the text input
            print(f"Text to be synthesized: {text}")

            # Define TTS options and print them
            options = SpeakOptions(
                model="aura-asteria-en",
            )
            print(f"TTS options: {options}")

            # Prepare the text input for TTS and print it
            tts_input = {"text": text}
            print(f"TTS Input: {tts_input}")

            # Call the TTS service and get the response
            response = await self.deepgram.speak.asyncrest.v("1").stream_memory(
                tts_input, options
            )
            print("Connected to Deepgram TTS service. Streaming audio data...")

            # Assuming the response has an attribute `stream_memory` with the audio data
            audio_data = response.stream_memory
            print(f"Audio data received: {len(audio_data.getbuffer())} bytes")
            await websocket.send_bytes(audio_data.getbuffer())
            print("Audio data sent to WebSocket client.")

            print("Finished streaming audio data.")

        except Exception as e:
            print(f"Error during TTS processing: {e}")

        print("TTS processing completed.")
