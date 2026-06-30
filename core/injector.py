import time
import pyperclip
from pynput.keyboard import Controller, Key

_keyboard = Controller()

def inject_text(text: str) -> None:
    if not text:
        return
    pyperclip.copy(text)
    time.sleep(0.3)
    # Explicitly release Option before pasting to avoid Cmd+Option+V
    _keyboard.release(Key.alt)
    _keyboard.release(Key.alt_r)
    time.sleep(0.05)
    with _keyboard.pressed(Key.cmd):
        _keyboard.press("v")
        _keyboard.release("v")
