import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import html
import re

def fetch_google_news(topic: str, max_results: int = 5) -> list[dict]:
    """
    Fetches news headlines, publication dates, and original source URLs from Google News.
    """
    encoded_topic = urllib.parse.quote(topic)
    rss_url = f"https://news.google.com/rss/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"

    req = urllib.request.Request(
        rss_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        items = []
        
        for item in root.findall("./channel/item")[:max_results]:
            title = item.findtext("title", default="No Title")
            link = item.findtext("link", default="#")
            pub_date = item.findtext("pubDate", default="")
            description = item.findtext("description", default="")

            # Clean HTML tags from description
            clean_desc = re.sub(r'<[^>]+>', '', html.unescape(description)).strip()

            # Separate source publisher from title if present (e.g. "Headline - Publisher")
            source = "Google News"
            source_elem = item.find("source")
            if source_elem is not None and source_elem.text:
                source = source_elem.text

            items.append({
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "source": source,
                "snippet": clean_desc
            })

        return items
    except Exception as e:
        print(f"[!] Error fetching Google News for '{topic}': {e}")
        return []

if __name__ == "__main__":
    articles = fetch_google_news("Artificial Intelligence", max_results=3)
    for i, a in enumerate(articles, 1):
        print(f"{i}. {a['title']}\n   Source: {a['source']}\n   Link: {a['link']}\n")
