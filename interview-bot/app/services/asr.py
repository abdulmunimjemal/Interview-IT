from faster_whisper import WhisperModel
from pathlib import Path

model_size = "small"

model = WhisperModel(model_size)

async def transcribe(audio_path: Path) -> str:
    _segments, _ = model.transcribe(audio_path)
    segments = list(segments)
    transcription = " ".join([segment["text"] for segment in segments])
    return transcription