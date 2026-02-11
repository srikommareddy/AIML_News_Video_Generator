"""
Video Generator Module
Creates videos from scripts using text-to-speech and MoviePy
"""

import os
from pathlib import Path
from datetime import datetime
import re

# Will be imported when needed
# from moviepy.editor import *
# from gtts import gTTS

def create_video(script, articles, config):
    """
    Create a video from a script
    
    Args:
        script: Video script text
        articles: List of news articles (for visuals)
        config: Dictionary with video configuration:
            - voice_provider: TTS provider to use
            - voice_option: Voice selection
            - background_color: Background color hex
            - text_color: Text color hex
            - font_size: Font size for text
            - show_captions: Whether to show captions
    
    Returns:
        Path to generated video file
    """
    
    try:
        # Create output directory
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"aiml_news_{timestamp}.mp4"
        
        # Generate audio from script
        audio_path = generate_audio(
            script, 
            config['voice_provider'],
            config['voice_option']
        )
        
        # Create video with visuals
        video_path = create_video_with_visuals(
            audio_path,
            script,
            articles,
            config,
            output_path
        )
        
        return str(video_path)
    
    except Exception as e:
        print(f"Error creating video: {e}")
        raise


def generate_audio(script, provider="gTTS (Free)", voice_option="en-US"):
    """
    Generate audio from script using specified TTS provider
    
    Args:
        script: Script text
        provider: TTS provider
        voice_option: Voice selection
    
    Returns:
        Path to generated audio file
    """
    
    output_dir = Path("./output/audio")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_path = output_dir / f"narration_{timestamp}.mp3"
    
    # Clean script - remove section markers and timing
    clean_script = clean_script_for_tts(script)
    
    if provider == "gTTS (Free)":
        return generate_audio_gtts(clean_script, voice_option, audio_path)
    elif provider == "OpenAI TTS":
        return generate_audio_openai(clean_script, voice_option, audio_path)
    elif provider == "ElevenLabs":
        return generate_audio_elevenlabs(clean_script, voice_option, audio_path)
    else:
        raise ValueError(f"Unknown TTS provider: {provider}")


def clean_script_for_tts(script):
    """
    Clean script for TTS by removing section markers and timing
    
    Args:
        script: Raw script with markers
    
    Returns:
        Cleaned script text
    """
    # Remove section markers like [INTRO], [STORY 1], etc.
    script = re.sub(r'\[([^\]]+)\]', '', script)
    
    # Remove extra whitespace
    script = re.sub(r'\n\s*\n\s*\n', '\n\n', script)
    
    return script.strip()


def generate_audio_gtts(text, language, output_path):
    """Generate audio using Google Text-to-Speech (free)"""
    try:
        from gtts import gTTS
        
        # Map language codes
        lang_map = {
            "en-US": "en",
            "en-UK": "en",
            "en-AU": "en"
        }
        
        lang = lang_map.get(language, "en")
        
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(str(output_path))
        
        return str(output_path)
    
    except ImportError:
        raise ImportError("gTTS not installed. Install with: pip install gtts")
    except Exception as e:
        raise Exception(f"Error generating audio with gTTS: {e}")


def generate_audio_openai(text, voice, output_path):
    """Generate audio using OpenAI TTS API"""
    try:
        import openai
        
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        client = openai.OpenAI(api_key=api_key)
        
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,  # alloy, echo, fable, onyx, nova, shimmer
            input=text
        )
        
        response.stream_to_file(str(output_path))
        
        return str(output_path)
    
    except ImportError:
        raise ImportError("openai not installed. Install with: pip install openai")
    except Exception as e:
        raise Exception(f"Error generating audio with OpenAI: {e}")


def generate_audio_elevenlabs(text, voice_id, output_path):
    """Generate audio using ElevenLabs API"""
    try:
        from elevenlabs import generate, save
        
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment")
        
        audio = generate(
            text=text,
            voice=voice_id,
            api_key=api_key
        )
        
        save(audio, str(output_path))
        
        return str(output_path)
    
    except ImportError:
        raise ImportError("elevenlabs not installed. Install with: pip install elevenlabs")
    except Exception as e:
        raise Exception(f"Error generating audio with ElevenLabs: {e}")


