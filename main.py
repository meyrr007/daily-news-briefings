import argparse
import os
import sys

from config import DEFAULT_TOPICS, MAX_NEWS_ITEMS, MAX_YOUTUBE_ITEMS, YOUTUBE_CHANNELS, YOUTUBE_MAX_AGE_DAYS, OUTPUT_DIR
from news_fetcher import fetch_google_news
from youtube_fetcher import search_youtube_videos, fetch_channel_recent_videos
from summarizer import summarize_news, summarize_youtube
from onenote_exporter import generate_onenote_html, export_to_file, publish_to_onenote_com
from index_generator import update_index_dashboard
from git_publisher import publish_to_github

def run_briefing(topic: str):
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print(f"\n==================================================")
    print(f" [!] Running Briefing Generator for: '{topic}'")
    print(f"==================================================")

    # 1. Fetch Google News
    print(f"[1/4] Fetching news from Google News...")
    raw_news = fetch_google_news(topic, max_results=MAX_NEWS_ITEMS)
    print(f"      Found {len(raw_news)} articles.")

    # 2. Fetch YouTube Videos (Search & Channels)
    print(f"[2/4] Searching YouTube & monitoring specific channels (last {YOUTUBE_MAX_AGE_DAYS} days)...")
    raw_videos = []
    
    if YOUTUBE_CHANNELS:
        for ch in YOUTUBE_CHANNELS:
            ch_vids = fetch_channel_recent_videos(ch, max_age_days=YOUTUBE_MAX_AGE_DAYS)
            raw_videos.extend(ch_vids)
            
    topic_vids = search_youtube_videos(topic, max_results=MAX_YOUTUBE_ITEMS)
    raw_videos.extend(topic_vids)

    print(f"      Found {len(raw_videos)} total YouTube video highlights.")

    # 3. Generate Summaries
    print(f"[3/4] Summarizing media and news...")
    news_summaries = summarize_news(raw_news)
    yt_summaries = summarize_youtube(raw_videos)

    # 4. Generate HTML and Export for OneNote
    print(f"[4/4] Generating OneNote briefing page...")
    html_content = generate_onenote_html(topic, news_summaries, yt_summaries)
    saved_path = export_to_file(topic, html_content, OUTPUT_DIR)

    print(f"\n[+] Briefing complete!")
    print(f"[*] Saved HTML Briefing File: file:///{saved_path.replace(os.sep, '/')}")
    
    # Try OneNote COM Post
    publish_to_onenote_com(saved_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OneNote News & Media Briefing Generator")
    parser.add_argument("--topic", type=str, help="Specific topic keyword (or leave empty to run all established topics)")
    args = parser.parse_args()

    if args.topic:
        run_briefing(args.topic)
    else:
        print(f"[*] Running briefing for all established topics: {DEFAULT_TOPICS}")
        for t in DEFAULT_TOPICS:
            run_briefing(t)

    # Update web dashboard index.html & publish to GitHub Pages
    print("\n[5/5] Updating Web Dashboard index.html...")
    index_file = update_index_dashboard(OUTPUT_DIR)
    print(f"[*] Dashboard index updated: file:///{index_file.replace(os.sep, '/')}")
    
    print("\n[+] Publishing updates to GitHub...")
    publish_to_github(OUTPUT_DIR)
