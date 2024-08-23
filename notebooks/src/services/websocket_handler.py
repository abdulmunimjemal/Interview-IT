from fastapi import WebSocket
from src.services.message_processor import MessageProcessor

class WebSocketHandler:
    def __init__(self, message_processor: MessageProcessor):
        self.message_processor = message_processor

    async def handle(self, websocket: WebSocket):
        await websocket.accept()
        print("WebSocket connection accepted.")
        try:
            while True:
                print("Waiting to receive a message...")
                message = await websocket.receive()

                if message['type'] == 'websocket.receive':
                    # Check if it's JSON or binary data
                    if 'text' in message:
                        print("Text message detected. Processing as JSON.")
                        json_message = message['text']
                        await self.message_processor.process_json(json_message, websocket)
                    elif 'bytes' in message:
                        print("Binary data detected. Processing as audio.")
                        audio_data = message['bytes']
                        await self.message_processor.process_audio(audio_data, websocket)
                elif message['type'] == 'websocket.disconnect':
                    print("WebSocket disconnected.")
                    break

        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            print("Closing WebSocket connection.")
            await websocket.close()
