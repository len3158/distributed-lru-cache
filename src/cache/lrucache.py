from collections import OrderedDict
from ..utils import CACHE_CAPACITY, CACHE_EXPIRATION_TIME, CACHE_ELEMENT_TTL

import time

"""This file contains the LRUCache class, implementing a basic LRU (Least Recently Used) cache with expiration 
functionality."""


class LRUCache:
    def __init__(self, capacity=CACHE_CAPACITY, expiration_time=CACHE_EXPIRATION_TIME):
        """
        Initialize an LRU Cache.

        :param capacity: The Maximum number of items the cache can hold.
        :param expiration_time: Time in seconds after which an item expires.
        """
        self.cache = OrderedDict()
        self.capacity = capacity
        self.expiration_time = expiration_time

    def get(self, key: str):
        """
        Retrieve an item from the cache.

        :param key: Key of the item to retrieve.
        :return: The value associated with the key or -1 if the key is not present or expired.
        """
        if key not in self.cache or self._is_expired(key):
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]['value']

    def put(self, key: str, value: str):
        """
        Add a new item to the cache or update an existing one.

        :param key: Key of the item to add or update.
        :param value: Value of the item.
        """
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = {'value': value, CACHE_ELEMENT_TTL: time.time()}
        if len(self.cache) > self.capacity:  # If the cache is full, pop the oldest element
            self.cache.popitem(last=False)

    def _is_expired(self, key: str):
        """
        Check if a cache item has expired.

        :param key: Key of the item to check.
        :return: True if the item has expired, False otherwise.
        """
        return time.time() - self.cache[key][CACHE_ELEMENT_TTL] > self.expiration_time

    def get_stale_data(self, key: str):
        """
        Retrieve stale data from the cache if available.

        :param key: Key of the item to retrieve.
        :return: The value associated with the key, or -1 if not found.
        """
        return self.cache.get(key, {}).get('value', -1)

    def _clear_cache(self):
        """
        Clear the cache
        """
        self.cache.clear()
