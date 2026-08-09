import urllib.request
import re
import json

url = 'https://www.youtube.com/watch?v=Z73BPOWenfs'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

title = re.search(r'<title>(.*?)</title>', html)
print("TITLE:", title.group(1) if title else "Unknown")

channel = re.search(r'"ownerChannelName":"([^"]+)"', html)
print("CHANNEL:", channel.group(1) if channel else "Unknown")

desc = re.search(r'"shortDescription":"([^"]+)"', html)
print("DESCRIPTION:", desc.group(1)[:500] if desc else "Unknown")
