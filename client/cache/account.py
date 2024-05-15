import json
import os

from settings import CACHE_PATH


class CacheController:
    def __init__(self):
        self.cache_path = os.path.expanduser(CACHE_PATH)
        self.file_name = "user_data.json"
        self.full_path = os.path.join(self.cache_path, self.file_name)
        self.ensure_cache_exists()

    def ensure_cache_exists(self):
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        if not os.path.exists(self.full_path):
            with open(self.full_path, "w") as f:
                json.dump({}, f)

    def read_cache(self) -> dict:
        with open(file=self.full_path, mode="r", encoding="utf-8") as f:
            return json.loads(f.read())

    def write_cache(self, data: dict):
        with open(file=self.full_path, mode="w", encoding="utf-8") as f:
            json.dump(data, f)

    def clear_cache(self):
        with open(file=self.full_path, mode="w", encoding="utf-8") as f:
            json.dump({}, f)
