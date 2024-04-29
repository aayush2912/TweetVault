"""

@author: Rohit Kulkarni
"""

from cache import Cache
import time
import atexit
import os

def clear_cache_on_shutdown():
    global cache
    cache = None  

atexit.register(clear_cache_on_shutdown)

def main():
    cache = Cache(max_size=5, expiry_time=10)
    cache.set(1, 'data1')
    cache.set(2, 'data2')
    cache.set(3, 'data3')
    cache.save_checkpoint('cache_data.pkl')
    time.sleep(5)
    time.sleep(5)
    print("Cache contents after expiry time:")
    print(cache.cache)
    os.remove('cache_data.pkl')

if __name__ == "__main__":
    main()
