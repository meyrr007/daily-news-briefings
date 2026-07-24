import os

def summarize_news(articles: list[dict]) -> list[dict]:
    """
    Generates structured bullet-point summaries for articles.
    """
    summarized = []
    for art in articles:
        title = art['title']
        snippet = art.get('snippet', '')
        source = art.get('source', 'News Source')
        
        # Simple extraction-based summary bullets
        bullets = []
        if snippet:
            # Clean snippet sentences
            sentences = [s.strip() for s in snippet.split('.') if len(s.strip()) > 10]
            bullets = sentences[:3]
        
        if not bullets:
            bullets = [f"Headline summary from {source}."]

        summarized.append({
            "title": title,
            "source": source,
            "link": art['link'],
            "pub_date": art.get('pub_date', ''),
            "bullets": bullets
        })

    return summarized

def summarize_youtube(videos: list[dict]) -> list[dict]:
    """
    Generates structured bullet-point summaries for YouTube videos.
    """
    summarized = []
    for vid in videos:
        title = vid['title']
        channel = vid.get('channel', 'YouTube Channel')
        snippet = vid.get('snippet', '')
        
        bullets = []
        if snippet:
            sentences = [s.strip() for s in snippet.split('.') if len(s.strip()) > 10]
            bullets = sentences[:3]
        
        if not bullets:
            bullets = [f"Video released by {channel}."]

        summarized.append({
            "title": title,
            "channel": channel,
            "link": vid['link'],
            "bullets": bullets
        })

    return summarized
