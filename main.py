import argparse
import os

from config import Config
from video_mgt import download_video


def load_config(file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, file_path)
    return Config(config_path)

def get_args(config):
    default_category = config.get("paths", "df")
    parser = argparse.ArgumentParser(description="Youtube video downloader.")

    # Add arguments
    parser.add_argument("url", type=str, help="Video url.")
    parser.add_argument("category", type=str, nargs="?", default=default_category,
                        help="Category folder to be saved (optional).")
    parser.add_argument("only_audio", type=bool, nargs='?', default=False,
            help="Download audio only.")
    parser.add_argument("--container", choices=("mp4", "mkv"), default="mp4",
                        help="Video container to be saved. Defaults to mp4.")

    # Parse arguments
    return parser.parse_args()

def main():
    config = load_config("config/config.yaml")

    args = get_args(config)

    download_video(config, args.url, args.category, args.only_audio, args.container)


if __name__ == '__main__':
    main()
