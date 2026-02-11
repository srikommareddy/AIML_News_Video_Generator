"""
Script Generator Module
Generates video scripts using Claude API based on selected news articles
"""

import anthropic
import os
from datetime import datetime

def generate_script(articles, duration_minutes=5, tone="Professional", channel_name="AI Insights"):
    """
    Generate a video script from selected news articles
    
    Args:
        articles: List of article dictionaries
        duration_minutes: Target duration for the video
        tone: Tone of the script (Professional, Casual, Enthusiastic, Educational)
        channel_name: Name of the YouTube channel
    
    Returns:
        Generated script as a string
    """
    
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return generate_mock_script(articles, duration_minutes, tone, channel_name)
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Prepare articles summary for the prompt
        articles_text = "\n\n".join([
            f"Article {i+1}:\n"
            f"Title: {article['title']}\n"
            f"Source: {article.get('source', 'Unknown')}\n"
            f"Date: {article.get('date', 'N/A')}\n"
            f"Summary: {article.get('snippet', 'No summary')}\n"
            for i, article in enumerate(articles)
        ])
        
        # Calculate target word count (assuming 150 words per minute)
        target_words = duration_minutes * 150
        
        prompt = f"""You are a professional YouTube script writer for the channel "{channel_name}". 
Create an engaging {duration_minutes}-minute video script for an AI/ML news roundup.

TONE: {tone}
TARGET LENGTH: Approximately {target_words} words ({duration_minutes} minutes at 150 words/minute)

NEWS ARTICLES TO COVER:
{articles_text}

SCRIPT REQUIREMENTS:
1. Start with an engaging hook and channel intro
2. Cover each news story in a clear, concise way
3. Include smooth transitions between stories
4. Add relevant context or implications for each story
5. Use the {tone.lower()} tone throughout
6. End with a compelling outro and call-to-action (like, subscribe, comment)
7. Format with clear sections: [INTRO], [STORY 1], [STORY 2], etc., [OUTRO]
8. Include timing estimates for each section in brackets like [0:00-0:30]
9. Write in a conversational style suitable for video narration
10. Make it engaging and informative

IMPORTANT: The script should be natural and easy to read aloud. Avoid overly complex sentences.

Generate the complete video script now:"""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract script from response
        script = ""
        for block in response.content:
            if block.type == "text":
                script += block.text
        
        return script.strip()
    
    except Exception as e:
        print(f"Error generating script: {e}")
        return generate_mock_script(articles, duration_minutes, tone, channel_name)


def generate_mock_script(articles, duration_minutes=5, tone="Professional", channel_name="AI Insights"):
    """Generate a mock script for testing without API"""
    
    intro = f"""[INTRO] [0:00-0:30]

Hey everyone, welcome back to {channel_name}! I'm excited to bring you the latest developments in artificial intelligence and machine learning. We've got some incredible stories to cover today, from groundbreaking research to major industry announcements. Let's dive right in!

"""
    
    stories = ""
    for i, article in enumerate(articles, 1):
        time_start = 0.5 + (i-1) * 0.7
        time_end = time_start + 0.7
        
        stories += f"""[STORY {i}] [{time_start:.1f}:00-{time_end:.1f}:00]

{article['title']}

{article.get('snippet', 'This is an important development in the AI space.')} 

According to {article.get('source', 'reports')}, this development could have significant implications for the future of AI technology. {get_context_sentence(tone)}

"""
    
    outro = f"""[OUTRO] [{duration_minutes-0.5:.1f}:00-{duration_minutes:.1f}:00]

And that wraps up today's AI news roundup! The pace of innovation in this field continues to accelerate, and it's an exciting time to be following these developments.

If you found this video helpful, please give it a thumbs up and subscribe to {channel_name} for more AI and machine learning content. Drop a comment below and let me know which story you found most interesting!

Thanks for watching, and I'll see you in the next video!
"""
    
    return intro + stories + outro


def get_context_sentence(tone):
    """Return a contextual sentence based on tone"""
    contexts = {
        "Professional": "Industry experts are closely monitoring this development.",
        "Casual": "Pretty cool stuff, right?",
        "Enthusiastic": "This is absolutely incredible and game-changing!",
        "Educational": "Let's break down what this means for the field."
    }
    return contexts.get(tone, "This is an interesting development.")


def estimate_reading_time(script):
    """
    Estimate reading time for a script
    
    Args:
        script: The script text
    
    Returns:
        Estimated duration in minutes
    """
    words = len(script.split())
    minutes = words / 150  # Average speaking rate
    return round(minutes, 1)


def format_script_for_display(script):
    """
    Format script with better readability for display
    
    Args:
        script: Raw script text
    
    Returns:
        Formatted script
    """
    # Add extra spacing around section markers
    import re
    script = re.sub(r'\[([^\]]+)\]', r'\n[\1]\n', script)
    return script.strip()


if __name__ == "__main__":
    # Test script generation
    from news_fetcher import get_mock_news_data
    
    print("Generating test script...")
    articles = get_mock_news_data(5)
    
    script = generate_script(
        articles,
        duration_minutes=5,
        tone="Professional",
        channel_name="AI Weekly"
    )
    
    print("\n" + "="*60)
    print("GENERATED SCRIPT")
    print("="*60)
    print(script)
    print("\n" + "="*60)
    print(f"Estimated duration: {estimate_reading_time(script)} minutes")
    print(f"Word count: {len(script.split())} words")
