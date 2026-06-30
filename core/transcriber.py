import os
import tempfile
import wave
import numpy as np
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "whisper-large-v3-turbo"


class Transcriber:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_key_here":
            raise ValueError("GROQ_API_KEY not set in .env file")
        self.client = Groq(api_key=api_key)

    def transcribe(self, audio: np.ndarray, sample_rate: int) -> str | None:
        pcm = (audio * 32767).astype(np.int16)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            with wave.open(tmp_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(pcm.tobytes())

        try:
            with open(tmp_path, "rb") as f:
                result = self.client.audio.transcriptions.create(
                    file=("audio.wav", f, "audio/wav"),
                    model=MODEL,
                    response_format="text",
                )
            text = result.strip() if isinstance(result, str) else result.text.strip()
            return text if text else None
        finally:
            os.unlink(tmp_path)
