#!/usr/bin/env python3
"""
Demo script for AI/ML Video Generator
Demonstrates the workflow without requiring a full Streamlit setup
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from news_fetcher import fetch_aiml_news, get_mock_news_data
from script_generator import generate_script, estimate_reading_time
from video_generator import create_video

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def demo_news_fetching():
    """Demonstrate news fetching"""
    print_section("STEP 1: Fetching AI/ML News")
    
    print("Fetching latest AI/ML news articles...")
    articles = fetch_aiml_news("artificial intelligence machine learning", num_articles=5)
    
    print(f"✅ Found {len(articles)} articles:\n")
    
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   📰 {article['source']} | 📅 {article['date']}")
        print(f"   📝 {article['snippet'][:100]}...")
        print()
    
    return articles

def demo_script_generation(articles):
    """Demonstrate script generation"""
    print_section("STEP 2: Generating Video Script")
    
    print("Generating script for a 5-minute video...")
    print("Configuration:")
    print("  - Duration: 5 minutes")
    print("  - Tone: Professional")
    print("  - Channel: AI Weekly\n")
    
    script = generate_script(
        articles[:5],  # Use first 5 articles
        duration_minutes=5,
        tone="Professional",
        channel_name="AI Weekly"
    )
    
    word_count = len(script.split())
    duration = estimate_reading_time(script)
    
    print(f"✅ Script generated!")
    print(f"   📊 Word count: {word_count}")
    print(f"   ⏱️  Estimated duration: {duration} minutes\n")
    
    print("Script preview (first 500 characters):")
    print("-" * 70)
    print(script[:500] + "...\n")
    
    # Save script to file
    script_path = Path("output/demo_script.txt")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(script)
    print(f"💾 Full script saved to: {script_path}\n")
    
    return script

def demo_video_creation(script, articles):
    """Demonstrate video creation"""
    print_section("STEP 3: Creating Video")
    
    print("⚠️  Video generation requires:")
    print("  - FFmpeg installed")
    print("  - Several minutes to process")
    print("  - Sufficient disk space\n")
    
    response = input("Do you want to generate the video? (y/n): ").strip().lower()
    
    if response != 'y':
        print("\n⏭️  Skipping video generation.")
        print("To generate videos, run the full Streamlit app: streamlit run app.py")
        return None
    
    print("\n🎬 Generating video...")
    print("This may take several minutes...\n")
    
    try:
        config = {
            'voice_provider': 'gTTS (Free)',
            'voice_option': 'en-US',
            'background_color': '#1a1a2e',
            'text_color': '#ffffff',
            'font_size': 48,
            'show_captions': True
        }
        
        video_path = create_video(script, articles, config)
        
        print(f"\n✅ Video created successfully!")
        print(f"   📹 Video saved to: {video_path}")
        print(f"   🎥 You can now upload this to YouTube!\n")
        
        return video_path
        
    except Exception as e:
        print(f"\n❌ Error creating video: {e}")
        print("Make sure FFmpeg is installed and requirements are met.")
        return None

def main():
    """Run the demo"""
    print_section("AI/ML Video Generator - Demo")
    
    print("This demo will walk you through the video generation process.")
    print("It will:")
    print("  1. Fetch AI/ML news articles")
    print("  2. Generate a video script")
    print("  3. (Optional) Create a video\n")
    
    input("Press Enter to continue...")
    
    # Step 1: Fetch news
    articles = demo_news_fetching()
    input("\nPress Enter to continue to script generation...")
    
    # Step 2: Generate script
    script = demo_script_generation(articles)
    input("\nPress Enter to continue to video creation...")
    
    # Step 3: Create video (optional)
    video_path = demo_video_creation(script, articles)
    
    # Final summary
    print_section("Demo Complete!")
    
    print("📁 Generated files:")
    print("  - Script: output/demo_script.txt")
    if video_path:
        print(f"  - Video: {video_path}")
    
    print("\n🚀 Next steps:")
    print("  1. Run the full app: streamlit run app.py")
    print("  2. Customize scripts and settings")
    print("  3. Create videos for your YouTube channel!")
    
    print("\n📚 For more information, see README.md")
    print("❓ Questions? Check QUICKSTART.md for common issues\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Demo error: {e}")
        print("Please check that all dependencies are installed.")
        sys.exit(1)
