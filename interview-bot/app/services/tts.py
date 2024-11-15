import edge_tts
from pathlib import Path
import tempfile


async def synthesize_audio(text: str) -> Path:
    output_path = Path(tempfile.mktemp(suffix=".wav"))
    tts = edge_tts.Communicate(text, "en-US-AriaNeural")
    await tts.save(output_path)
    return output_path