import streamlit as st
import json
from datetime import datetime
import os
from pathlib import Path

# Import custom modules
from news_fetcher import fetch_aiml_news
from script_generator import generate_script
from video_generator import create_video

# Page configuration
st.set_page_config(
    page_title="AI/ML Video Generator",
    page_icon="🎬",
    layout="wide"
)

# Initialize session state
if 'news_articles' not in st.session_state:
    st.session_state.news_articles = []
if 'selected_articles' not in st.session_state:
    st.session_state.selected_articles = []
if 'script' not in st.session_state:
    st.session_state.script = ""
if 'video_path' not in st.session_state:
    st.session_state.video_path = None

# Title and description
st.title("🎬 AI/ML News Video Generator")
st.markdown("""
Generate engaging AI/ML news roundup videos with full human-in-the-loop control.
Follow the workflow steps below to create your video.
""")

# Workflow tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Fetch News", 
    "2️⃣ Generate Script", 
    "3️⃣ Create Video",
    "4️⃣ Settings"
])

# ============================================================
# TAB 1: FETCH NEWS
# ============================================================
with tab1:
    st.header("Fetch Latest AI/ML News")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input(
            "Search Query",
            value="artificial intelligence machine learning",
            help="Customize the search query for news articles"
        )
    
    with col2:
        num_articles = st.number_input(
            "Number of Articles",
            min_value=3,
            max_value=20,
            value=10,
            help="How many articles to fetch"
        )
    
    if st.button("🔍 Fetch News Articles", type="primary"):
        with st.spinner("Fetching latest AI/ML news..."):
            try:
                articles = fetch_aiml_news(search_query, num_articles)
                st.session_state.news_articles = articles
                st.success(f"✅ Fetched {len(articles)} articles!")
            except Exception as e:
                st.error(f"❌ Error fetching news: {str(e)}")
    
    # Display fetched articles
    if st.session_state.news_articles:
        st.subheader("📰 Available Articles")
        st.markdown("Select the articles you want to include in your video:")
        
        selected_indices = []
        
        for idx, article in enumerate(st.session_state.news_articles):
            with st.expander(f"📄 {article['title']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Source:** {article.get('source', 'Unknown')}")
                    st.markdown(f"**Date:** {article.get('date', 'N/A')}")
                    st.markdown(f"**Summary:** {article.get('snippet', 'No summary available')}")
                    if article.get('url'):
                        st.markdown(f"[Read full article]({article['url']})")
                
                with col2:
                    if st.checkbox("Include", key=f"article_{idx}"):
                        selected_indices.append(idx)
        
        # Update selected articles
        st.session_state.selected_articles = [
            st.session_state.news_articles[i] for i in selected_indices
        ]
        
        if st.session_state.selected_articles:
            st.info(f"✓ {len(st.session_state.selected_articles)} article(s) selected")

