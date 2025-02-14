import os
from datetime import datetime

import yt_dlp


def download_video(config, url, category):
    base_downloads = config.get("general", "downloads")
    category_path = config.get("paths", category)

    if not category_path:
        category_path = config.get("paths", "df")

    final_path = str(os.path.join(base_downloads, category_path))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    options = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': f'{final_path}/{timestamp}_%(title)s.%(ext)s',  # Save path
        'writesubtitles': True,  # Download subtitles
        'subtitleslangs': ['en'],  # Subtitles language
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Convert to mp4
        }],
        'ignoreerrors': True,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error: {e}")