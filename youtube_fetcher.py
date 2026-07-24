import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import json
import re

def get_channel_id_from_handle(handle: str) -> tuple[str, str]:
    """
    Resolves YouTube handle (e.g. '@mkbhd') to (channel_id, channel_name).
    """
    clean_handle = handle.strip()
    if not clean_handle.startswith("@"):
        clean_handle = f"@{clean_handle}"
        
    url = f"https://www.youtube.com/{clean_handle}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')

        # Find channelId in meta tags or script JSON
        match_id = re.search(r'meta itemprop="identifier" content="(UC[a-zA-Z0-9_-]+)"', html)
        if not match_id:
            match_id = re.search(r'"channelId":"(UC[a-zA-Z0-9_-]+)"', html)

        channel_id = match_id.group(1) if match_id else None

        # Find channel name
        match_name = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        channel_name = match_name.group(1) if match_name else handle

        return channel_id, channel_name
    except Exception as e:
        print(f"[!] Could not resolve handle '{handle}': {e}")
        return None, handle

def fetch_channel_recent_videos(channel_handle_or_id: str, max_age_days: int = 3) -> list[dict]:
    """
    Fetches videos from a specific YouTube channel published within the last max_age_days.
    """
    if channel_handle_or_id.startswith("UC") and len(channel_handle_or_id) == 24:
        channel_id = channel_handle_or_id
        channel_name = channel_handle_or_id
    else:
        channel_id, channel_name = get_channel_id_from_handle(channel_handle_or_id)

    if not channel_id:
        print(f"[!] Skipping '{channel_handle_or_id}': Channel ID not found.")
        return []

    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    req = urllib.request.Request(
        rss_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )

    cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=max_age_days)
    recent_videos = []

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015', 'media': 'http://search.yahoo.com/mrss/'}

        for entry in root.findall('atom:entry', ns):
            title = entry.findtext('atom:title', default='No Title', namespaces=ns)
            link_elem = entry.find('atom:link', ns)
            link = link_elem.attrib.get('href', '#') if link_elem is not None else '#'
            published_str = entry.findtext('atom:published', default='', namespaces=ns)
            
            # Extract video snippet/description
            media_group = entry.find('media:group', ns)
            snippet = ""
            if media_group is not None:
                desc_elem = media_group.find('media:description', ns)
                if desc_elem is not None and desc_elem.text:
                    snippet = desc_elem.text[:300]

            # Parse published date and filter by max_age_days
            if published_str:
                pub_dt = datetime.datetime.fromisoformat(published_str.replace("Z", "+00:00"))
                if pub_dt >= cutoff_date:
                    recent_videos.append({
                        "title": title,
                        "link": link,
                        "channel": channel_name,
                        "pub_date": pub_dt.strftime("%Y-%m-%d %H:%M UTC"),
                        "snippet": snippet
                    })

        print(f"[+] Found {len(recent_videos)} video(s) for '{channel_name}' published in last {max_age_days} days.")
        return recent_videos

    except Exception as e:
        print(f"[!] Error fetching RSS for channel '{channel_handle_or_id}': {e}")
        return []

def search_youtube_videos(query: str, max_results: int = 3) -> list[dict]:
    """
    Searches YouTube for top videos matching a query string.
    """
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.youtube.com/results?search_query={encoded_query}"

    req = urllib.request.Request(
        search_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64); en-US"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')

        match = re.search(r'var ytInitialData = ({.*?});</script>', html_content)
        if not match:
            match = re.search(r'window\["ytInitialData"\] = ({.*?});', html_content)

        videos = []
        if match:
            data = json.loads(match.group(1))
            contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
            
            for section in contents:
                item_list = section.get('itemSectionRenderer', {}).get('contents', [])
                for item in item_list:
                    v = item.get('videoRenderer')
                    if v and len(videos) < max_results:
                        video_id = v.get('videoId')
                        title = v.get('title', {}).get('runs', [{}])[0].get('text', 'No Title')
                        channel = v.get('ownerText', {}).get('runs', [{}])[0].get('text', 'Unknown Channel')
                        snippet = v.get('detailedMetadataSnippets', [{}])[0].get('snippetText', {}).get('runs', [{}])[0].get('text', '')

                        if video_id:
                            videos.append({
                                "video_id": video_id,
                                "title": title,
                                "link": f"https://www.youtube.com/watch?v={video_id}",
                                "channel": channel,
                                "snippet": snippet
                            })
        return videos
    except Exception as e:
        print(f"[!] Error searching YouTube for '{query}': {e}")
        return []

if __name__ == "__main__":
    vids = fetch_channel_recent_videos("@mkbhd", max_age_days=3)
    for v in vids:
        print(f"- {v['title']} ({v['pub_date']})")
