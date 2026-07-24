import os
import datetime

def update_index_dashboard(output_dir: str):
    """
    Scans the briefings/ directory and generates a clean index.html dashboard listing all daily briefings.
    """
    briefings_root = os.path.join(output_dir, "briefings")
    if not os.path.exists(briefings_root):
        return

    # Find all date folders (e.g. 2026-07-23)
    date_folders = sorted([d for d in os.listdir(briefings_root) if os.path.isdir(os.path.join(briefings_root, d))], reverse=True)

    dates_html = ""
    for date_str in date_folders:
        folder_path = os.path.join(briefings_root, date_str)
        files = sorted([f for f in os.listdir(folder_path) if f.endswith(".html")])
        
        links_html = ""
        for f in files:
            topic_name = f.replace("briefing_", "").replace(".html", "").replace("_", " ").title()
            rel_path = f"briefings/{date_str}/{f}"
            links_html += f"""
            <a class="briefing-badge" href="{rel_path}" target="_blank">
                📖 {topic_name}
            </a>
            """

        dates_html += f"""
        <div class="date-card">
            <h3>📅 {date_str}</h3>
            <div class="briefing-links">
                {links_html}
            </div>
        </div>
        """

    index_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily News & Media Briefings Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .container {{
            max-width: 800px;
            width: 100%;
        }}
        header {{
            border-bottom: 2px solid #334155;
            padding-bottom: 16px;
            margin-bottom: 32px;
        }}
        h1 {{
            color: #38bdf8;
            margin: 0 0 8px 0;
            font-size: 28px;
        }}
        p {{
            color: #94a3b8;
            margin: 0;
        }}
        .date-card {{
            background: #1e293b;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #334155;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .date-card h3 {{
            margin-top: 0;
            margin-bottom: 12px;
            color: #f1f5f9;
            font-size: 18px;
        }}
        .briefing-links {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .briefing-badge {{
            display: inline-block;
            background: #0284c7;
            color: #ffffff;
            text-decoration: none;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            transition: background 0.2s ease;
        }}
        .briefing-badge:hover {{
            background: #0369a1;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌐 Daily Media & News Briefings Dashboard</h1>
            <p>Automated daily digest of Google News and YouTube highlights.</p>
        </header>
        {dates_html if dates_html else '<p>No briefings generated yet.</p>'}
    </div>
</body>
</html>
"""
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    return index_path
