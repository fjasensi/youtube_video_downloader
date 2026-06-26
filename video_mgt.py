import os

import yt_dlp


VIDEO_FORMATS = {
    "mp4": {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "merge_output_format": "mp4",
    },
    "mkv": {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mkv",
    },
}


def download_video(config, url, category, only_audio, container="mp4"):
    base_downloads = os.path.expanduser(
        os.path.expandvars(config.get("general", "downloads"))
    )
    category_path = config.get("paths", category)

    if not category_path:
        category_path = config.get("paths", "df")

    final_path = str(os.path.join(base_downloads, category_path or ""))
    os.makedirs(final_path, exist_ok=True)

    output_template = os.path.join(final_path, '%(title)s.%(ext)s')
    shared_options = {
        'ignoreerrors': True,
        'noprogress': True,
        'remote_components': ['ejs:github'],
    }

    if not only_audio:
        video_format = VIDEO_FORMATS.get(container, VIDEO_FORMATS["mp4"])
        options = {
            **shared_options,
            'format': video_format["format"],
            'merge_output_format': video_format["merge_output_format"],
            'outtmpl': output_template,
            'writesubtitles': True,  # Download subtitles
            'subtitleslangs': ['en'],  # Subtitles language
        }
    else:
        options = {
            **shared_options,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
         }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error: {e}")
