import threading
import rumps
from pynput import keyboard
from core.recorder import AudioRecorder
from core.transcriber import Transcriber
from core.injector import inject_text

HOTKEY = {keyboard.Key.alt_r}

ICON_READY = "🎙"
ICON_RECORDING = "🔴"


class VoiceTyperApp(rumps.App):
    def __init__(self):
        super().__init__(ICON_READY, quit_button=None)

        self.status_item = rumps.MenuItem("Status: Ready")
        self.status_item.set_callback(None)

        self.hotkey_item = rumps.MenuItem("Hotkey: Right ⌥")
        self.hotkey_item.set_callback(None)

        self.menu = [
            self.status_item,
            None,
            self.hotkey_item,
            None,
            rumps.MenuItem("Quit", callback=self._quit),
        ]

        self.recorder = AudioRecorder()
        try:
            self.transcriber = Transcriber()
        except ValueError as e:
            rumps.alert(
                title="VoiceTyper — Missing API Key",
                message=str(e) + "\n\nEdit .env and restart the app.",
            )
            self.transcriber = None

        self._held_keys = set()
        self._recording = False

        self._start_hotkey_listener()

    def _start_hotkey_listener(self):
        t = threading.Thread(target=self._run_listener, daemon=True)
        t.start()

    def _run_listener(self):
        try:
            with keyboard.Listener(
                on_press=self._on_press, on_release=self._on_release
            ) as listener:
                listener.join()
        except Exception as e:
            print(f"Hotkey listener error: {e}")
            rumps.notification(
                title="VoiceTyper",
                subtitle="Hotkey listener failed",
                message="Check Accessibility permissions and restart.",
            )

    def _normalize_key(self, key):
        if hasattr(key, "char") and key.char == " ":
            return keyboard.KeyCode.from_char(" ")
        return key

    def _on_press(self, key):
        self._held_keys.add(self._normalize_key(key))
        if HOTKEY.issubset(self._held_keys) and not self._recording:
            self._recording = True
            self._start_recording()

    def _on_release(self, key):
        self._held_keys.discard(self._normalize_key(key))
        if self._recording and not HOTKEY.issubset(self._held_keys):
            self._recording = False
            self._stop_and_transcribe()

    def _start_recording(self):
        self.title = ICON_RECORDING
        self.status_item.title = "Status: Recording..."
        try:
            self.recorder.start()
        except Exception as e:
            print(f"Mic error: {e}")
            rumps.notification(
                title="VoiceTyper",
                subtitle="Microphone error",
                message=str(e),
            )
            self._recording = False
            self.title = ICON_READY
            self.status_item.title = "Status: Ready"

    def _stop_and_transcribe(self):
        self.title = ICON_READY
        self.status_item.title = "Status: Transcribing..."

        result = self.recorder.stop()

        if result is None:
            self.status_item.title = "Status: Ready"
            return

        audio, sample_rate = result

        def _transcribe():
            try:
                if self.transcriber is None:
                    print("ERROR: No transcriber (API key missing?)")
                    return
                print(f"Transcribing {len(audio)/sample_rate:.1f}s of audio...")
                text = self.transcriber.transcribe(audio, sample_rate)
                print(f"Transcribed: '{text}'")
                if text:
                    inject_text(text)
                    print("Injected.")
                else:
                    print("Empty transcription, nothing injected.")
            except Exception as e:
                print(f"Transcription error: {e}")
                rumps.notification(
                    title="VoiceTyper",
                    subtitle="Transcription failed",
                    message=str(e),
                )
            finally:
                self.status_item.title = "Status: Ready"

        threading.Thread(target=_transcribe, daemon=True).start()

    def _quit(self, _):
        rumps.quit_application()


if __name__ == "__main__":
    VoiceTyperApp().run()
