import speech_recognition as sr

async def transcribe(audio_path):
  audio_path = str(audio_path)
  print("AUDIO PATH",audio_path)
  r = sr.Recognizer()

  with sr.AudioFile(audio_path) as source:
    audio_data = r.record(source)

  try:
    text = r.recognize_google(audio_data)
    return text
  except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))