import urllib.request
import re

url = 'https://www.youtube.com/watch?v=eCp6ixlzyh0'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

title = re.search(r'<title>(.*?)</title>', html)
print("TITLE:", title.group(1) if title else "Unknown")

channel = re.search(r'"ownerChannelName":"([^"]+)"', html)
print("CHANNEL:", channel.group(1) if channel else "Unknown")

from youtube_transcript_api import YouTubeTranscriptApi
ytt = YouTubeTranscriptApi()
try:
    t = ytt.fetch('eCp6ixlzyh0')
    text = ' '.join([item.text for item in t[:300]])
    print("TRANSCRIPT SNIPPET:", text[:1000])
except Exception as e:
    print("TRANSCRIPT ERROR:", e)