# ============================================================
# TAB 2: GENERATE SCRIPT
# ============================================================
with tab2:
    st.header("Generate Video Script")
    
    if not st.session_state.selected_articles:
        st.warning("⚠️ Please select articles from the 'Fetch News' tab first.")
    else:
        st.success(f"✅ {len(st.session_state.selected_articles)} articles selected")
        
        # Script generation options
        col1, col2 = st.columns(2)
        
        with col1:
            video_duration = st.slider(
                "Target Video Duration (minutes)",
                min_value=2,
                max_value=15,
                value=5,
                help="Approximate duration for the final video"
            )
        
        with col2:
            tone = st.selectbox(
                "Video Tone",
                ["Professional", "Casual", "Enthusiastic", "Educational"],
                help="The tone and style of narration"
            )
        
        channel_name = st.text_input(
            "Channel Name/Intro",
            value="AI Insights",
            help="Your channel name for intro/outro"
        )
        
        if st.button("✍️ Generate Script", type="primary"):
            with st.spinner("Generating script with Claude..."):
                try:
                    script = generate_script(
                        st.session_state.selected_articles,
                        duration_minutes=video_duration,
                        tone=tone,
                        channel_name=channel_name
                    )
                    st.session_state.script = script
                    st.success("✅ Script generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error generating script: {str(e)}")
        
        # Display and edit script
        if st.session_state.script:
            st.subheader("📝 Video Script")
            st.markdown("Review and edit the script below:")
            
            edited_script = st.text_area(
                "Script Content",
                value=st.session_state.script,
                height=400,
                help="You can edit the script directly here"
            )
            
            # Update script if edited
            if edited_script != st.session_state.script:
                st.session_state.script = edited_script
                st.info("💡 Script updated!")
            
            # Word count
            word_count = len(st.session_state.script.split())
            estimated_duration = word_count / 150  # Assuming 150 words per minute
            st.metric("Estimated Duration", f"{estimated_duration:.1f} minutes")
            
            # Download script
            st.download_button(
                label="📥 Download Script",
                data=st.session_state.script,
                file_name=f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# ============================================================
# TAB 3: CREATE VIDEO
# ============================================================
with tab3:
    st.header("Create Video")
    
    if not st.session_state.script:
        st.warning("⚠️ Please generate a script in the 'Generate Script' tab first.")
    else:
        st.success("✅ Script ready for video generation")
        
        # Voice settings
        st.subheader("🎙️ Voice Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            voice_provider = st.selectbox(
                "Voice Provider",
                ["gTTS (Free)", "OpenAI TTS", "ElevenLabs"],
                help="Select text-to-speech provider"
            )
        
        with col2:
            if voice_provider == "gTTS (Free)":
                voice_option = st.selectbox("Voice", ["en-US", "en-UK", "en-AU"])
            else:
                voice_option = st.text_input("Voice ID/Name", value="alloy")
        
        # Visual settings
        st.subheader("🎨 Visual Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            background_color = st.color_picker("Background Color", "#1a1a2e")
            text_color = st.color_picker("Text Color", "#ffffff")
        
        with col2:
            font_size = st.slider("Font Size", 24, 72, 48)
            show_captions = st.checkbox("Show Captions", value=True)
        
        # API keys (if needed)
        with st.expander("🔑 API Keys (if required)"):
            anthropic_api_key = st.text_input(
                "Anthropic API Key",
                type="password",
                help="Required for script generation with Claude API"
            )
            if voice_provider == "OpenAI TTS":
                openai_api_key = st.text_input(
                    "OpenAI API Key",
                    type="password"
                )
            elif voice_provider == "ElevenLabs":
                elevenlabs_api_key = st.text_input(
                    "ElevenLabs API Key",
                    type="password"
                )
        
        # Generate video button
        if st.button("🎬 Generate Video", type="primary"):
            with st.spinner("Creating video... This may take a few minutes."):
                try:
                    video_config = {
                        'voice_provider': voice_provider,
                        'voice_option': voice_option,
                        'background_color': background_color,
                        'text_color': text_color,
                        'font_size': font_size,
                        'show_captions': show_captions
                    }
                    
                    video_path = create_video(
                        st.session_state.script,
                        st.session_state.selected_articles,
                        video_config
                    )
                    
                    st.session_state.video_path = video_path
                    st.success("✅ Video created successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error creating video: {str(e)}")
        
        # Display video if created
        if st.session_state.video_path and os.path.exists(st.session_state.video_path):
            st.subheader("🎥 Generated Video")
            st.video(st.session_state.video_path)
            
            # Download video
            with open(st.session_state.video_path, 'rb') as video_file:
                st.download_button(
                    label="📥 Download Video",
                    data=video_file,
                    file_name=f"aiml_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                    mime="video/mp4"
                )

# ============================================================
# TAB 4: SETTINGS
# ============================================================
with tab4:
    st.header("⚙️ Settings & Configuration")
    
    st.subheader("📁 Output Directories")
    
    output_dir = st.text_input(
        "Output Directory",
        value="./output",
        help="Where generated videos will be saved"
    )
    
    if st.button("Create Directory"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        st.success(f"✅ Directory created: {output_dir}")
    
    st.subheader("💾 Save/Load Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Current State"):
            state_data = {
                'selected_articles': st.session_state.selected_articles,
                'script': st.session_state.script,
                'timestamp': datetime.now().isoformat()
            }
            
            filename = f"state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(state_data, f, indent=2)
            
            st.success(f"✅ State saved to {filename}")
    
    with col2:
        uploaded_file = st.file_uploader("📂 Load Previous State", type=['json'])
        if uploaded_file:
            state_data = json.load(uploaded_file)
            st.session_state.selected_articles = state_data.get('selected_articles', [])
            st.session_state.script = state_data.get('script', '')
            st.success("✅ State loaded successfully!")
    
    st.subheader("🔄 Reset")
    if st.button("🗑️ Clear All Data", type="secondary"):
        st.session_state.news_articles = []
        st.session_state.selected_articles = []
        st.session_state.script = ""
        st.session_state.video_path = None
        st.success("✅ All data cleared!")
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>AI/ML Video Generator | Built with Streamlit & Claude</small>
</div>
""", unsafe_allow_html=True)
