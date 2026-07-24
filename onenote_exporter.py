import os
import datetime
import xml.etree.ElementTree as ET

def generate_onenote_html(topic: str, news_summaries: list[dict], yt_summaries: list[dict]) -> str:
    """
    Generates rich, modern HTML content structured perfectly for OneNote page importing.
    """
    today_str = datetime.date.today().strftime("%B %d, %Y")
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{topic} - Media & News Briefing ({today_str})</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #222222;
            line-height: 1.6;
            margin: 20px;
            max-width: 800px;
        }}
        h1 {{
            color: #7719aa;
            border-bottom: 2px solid #7719aa;
            padding-bottom: 8px;
            font-size: 24px;
        }}
        h2 {{
            color: #2b579a;
            margin-top: 24px;
            font-size: 18px;
        }}
        .card {{
            background: #f9f9fb;
            border-left: 4px solid #7719aa;
            padding: 12px 16px;
            margin-bottom: 16px;
            border-radius: 4px;
        }}
        .card-yt {{
            border-left-color: #cc181e;
        }}
        .title-link {{
            font-size: 16px;
            font-weight: bold;
            color: #0066cc;
            text-decoration: none;
        }}
        .title-link:hover {{
            text-decoration: underline;
        }}
        .metadata {{
            font-size: 12px;
            color: #666666;
            margin-top: 4px;
            margin-bottom: 8px;
        }}
        ul {{
            margin: 4px 0 0 20px;
            padding: 0;
        }}
        li {{
            margin-bottom: 4px;
        }}
        .badge {{
            display: inline-block;
            background: #e1dfdd;
            color: #323130;
            font-size: 11px;
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <h1>📰 Daily Media & News Briefing: {topic}</h1>
    <p><strong>Date:</strong> {today_str}</p>
    
    <h2>🌐 Top News Articles</h2>
"""
    if news_summaries:
        for item in news_summaries:
            bullets_html = "".join([f"<li>{b}</li>" for b in item['bullets']])
            html += f"""
    <div class="card">
        <div>
            <a class="title-link" href="{item['link']}" target="_blank">{item['title']}</a>
            <span class="badge">{item['source']}</span>
        </div>
        <div class="metadata">Published: {item.get('pub_date', 'Recently')}</div>
        <ul>
            {bullets_html}
        </ul>
    </div>
"""
    else:
        html += "<p><em>No news items retrieved.</em></p>"

    html += f"<h2>📺 YouTube Video Highlights</h2>"

    if yt_summaries:
        for item in yt_summaries:
            bullets_html = "".join([f"<li>{b}</li>" for b in item['bullets']])
            html += f"""
    <div class="card card-yt">
        <div>
            <a class="title-link" href="{item['link']}" target="_blank">▶ {item['title']}</a>
            <span class="badge">{item['channel']}</span>
        </div>
        <ul>
            {bullets_html}
        </ul>
    </div>
"""
    else:
        html += "<p><em>No YouTube video highlights retrieved.</em></p>"

    html += """
    <hr>
    <p style="font-size: 11px; color: #888888;">Generated automatically by Antigravity OneNote News & Media Briefing Tool.</p>
</body>
</html>
"""
    return html

def export_to_file(topic: str, html_content: str, output_dir: str) -> str:
    """
    Saves HTML briefing file inside a date-stamped subfolder under briefings/.
    Example path: briefings/2026-07-23/briefing_artificial_intelligence.html
    """
    today_folder = datetime.date.today().strftime('%Y-%m-%d')
    briefings_dir = os.path.join(output_dir, "briefings", today_folder)
    os.makedirs(briefings_dir, exist_ok=True)
    
    safe_topic = topic.replace(" ", "_").lower()
    filename = f"briefing_{safe_topic}.html"
    filepath = os.path.join(briefings_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return filepath

def publish_to_onenote_com(html_filepath: str) -> bool:
    """
    Attempts to publish directly to Windows OneNote Win32 Desktop App via COM Interop.
    """
    try:
        import win32com.client
        onenote = win32com.client.Dispatch("OneNote.Application")
        
        # Query hierarchy to find default/first section
        xml_out = ""
        _, xml_out = onenote.GetHierarchy("", 1, xml_out)
        
        # Parse xml to find first section ID
        root = ET.fromstring(xml_out)
        ns = {'one': 'http://schemas.microsoft.com/office/onenote/2013/onedoc'}
        
        # Find first section node
        section = root.find('.//one:Section', ns)
        if section is None:
            # Fallback search without namespace
            section = root.find('.//Section')

        if section is not None:
            section_id = section.attrib.get('ID')
            page_id = ""
            _, page_id = onenote.CreateNewPage(section_id, page_id)
            print(f"[+] Successfully created new OneNote page (ID: {page_id}) in Section: {section.attrib.get('name')}")
            return True
        else:
            print("[i] OneNote app responded, but no open sections were found in default notebook.")
            return False
    except Exception as e:
        print(f"[i] Note on direct OneNote application sync: {e}")
        return False
