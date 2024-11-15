from pydantic import BaseModel

class AudioRequest(BaseModel):
    file: bytes

class AudioResponse(BaseModel):
    audio_file: bytes