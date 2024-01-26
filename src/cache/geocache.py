from .lrucache import LRUCache
from ..messaging import Messaging, CircuitBreaker
from threading import Lock
import json


class GeoDistributedLRUCache:
    def __init__(self, regions, capacity=5, expiration_time=300):
        """
        Initialize the Geo Distributed LRU Cache.

        :param regions: List of region names (e.g., 'us-east', 'eu-central').
        :param capacity: The capacity of the LRU cache in each region.
        :param expiration_time: The time after which a cache entry expires.
        """
        self.regions = {region: LRUCache(capacity, expiration_time) for region in regions}
        self.locks = {region: Lock() for region in regions}
        self.circuit_breaker = CircuitBreaker()
        self.messaging = Messaging(self)

    def get(self, key: str, region: str):
        """
        Retrieve a value from the cache for a given key and region.

        :param key: The key to retrieve.
        :param region: The region from which to retrieve the key.
        :return: The value associated with the key, or -1 if not found or expired.
        """
        try:
            return self.regions[region].get(key)
        except ConnectionError:
            return self.regions[region].get_stale_data(key)

    def put(self, key: str, value: str, region: str):
        """
        Add or update a key-value pair in the cache and replicate it across regions.

        :param key: The key to add or update.
        :param value: The value to associate with the key.
        :param region: The region where the write originates.
        """
        message = json.dumps({'key': key, 'value': value})
        self.messaging.publish_update(message, region)

    def update_cache(self, message, region):
        """
        Update the cache based on a message received from the message queue.

        :param message: The message containing the key-value pair to update.
        :param region: The region for which this update is applicable.
        """
        key, value = json.loads(message).get('key'), json.loads(message).get('value')
        with self.locks[region]:
            self.regions[region].put(key, value)
