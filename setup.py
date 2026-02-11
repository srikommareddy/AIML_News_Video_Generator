#!/usr/bin/env python3
"""
Setup script for AI/ML Video Generator
Helps users verify their environment and configure the application
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Python version: {version_str}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Python 3.8 or higher is required")
        return False
    else:
        print_success("Python version is compatible")
        return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print_header("Checking FFmpeg")
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success("FFmpeg is installed")
            return True
    except FileNotFoundError:
        pass
    
    print_error("FFmpeg is not installed")
    print_info("FFmpeg is required for video generation")
    print_info("Install instructions:")
    print("  - Mac: brew install ffmpeg")
    print("  - Ubuntu/Debian: sudo apt-get install ffmpeg")
    print("  - Windows: Download from https://ffmpeg.org/download.html")
    return False

def check_packages():
    """Check if required packages are installed"""
    print_header("Checking Python Packages")
    
    required_packages = {
        'streamlit': 'streamlit',
        'anthropic': 'anthropic',
        'gtts': 'gtts',
        'moviepy': 'moviepy',
        'PIL': 'pillow'
    }
    
    missing_packages = []
    
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print_success(f"{package_name} is installed")
        except ImportError:
            print_error(f"{package_name} is NOT installed")
            missing_packages.append(package_name)
    
    if missing_packages:
        print_warning("Some packages are missing")
        print_info("Install them with: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists"""
    print_header("Checking Environment Configuration")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        print_warning(".env file not found")
        
        if env_example.exists():
            print_info("Creating .env from .env.example...")
            env_example.read_text()
            with open('.env', 'w') as f:
                f.write(env_example.read_text())
            print_success(".env file created")
            print_warning("Please edit .env and add your API keys")
        else:
            print_error(".env.example not found")
            return False
    else:
        print_success(".env file exists")
    
    # Check if API keys are configured
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
            print_success("ANTHROPIC_API_KEY is configured")
        else:
            print_warning("ANTHROPIC_API_KEY needs to be set in .env")
            print_info("Get your key from: https://console.anthropic.com")
    except ImportError:
        print_warning("python-dotenv not installed (optional)")
    
    return True

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = ['output', 'output/audio', 'output/videos']
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print_success(f"Created {directory}/")
        else:
            print_info(f"{directory}/ already exists")
    
    return True

def test_imports():
    """Test if all modules can be imported"""
    print_header("Testing Module Imports")
    
    modules = [
        ('news_fetcher', 'News Fetcher'),
        ('script_generator', 'Script Generator'),
        ('video_generator', 'Video Generator')
    ]
    
    all_success = True
    
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print_success(f"{display_name} module OK")
        except Exception as e:
            print_error(f"{display_name} module error: {e}")
            all_success = False
    
    return all_success

def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")
    
    print("🎉 Your environment is ready!\n")
    print("Next steps:")
    print("1. Edit .env and add your Anthropic API key")
    print("2. Run the application: streamlit run app.py")
    print("3. Open your browser to http://localhost:8501")
    print("\nFor detailed instructions, see README.md")

def main():
    """Main setup function"""
    print_header("AI/ML Video Generator - Setup")
    
    checks = [
        ("Python Version", check_python_version()),
        ("FFmpeg", check_ffmpeg()),
        ("Python Packages", check_packages()),
        ("Environment File", check_env_file()),
        ("Directories", create_directories()),
        ("Module Imports", test_imports())
    ]
    
    print_header("Setup Summary")
    
    all_passed = True
    for check_name, result in checks:
        if result:
            print_success(f"{check_name}: PASSED")
        else:
            print_error(f"{check_name}: FAILED")
            all_passed = False
    
    print()
    
    if all_passed:
        print_next_steps()
    else:
        print_error("Some checks failed. Please fix the issues above before running the application.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
