# VoiceTyper

A lightweight macOS menu bar app that records audio via a global hotkey, transcribes it with Groq's Whisper API, and types the result wherever your cursor is.

## Prerequisites

- Python 3.11+
- macOS (Apple Silicon recommended)
- A free Groq API key — get one at [console.groq.com](https://console.groq.com)

## Setup

```bash
# 1. Clone / enter the project
cd voicetyper

# 2. Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
#    Edit .env and replace "your_key_here" with your actual Groq API key
nano .env   # or open in any editor
```

## macOS Permissions

VoiceTyper needs two permissions:

### Microphone
System Settings → Privacy & Security → Microphone → enable Terminal (or your Python binary).

### Accessibility (required for text injection)
System Settings → Privacy & Security → Accessibility → click `+` → add `/Applications/Utilities/Terminal.app` (or your Python binary path) → toggle it ON.

> If you run via a virtual environment, you may need to add the `python3` binary inside `.venv/bin/` instead of Terminal.

Restart the app after granting permissions.

## How to Use

```bash
python app.py
```

A microphone icon (🎙) appears in your menu bar.

1. Click into any text field (TextEdit, browser address bar, VS Code, Spotlight, etc.)
2. Hold **⌘ + Shift + Space** and speak
3. Release the hotkey — text is transcribed and pasted at your cursor

The icon turns 🔴 while recording.

## Launch on Login

Create a launchd plist so the app starts automatically:

```bash
cat > ~/Library/LaunchAgents/com.voicetyper.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.voicetyper</string>
  <key>ProgramArguments</key>
  <array>
    <!-- Replace with the absolute path to your python binary -->
    <string>/path/to/voicetyper/.venv/bin/python</string>
    <string>/path/to/voicetyper/app.py</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <false/>
  <key>StandardOutPath</key>
  <string>/tmp/voicetyper.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/voicetyper.err</string>
</dict>
</plist>
EOF

# Load it
launchctl load ~/Library/LaunchAgents/com.voicetyper.plist
```

Update the `ProgramArguments` paths to match your actual install location (`which python` inside the venv).

## Test Checklist

After `python app.py`:

- [ ] 🎙 icon appears in menu bar
- [ ] Menu shows Status, Hotkey info, and Quit
- [ ] Open TextEdit → hold ⌘⇧Space → speak → release → text appears
- [ ] Icon turns 🔴 during recording, returns to 🎙 after
- [ ] Test in: TextEdit, Chrome address bar, Spotlight, VS Code terminal
- [ ] Short press (< 0.3s) does nothing (no empty paste)
- [ ] Kill internet → Groq error shows as notification, app keeps running
