import os

# Default topics to fetch Google News for
DEFAULT_TOPICS = [
    "Artificial Intelligence",
    "Tech News",
    "cybersecurity",
    "ethical hacking",
    "data science",
    "machine learning",
    "deep learning",
]

# Max news items to fetch per topic
MAX_NEWS_ITEMS = 5

# Max YouTube search items
MAX_YOUTUBE_ITEMS = 3

# YouTube Channel Monitoring
# You can list YouTube channel handles (e.g. "@mkbhd", "@lexfridman", "@Veritasium") or channel IDs
YOUTUBE_CHANNELS = [
    "@networkchuck",
    "@level1techs",
]

# How many days back to look for new YouTube videos (e.g. 3 = last 3 days)
YOUTUBE_MAX_AGE_DAYS = 3

# Maximum age of local & web briefing folders to keep (e.g. 7 days). Older folders will be deleted automatically.
MAX_BRIEFING_AGE_DAYS = 7

# Directory to save generated HTML briefing files
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
