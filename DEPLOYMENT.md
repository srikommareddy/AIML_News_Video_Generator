# Deployment Guide - Streamlit Cloud

This guide will help you deploy the AI/ML Video Generator to Streamlit Cloud.

## 📋 Prerequisites

1. **GitHub Account**: You need a GitHub account to host your code
2. **Streamlit Cloud Account**: Sign up for free at https://streamlit.io/cloud
3. **Anthropic API Key**: Get from https://console.anthropic.com

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

1. **Create a new GitHub repository**:
   ```bash
   # Initialize git in your project directory
   cd aiml_video_agent
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit: AI/ML Video Generator"
   ```

2. **Push to GitHub**:
   ```bash
   # Create a new repository on GitHub, then:
   git remote add origin https://github.com/YOUR_USERNAME/aiml-video-generator.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Configure Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit https://share.streamlit.io
   - Sign in with your GitHub account

2. **Create New App**:
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/aiml-video-generator`
   - Set branch: `main`
   - Set main file path: `app.py`
   - Click "Deploy"

### Step 3: Configure Secrets

Streamlit Cloud needs your API keys to be configured as secrets.

1. **Navigate to App Settings**:
   - Go to your deployed app
   - Click the hamburger menu (☰)
   - Select "Settings"

2. **Add Secrets**:
   - Click "Secrets" in the left sidebar
   - Add your secrets in TOML format:

   ```toml
   # Required
   ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
   
   # Optional: Only if using these TTS providers
   OPENAI_API_KEY = "sk-your-openai-key"
   ELEVENLABS_API_KEY = "your-elevenlabs-key"
   ```

3. **Save**:
   - Click "Save"
   - The app will automatically restart with the new secrets

### Step 4: Access Environment Variables in Code

The secrets are automatically available as environment variables. Your code already handles this:

```python
import os

# This works automatically in Streamlit Cloud
api_key = os.environ.get("ANTHROPIC_API_KEY")
```

## ⚙️ Configuration for Streamlit Cloud

### packages.txt (System Dependencies)

If you need FFmpeg for video generation, create a `packages.txt` file:

```bash
ffmpeg
```

However, note that video generation on Streamlit Cloud has limitations (see below).

### config.toml (Optional Streamlit Configuration)

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[server]
maxUploadSize = 200
```

## ⚠️ Important Limitations

### Streamlit Cloud Resource Constraints

1. **CPU/Memory Limits**:
   - Free tier has limited resources
   - Video generation is CPU-intensive
   - May timeout for long videos

2. **Storage Limits**:
   - Temporary file storage only
   - Generated videos are not permanently stored
   - Use download buttons to save locally

3. **Execution Time**:
   - Maximum execution time limits
   - Long video generation may fail
   - Recommended: Generate videos locally, use cloud for script generation

### Recommended Cloud Deployment Strategy

**Option A: Hybrid Approach (Recommended)**
- Deploy to Streamlit Cloud for news fetching and script generation
- Generate videos locally on your machine
- Best balance of convenience and capability

**Option B: Full Local Development**
- Run entire application locally
- Full control over resources
- Best for production video generation

**Option C: Cloud VM Deployment**
- Deploy on AWS EC2, Google Cloud, or Azure
- Full control and better resources
- More expensive but more reliable

## 🔄 Updating Your Deployment

### Deploy Updates

```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push

# Streamlit Cloud automatically redeploys
```

### Force Restart

If your app needs a restart:
1. Go to app settings
2. Click "Reboot app"

## 🐛 Troubleshooting

### App Won't Deploy

**Check logs**:
- Click "Manage app" → "Logs"
- Look for error messages

**Common issues**:
- Missing dependencies in `requirements.txt`
- Incorrect file paths
- Missing secrets/API keys

### Secrets Not Working

**Verify format**:
- Must be valid TOML
- Use quotes for string values
- No extra spaces or characters

**Test locally**:
```python
import streamlit as st

# Access secrets
api_key = st.secrets.get("ANTHROPIC_API_KEY")
print(f"API Key present: {api_key is not None}")
```

### Video Generation Fails

**This is expected on Streamlit Cloud**:
- Video generation is resource-intensive
- Use local generation instead
- Or deploy to a more powerful cloud instance

**Alternatives**:
1. Generate videos locally
2. Use the cloud app only for news/scripts
3. Deploy to a cloud VM with more resources

## 📊 Monitoring Your App

### View Analytics
- App settings → "Analytics"
- See usage statistics
- Monitor errors

### Resource Usage
- Check CPU and memory usage
- Identify performance bottlenecks
- Optimize if needed

## 💰 Cost Considerations

### Streamlit Cloud (Free Tier)
- **Cost**: Free
- **Limits**: 
  - 1 private app or unlimited public apps
  - Community support only
  - Limited resources

### Streamlit Cloud (Paid Tiers)
- **Teams**: $20/month
  - Private apps
  - More resources
  - Better support

### API Costs
- **Anthropic API**: Pay per token
  - Script generation: ~$0.01-0.05 per video
  - News fetching: ~$0.01-0.02 per session
- **OpenAI TTS**: ~$0.015 per 1000 characters
- **ElevenLabs**: Varies by plan

### Estimated Monthly Costs
For 4 videos per week:
- Anthropic API: ~$5-10/month
- OpenAI TTS (optional): ~$5/month
- ElevenLabs (optional): ~$15+/month
- **Total**: $5-30/month depending on choices

## 🎯 Best Practices

1. **Start Simple**:
   - Deploy with basic features first
   - Test thoroughly before adding complexity

2. **Use Secrets**:
   - Never commit API keys to Git
   - Always use Streamlit secrets

3. **Monitor Usage**:
   - Check API usage regularly
   - Set up billing alerts
   - Optimize prompts to reduce costs

4. **User Experience**:
   - Add loading indicators
   - Handle errors gracefully
   - Provide clear instructions

5. **Testing**:
   - Test locally first
   - Use mock data for development
   - Verify cloud deployment with small tests

## 🔗 Useful Links

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Anthropic API Docs](https://docs.anthropic.com)
- [GitHub Help](https://docs.github.com)

## 📧 Getting Help

**Streamlit Community**:
- Forum: https://discuss.streamlit.io
- Documentation: https://docs.streamlit.io

**Anthropic Support**:
- Support: https://support.anthropic.com
- Discord: https://discord.gg/anthropic

---

**Ready to deploy? Follow the steps above and your app will be live! 🚀**
