# VoiceTyper (free-wispr)

A lightweight macOS menu bar app that records audio via a global hotkey, transcribes it with Groq's Whisper API, and types the result wherever your cursor is. No Dock icon, no GUI — just a 🎙 in your menu bar.

## Prerequisites

- Python 3.11+ (tested on 3.14)
- macOS (Apple Silicon)
- A free Groq API key — get one at [console.groq.com](https://console.groq.com)

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/dhruvywuvy/free-wispr.git
cd free-wispr

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env   # then open .env and paste your Groq key
```

## macOS Permissions

VoiceTyper needs three permissions. All three must be granted to the **Python binary** that runs the app — the real one, not a symlink.

Find your binary path:
```bash
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
# e.g. /opt/homebrew/Cellar/python@3.14/.../bin/python3.14
```

Then in **System Settings → Privacy & Security**, add that path to each of:

| Permission | Why it's needed |
|---|---|
| **Microphone** | Record your voice |
| **Input Monitoring** | Detect the hotkey globally (across all apps) |
| **Accessibility** | Simulate Cmd+V to paste transcribed text |

Click `+` in each section, press `⌘⇧G` in the file picker, paste the path, and toggle it ON. Restart the app after granting all three.

## How to Use

```bash
source .venv/bin/activate
python app.py
```

A 🎙 icon appears in your menu bar.

1. Click into any text field (TextEdit, browser, VS Code, Spotlight, etc.)
2. Hold **right Option (⌥)** and speak
3. Release — text is transcribed and pasted at your cursor

The icon turns 🔴 while recording.

## Run on Login (no terminal needed)

The included launchd plist starts VoiceTyper automatically at login:

```bash
# Edit the plist to set your actual python path, then:
launchctl load ~/Library/LaunchAgents/com.voicetyper.plist
```

Check logs if something goes wrong:
```bash
tail -f /tmp/voicetyper.log
tail -f /tmp/voicetyper.err
```

## Test Checklist

- [ ] 🎙 icon appears in menu bar (no Dock icon)
- [ ] Hold right ⌥ → icon turns 🔴 → release → text appears in focused field
- [ ] Test in: TextEdit, Chrome address bar, Spotlight, VS Code
- [ ] Short press (< 0.3s) does nothing
- [ ] No internet → notification appears, app keeps running