def create_video_with_visuals(audio_path, script, articles, config, output_path):
    """
    Create video with visuals synchronized to audio
    
    Args:
        audio_path: Path to audio file
        script: Original script with timing
        articles: List of articles
        config: Video configuration
        output_path: Output video path
    
    Returns:
        Path to generated video
    """
    try:
        from moviepy.editor import (
            AudioFileClip, TextClip, CompositeVideoClip, 
            ColorClip, concatenate_videoclips
        )
        
        # Load audio
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration
        
        # Create background
        background = ColorClip(
            size=(1920, 1080),
            color=hex_to_rgb(config['background_color']),
            duration=duration
        )
        
        # Parse script into sections with timing
        sections = parse_script_sections(script)
        
        # Create text clips for each section
        clips = [background]
        
        for section in sections:
            text_clip = create_text_clip(
                text=section['text'],
                start_time=section['start'],
                duration=section['duration'],
                config=config
            )
            if text_clip:
                clips.append(text_clip)
        
        # Composite all clips
        video = CompositeVideoClip(clips)
        video = video.set_audio(audio)
        
        # Write video file
        video.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        return output_path
    
    except ImportError:
        raise ImportError(
            "MoviePy not installed. Install with: pip install moviepy\n"
            "You may also need to install ffmpeg"
        )
    except Exception as e:
        raise Exception(f"Error creating video: {e}")


def parse_script_sections(script):
    """
    Parse script into sections with timing information
    
    Args:
        script: Script with timing markers
    
    Returns:
        List of sections with start time, duration, and text
    """
    sections = []
    
    # Find all sections with timing like [INTRO] [0:00-0:30]
    pattern = r'\[([^\]]+)\]\s*\[([0-9:.]+)-([0-9:.]+)\](.*?)(?=\[|$)'
    matches = re.finditer(pattern, script, re.DOTALL)
    
    for match in matches:
        section_name = match.group(1)
        start_time = parse_time(match.group(2))
        end_time = parse_time(match.group(3))
        text = match.group(4).strip()
        
        sections.append({
            'name': section_name,
            'start': start_time,
            'duration': end_time - start_time,
            'text': text
        })
    
    return sections


def parse_time(time_str):
    """
    Parse time string to seconds
    
    Args:
        time_str: Time string like "1:30" or "0:45"
    
    Returns:
        Time in seconds
    """
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    return float(parts[0])


def create_text_clip(text, start_time, duration, config):
    """
    Create a text clip for the video
    
    Args:
        text: Text to display
        start_time: When to start displaying (seconds)
        duration: How long to display (seconds)
        config: Video configuration
    
    Returns:
        TextClip object
    """
    try:
        from moviepy.editor import TextClip
        
        if not config.get('show_captions', True):
            return None
        
        # Truncate long text
        if len(text) > 200:
            text = text[:200] + "..."
        
        txt_clip = TextClip(
            text,
            fontsize=config.get('font_size', 48),
            color=config.get('text_color', 'white'),
            font='Arial',
            size=(1600, None),  # Width constraint
            method='caption',
            align='center'
        )
        
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_start(start_time).set_duration(duration)
        
        return txt_clip
    
    except Exception as e:
        print(f"Warning: Could not create text clip: {e}")
        return None


def hex_to_rgb(hex_color):
    """
    Convert hex color to RGB tuple
    
    Args:
        hex_color: Hex color string like "#1a1a2e"
    
    Returns:
        RGB tuple like (26, 26, 46)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    # Test video generation
    print("Testing video generation...")
    
    test_script = """[INTRO] [0:00-0:30]
Welcome to AI Insights! Today we're covering the latest in artificial intelligence.

[STORY 1] [0:30-1:00]
OpenAI has released GPT-5 with incredible new capabilities.

[OUTRO] [1:00-1:15]
Thanks for watching! Don't forget to subscribe!
"""
    
    test_config = {
        'voice_provider': 'gTTS (Free)',
        'voice_option': 'en-US',
        'background_color': '#1a1a2e',
        'text_color': '#ffffff',
        'font_size': 48,
        'show_captions': True
    }
    
    try:
        video_path = create_video(test_script, [], test_config)
        print(f"✅ Test video created: {video_path}")
    except Exception as e:
        print(f"❌ Test failed: {e}")
