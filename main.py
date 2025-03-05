import argparse
import os

from config import Config
from paths_mgt import create_paths
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

    # Parse arguments
    return parser.parse_args()

def main():
    config = load_config("config/config.yaml")

    create_paths(config)

    args = get_args(config)

    download_video(config, args.url, args.category, args.only_audio)


if __name__ == '__main__':
    main()
