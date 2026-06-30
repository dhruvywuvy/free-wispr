from setuptools import setup

APP = ["app.py"]
OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "VoiceTyper",
        "CFBundleDisplayName": "VoiceTyper",
        "CFBundleIdentifier": "com.voicetyper",
        "CFBundleVersion": "1.0.0",
        "LSUIElement": True,  # menu bar only, no Dock icon
        "NSMicrophoneUsageDescription": "VoiceTyper needs microphone access to record your voice.",
        "NSAppleEventsUsageDescription": "VoiceTyper needs Accessibility access to type transcribed text.",
    },
    "packages": ["core", "groq", "sounddevice", "numpy", "pyperclip", "pyautogui", "rumps", "dotenv", "pynput"],
}

setup(
    app=APP,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
