import yaml


class Config:
    def __init__(self, file_path):
        with open(file_path, "r") as file:
            self.config = yaml.safe_load(file)

    def get(self, *keys, default=None):
        value = self.config

        for key in keys:
            value = value.get(key, default)

            if value is None:
                return default

        return value
