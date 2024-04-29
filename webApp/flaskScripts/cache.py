"""

@author:Rohit Kulkarni
"""

import pickle
import time

class Cache:

    def __init__(self, max_size=100, expiry_time=60):
        self.max_size = max_size
        self.expiry_time = expiry_time
        self.cache = {}

    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            self._remove_expired_entries()
        self.cache[key] = (value, time.time())

    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp <= self.expiry_time:
                return value
            else:
                del self.cache[key]  # Remove expired entry
        return None

    def _remove_expired_entries(self):
        current_time = time.time()
        keys_to_remove = [key for key, (value, timestamp) in self.cache.items() if current_time - timestamp > self.expiry_time]
        for key in keys_to_remove:
            del self.cache[key]

    def save_checkpoint(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump({'cache': self.cache}, f)

    def load_checkpoint(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
                if 'cache' in data:
                    self.cache = data['cache']
                else:
                    print("Cache data not found in the file. Starting with an empty cache.")
        except FileNotFoundError:
            print("Cache file not found. Starting with an empty cache.")
