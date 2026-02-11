# AI/ML Video Generator for YouTube

An intelligent Streamlit application that helps you create AI/ML news roundup videos for your YouTube channel. Features human-in-the-loop control at every step, from news selection to final video generation.

## 🌟 Features

- **📰 Automated News Fetching**: Uses Claude with web search to find the latest AI/ML news
- **✅ Article Selection**: Human review and selection of news articles
- **✍️ Script Generation**: Claude generates engaging video scripts based on selected articles
- **📝 Script Editing**: Full control to edit and customize scripts before video generation
- **🎙️ Multiple TTS Options**: Support for gTTS (free), OpenAI TTS, and ElevenLabs
- **🎬 Video Generation**: Automated video creation with captions and visuals
- **💾 Save/Load States**: Save your work and continue later
- **🎨 Customizable Styling**: Control colors, fonts, and visual elements

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd aiml_video_agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### 2. Configure API Keys

Edit the `.env` file with your API keys:

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional (depending on TTS choice)
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

**Getting API Keys:**
- **Anthropic**: Sign up at https://console.anthropic.com
- **OpenAI**: Sign up at https://platform.openai.com
- **ElevenLabs**: Sign up at https://elevenlabs.io

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 User Guide

### Workflow

#### Step 1: Fetch News
1. Navigate to the "Fetch News" tab
2. Customize the search query if needed (default: "artificial intelligence machine learning")
3. Set the number of articles to fetch (3-20)
4. Click "Fetch News Articles"
5. Review the fetched articles
6. Select the articles you want to include by checking the boxes

#### Step 2: Generate Script
1. Go to the "Generate Script" tab
2. Set your preferred video duration (2-15 minutes)
3. Choose the tone (Professional, Casual, Enthusiastic, Educational)
4. Enter your channel name
5. Click "Generate Script"
6. Review and edit the generated script as needed
7. Download the script if you want to save it separately

#### Step 3: Create Video
1. Move to the "Create Video" tab
2. Configure voice settings:
   - Choose TTS provider (gTTS is free and works without API keys)
   - Select voice options
3. Customize visual settings:
   - Background color
   - Text color
   - Font size
   - Enable/disable captions
4. Click "Generate Video"
5. Wait for video generation (may take a few minutes)
6. Preview the video in the browser
7. Download the final video

#### Step 4: Settings
- Save your current state (articles, script) for later
- Load previously saved states
- Clear all data to start fresh
- Configure output directories

## 🔧 Technical Details

### Project Structure

```
aiml_video_agent/
├── app.py                 # Main Streamlit application
├── news_fetcher.py        # News fetching with Claude & web search
├── script_generator.py    # Script generation with Claude API
├── video_generator.py     # Video creation with MoviePy & TTS
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

### Dependencies

**Core:**
- `streamlit`: Web interface
- `anthropic`: Claude API for news fetching and script generation

**Text-to-Speech:**
- `gtts`: Free Google TTS (no API key needed)
- `openai`: OpenAI TTS (requires API key)
- `elevenlabs`: ElevenLabs TTS (requires API key)

**Video Generation:**
- `moviepy`: Video editing and composition
- `pillow`: Image processing

### System Requirements

- Python 3.8 or higher
- FFmpeg (for video encoding)
  - **Mac**: `brew install ffmpeg`
  - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
  - **Windows**: Download from https://ffmpeg.org/download.html

## 💡 Tips & Best Practices

### For Better Scripts
- Select 3-5 articles for a 5-minute video
- Mix different types of news (research, products, policy)
- Edit the script to match your personal style
- Add your own commentary or insights

### For Better Videos
- Use a professional tone for technical audiences
- Keep captions enabled for accessibility
- Choose background colors with good contrast
- Test with short videos first (2-3 minutes)

### TTS Recommendations
- **gTTS**: Best for testing, free, no setup required
- **OpenAI TTS**: Good quality, moderate cost, natural voices
- **ElevenLabs**: Highest quality, more expensive, very natural

## 🎨 Customization

### Modifying Video Style

Edit `video_generator.py` to customize:
- Video resolution (default: 1920x1080)
- Frame rate (default: 24 fps)
- Text positioning and animation
- Transition effects

### Adding Custom Visuals

You can extend the video generator to include:
- Article thumbnails
- Logo overlays
- Custom intro/outro sequences
- Animated graphics

## 🐛 Troubleshooting

### Common Issues

**"ANTHROPIC_API_KEY not found"**
- Make sure you've created a `.env` file with your API key
- Check that the key is valid and has sufficient credits

**"FFmpeg not found"**
- Install FFmpeg using your system's package manager
- Make sure it's in your system PATH

**"gTTS not installed"**
- Run `pip install gtts`
- For other TTS providers, install `openai` or `elevenlabs`

**Video generation is slow**
- This is normal - video processing takes time
- Shorter videos process faster
- Consider using a more powerful machine for production

**MoviePy errors**
- Make sure FFmpeg is properly installed
- Check that you have write permissions in the output directory
- Try reducing video duration or resolution

## 🚀 Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)

### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/aiml-video-generator.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
- Go to https://share.streamlit.io
- Click "New app"
- Select your GitHub repository
- Set main file: `app.py`
- Click "Deploy"

3. **Configure Secrets**
- In Streamlit Cloud, go to app settings
- Add your API keys in the "Secrets" section:
```toml
ANTHROPIC_API_KEY = "your_key_here"
OPENAI_API_KEY = "your_key_here"  # optional
ELEVENLABS_API_KEY = "your_key_here"  # optional
```

4. **Note on Video Generation**
- Streamlit Cloud has limited resources
- For production video generation, consider:
  - Running locally
  - Using a cloud VM (AWS, GCP, Azure)
  - Deploying on a more powerful server

## 📝 Example Workflow

Here's a typical workflow for creating a weekly AI news video:

1. **Monday**: Run the app, fetch 8-10 recent articles
2. **Tuesday**: Review articles, select 5 best ones
3. **Wednesday**: Generate script, edit and refine
4. **Thursday**: Generate video with your preferred settings
5. **Friday**: Review video, upload to YouTube

## 🛠️ Development

### Running Tests

```bash
# Test news fetching
python news_fetcher.py

# Test script generation
python script_generator.py

# Test video generation
python video_generator.py
```

### Adding Features

The modular design makes it easy to add features:
- New TTS providers → Edit `video_generator.py`
- Different video styles → Extend `create_video_with_visuals()`
- Additional news sources → Modify `news_fetcher.py`
- Custom templates → Add to `script_generator.py`

## 📄 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Feel free to fork, modify, and adapt this code for your needs!

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test individual modules separately
4. Consult the documentation for dependencies

## 🎯 Future Enhancements

Potential features to add:
- [ ] YouTube API integration for direct upload
- [ ] Thumbnail generation
- [ ] Multiple video templates
- [ ] Background music support
- [ ] Advanced editing features
- [ ] Batch video generation
- [ ] Analytics integration
- [ ] Multi-language support

---

**Happy video creating! 🎬✨**
