import unittest
import time
from src.cache.lrucache import LRUCache


class TestLRUCache(unittest.TestCase):

    def test_cache_initialization(self):
        cache = LRUCache(capacity=3, expiration_time=10)
        self.assertEqual(cache.capacity, 3, "Cache capacity should be initialized to 3")
        self.assertEqual(cache.expiration_time, 10, "Cache expiration time should be initialized to 10 seconds")

    def test_basic_put_and_get(self):
        cache = LRUCache(capacity=2, expiration_time=10)
        cache.put("key1", "value1")
        result = cache.get("key1")
        self.assertEqual(result, "value1", "Failed to get the correct value for 'key1'")

    def test_lru_eviction_policy(self):
        cache = LRUCache(capacity=2, expiration_time=10)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.get("key1")  # Access key1 to make it recently used
        cache.put("key3", "value3")  # This should evict key2
        result = cache.get("key2")
        self.assertEqual(result, -1, "LRU eviction policy failed")

    def test_cache_expiration(self):
        cache = LRUCache(capacity=2, expiration_time=1)
        cache.put("key1", "value1")
        time.sleep(1.1)  # Wait for key1 to expire
        result = cache.get("key1")
        self.assertEqual(result, -1, "Cache expiration failed")

    def test_updating_existing_keys(self):
        cache = LRUCache(capacity=2, expiration_time=10)
        cache.put("key1", "value1")
        cache.put("key1", "value2")  # Update key1
        result = cache.get("key1")
        self.assertEqual(result, "value2", "Failed to update the existing key")

    def test_concurrent_access(self):
        cache = LRUCache(capacity=2, expiration_time=10)
        cache.put("key1", "value1")
        # Simulate concurrent access by interleaving gets and puts
        cache.put("key2", "value2")
        cache.get("key1")
        cache.put("key3", "value3")
        result1 = cache.get("key1")
        result2 = cache.get("key2")
        self.assertEqual(result1, "value1", "Concurrent access to 'key1' failed")
        self.assertEqual(result2, -1, "Concurrent access should have evicted 'key2'")

    def test_retrieving_non_existent_keys(self):
        cache = LRUCache(capacity=2, expiration_time=10)
        result = cache.get("nonexistent")
        self.assertEqual(result, -1, "Retrieving a non-existent key should return -1")

    def test_cache_capacity_limits(self):
        cache = LRUCache(capacity=2, expiration_time=10)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")  # Should evict key1
        self.assertEqual(cache.get("key1"), -1, "Cache exceeded its capacity limit")

    def test_access_patterns(self):
        cache = LRUCache(capacity=3, expiration_time=10)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.get("key1")  # Access key1 to make it recently used
        cache.put("key3", "value3")
        cache.put("key4", "value4")  # Should evict key2
        self.assertEqual(cache.get("key2"), -1, "Access patterns did not affect eviction as expected")

    def test_stale_data_retrieval(self):
        cache = LRUCache(capacity=2, expiration_time=1)  # 1 second expiration
        cache.put("key1", "value1")
        time.sleep(1.1)  # Wait for the key to expire
        result = cache.get_stale_data("key1")
        self.assertEqual(result, "value1", "Failed to retrieve stale data for 'key1'")


if __name__ == '__main__':
    unittest.main()
