import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000
CHANNELS = 1
MIN_DURATION_SECONDS = 0.3


class AudioRecorder:
    def __init__(self):
        self._frames = []
        self._stream = None
        self.is_recording = False

    def start(self):
        self._frames = []
        self.is_recording = True
        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()

    def _callback(self, indata, frames, time, status):
        if self.is_recording:
            self._frames.append(indata.copy())

    def stop(self):
        self.is_recording = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        if not self._frames:
            return None

        audio = np.concatenate(self._frames, axis=0).flatten()

        duration = len(audio) / SAMPLE_RATE
        if duration < MIN_DURATION_SECONDS:
            return None

        return audio, SAMPLE_RATE
