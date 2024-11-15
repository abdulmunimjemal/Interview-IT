from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from app.models import AudioResponse
from app.services import asr, llm, tts
from pathlib import Path
import tempfile

app = FastAPI()

@app.post("/converse", response_model=AudioResponse)
async def converse(file: UploadFile = File(...)):

    # CHeck file type
    if file.content_type not in ["audio/wav", "audio/x-wav", "audio/vnd.wav", "audio/mpeg"]:
        raise HTTPException(status_code=415, detail="Unsupported media type")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_audio_path = Path(tmp.name)
    
    # Step 1: Tramscribe the audio
    transcription = await asr.transcribe(tmp_audio_path)
    # Step 2: Generate the response
    response_text = await llm.generate_response(transcription)
    # Step 3: Generate the audio response
    audio_output_path = await tts.synthesize_audio(response_text)

    return FileResponse(audio_output_path, media_type="audio/wav", filename="response.wav")