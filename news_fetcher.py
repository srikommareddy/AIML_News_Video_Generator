"""
News Fetcher Module
Fetches latest AI/ML news articles using web search
"""

import anthropic
import os
from datetime import datetime

def fetch_aiml_news(query="artificial intelligence machine learning", num_articles=10):
    """
    Fetch AI/ML news articles using Claude with web search
    
    Args:
        query: Search query string
        num_articles: Number of articles to fetch
    
    Returns:
        List of article dictionaries with title, source, date, snippet, url
    """
    
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # Return mock data if no API key
        return get_mock_news_data(num_articles)
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""Find the {num_articles} most recent and important news articles about {query}. 
        
Focus on:
- Recent developments (last 7 days preferred)
- Major AI/ML announcements
- Research breakthroughs
- Industry news
- Product launches

For each article, provide:
1. Title
2. Source/Publication
3. Date
4. Brief summary (2-3 sentences)
5. URL

Format your response as a JSON array of objects with keys: title, source, date, snippet, url"""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search"
            }],
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract articles from response
        articles = parse_claude_response(response)
        
        return articles[:num_articles]
    
    except Exception as e:
        print(f"Error fetching news: {e}")
        return get_mock_news_data(num_articles)


def parse_claude_response(response):
    """Parse Claude's response to extract article information"""
    import json
    import re
    
    articles = []
    
    # Get text content from response
    text_content = ""
    for block in response.content:
        if block.type == "text":
            text_content += block.text
    
    # Try to extract JSON
    try:
        # Look for JSON array in the response
        json_match = re.search(r'\[[\s\S]*\]', text_content)
        if json_match:
            articles_data = json.loads(json_match.group())
            return articles_data
    except:
        pass
    
    # If JSON parsing fails, try to parse structured text
    lines = text_content.split('\n')
    current_article = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_article:
                articles.append(current_article)
                current_article = {}
            continue
        
        if line.lower().startswith('title:'):
            current_article['title'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('source:'):
            current_article['source'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('date:'):
            current_article['date'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('summary:') or line.lower().startswith('snippet:'):
            current_article['snippet'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('url:'):
            current_article['url'] = line.split(':', 1)[1].strip()
    
    if current_article:
        articles.append(current_article)
    
    return articles


def get_mock_news_data(num_articles=10):
    """Return mock news data for testing without API"""
    
    mock_articles = [
        {
            "title": "OpenAI Releases GPT-5 with Multimodal Capabilities",
            "source": "TechCrunch",
            "date": "2026-02-01",
            "snippet": "OpenAI has unveiled GPT-5, featuring enhanced multimodal understanding and reasoning capabilities. The new model shows significant improvements in mathematical reasoning and code generation.",
            "url": "https://techcrunch.com/example1"
        },
        {
            "title": "Google DeepMind Achieves Breakthrough in Protein Folding",
            "source": "Nature",
            "date": "2026-01-30",
            "snippet": "Researchers at Google DeepMind have developed a new AI system that can predict protein structures with unprecedented accuracy, potentially accelerating drug discovery.",
            "url": "https://nature.com/example2"
        },
        {
            "title": "Meta Launches Open Source Large Language Model",
            "source": "The Verge",
            "date": "2026-01-28",
            "snippet": "Meta has released Llama 4, an open-source large language model that rivals proprietary alternatives in performance while being freely available for commercial use.",
            "url": "https://theverge.com/example3"
        },
        {
            "title": "AI Regulation Bill Passes Senate Committee",
            "source": "Reuters",
            "date": "2026-01-27",
            "snippet": "The Senate has advanced new AI safety legislation that would establish federal oversight for AI development and deployment, marking a significant step in AI governance.",
            "url": "https://reuters.com/example4"
        },
        {
            "title": "Anthropic Announces Constitutional AI Framework",
            "source": "Wired",
            "date": "2026-01-26",
            "snippet": "Anthropic has introduced a new framework for training AI systems with built-in ethical constraints, aiming to create more reliable and aligned AI assistants.",
            "url": "https://wired.com/example5"
        },
        {
            "title": "Tesla Deploys Humanoid Robots in Manufacturing",
            "source": "Bloomberg",
            "date": "2026-01-25",
            "snippet": "Tesla has begun using its Optimus humanoid robots in production facilities, marking a milestone in the integration of AI-powered robotics in manufacturing.",
            "url": "https://bloomberg.com/example6"
        },
        {
            "title": "AI Chip Startup Raises $500M Series C",
            "source": "VentureBeat",
            "date": "2026-01-24",
            "snippet": "A Silicon Valley startup developing specialized AI chips has secured $500 million in funding, led by major tech investors betting on next-generation hardware.",
            "url": "https://venturebeat.com/example7"
        },
        {
            "title": "Stanford Researchers Develop Explainable AI System",
            "source": "MIT Technology Review",
            "date": "2026-01-23",
            "snippet": "Stanford scientists have created an AI system that can explain its decision-making process in human-understandable terms, addressing the black box problem.",
            "url": "https://technologyreview.com/example8"
        },
        {
            "title": "Microsoft Integrates AI into Windows 12",
            "source": "ZDNet",
            "date": "2026-01-22",
            "snippet": "Microsoft has announced Windows 12 will feature deep AI integration, including an intelligent assistant that can help users with complex tasks across applications.",
            "url": "https://zdnet.com/example9"
        },
        {
            "title": "AI-Generated Art Wins Major Competition",
            "source": "The Guardian",
            "date": "2026-01-21",
            "snippet": "An AI-generated artwork has won first place in a prestigious international art competition, reigniting debates about creativity and machine learning.",
            "url": "https://theguardian.com/example10"
        }
    ]
    
    return mock_articles[:num_articles]


if __name__ == "__main__":
    # Test the news fetcher
    print("Fetching AI/ML news...")
    articles = fetch_aiml_news(num_articles=5)
    
    print(f"\nFound {len(articles)} articles:\n")
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']} | Date: {article['date']}")
        print(f"   {article['snippet'][:100]}...")
        print()
