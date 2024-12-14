import os


def create_paths(config):
    base_downloads = config.get("general", "downloads")
    create_folder_if_not_exists(base_downloads)

    paths = {key: os.path.join(base_downloads, value) for key, value in config.get("paths").items()}

    for key, path in paths.items():
        create_folder_if_not_exists(path)

def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
