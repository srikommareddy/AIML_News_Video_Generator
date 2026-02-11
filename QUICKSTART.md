# Quick Start Guide - AI/ML Video Generator

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

```bash
# Install Python packages
pip install -r requirements.txt

# Install FFmpeg (if not already installed)
# Mac:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Windows: Download from https://ffmpeg.org/download.html
```

### Step 2: Configure API Key (1 minute)

1. Get your Anthropic API key from https://console.anthropic.com
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

### Step 3: Run Setup Check (1 minute)

```bash
python setup.py
```

This will verify your environment is ready.

### Step 4: Launch the App (1 minute)

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📹 Create Your First Video (10 minutes)

### Workflow:

1. **Fetch News** (2 min)
   - Click "Fetch News Articles"
   - Select 3-5 articles by checking boxes

2. **Generate Script** (3 min)
   - Set duration to 3-5 minutes
   - Choose tone (try "Professional" first)
   - Click "Generate Script"
   - Review and edit if needed

3. **Create Video** (5 min)
   - Use "gTTS (Free)" for voice (no API key needed)
   - Click "Generate Video"
   - Wait for processing
   - Download your video!

## 💡 Pro Tips

- Start with 3-4 articles for a 3-5 minute video
- Edit the script to add your personal touch
- Use gTTS for testing, upgrade to OpenAI/ElevenLabs later
- Save your work frequently using the Settings tab

## 🐛 Troubleshooting

**App won't start?**
- Run `python setup.py` to check for issues

**No API key?**
- The app will work with mock data for testing
- Get a real key from https://console.anthropic.com

**Video generation fails?**
- Check that FFmpeg is installed: `ffmpeg -version`
- Make sure output directory exists and is writable

## 📚 Need More Help?

See the full [README.md](README.md) for detailed documentation.

---

**You're ready to create AI/ML videos! 🎬**
