from deepgram import DeepgramClient
from dotenv import load_dotenv

load_dotenv()

class DeepgramAPI:
    """
    Deepgram API client
    - Handles WebSocket connection to Deepgram API
    """
    
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            raise ValueError("Deepgram API Key is required")
        self.api_key = api_key
        self.dg_client = DeepgramClient(api_key)

    def create_connection(self):
        return self.dg_client.listen.asyncwebsocket.v("1")
