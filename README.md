# OneNote News & Media Briefing Generator

A Python tool that fetches fresh news articles from Google News and video highlights/transcripts from YouTube, generates structured summaries with source links, and formats them into modern HTML pages ready for Microsoft OneNote.

## Features

- 🌐 **Google News Scraping**: Fetches fresh news headlines, publication dates, and source URLs.
- 📺 **YouTube Video Highlights**: Searches top relevant videos and extracts metadata/transcripts.
- 📝 **Structured Summarization**: Generates key bullet points with direct links to sources.
- 🎨 **OneNote-Ready HTML Export**: Produces cleanly styled documents with custom CSS cards, source badges, and hyperlinks optimized for OneNote.
- 🔌 **Windows OneNote Integration**: Compatible with Microsoft OneNote Desktop app and OneNote web importer.

---

## How to Run

### 1. Run for a Custom Topic
```powershell
python main.py --topic "Artificial Intelligence"
```
Or for other topics:
```powershell
python main.py --topic "SpaceX"
python main.py --topic "Tech News"
```

### 2. View Briefings
All generated briefings are saved in:
`briefings/briefing_<topic>_<date>.html`

You can open these files in any browser or copy & paste directly into your OneNote notebook pages!
