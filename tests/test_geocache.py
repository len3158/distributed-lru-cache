import json
import unittest
from unittest.mock import patch, MagicMock
from src.cache.geocache import GeoDistributedLRUCache


class TestGeoDistributedLRUCacheReplication(unittest.TestCase):

    def setUp(self):
        self.threads = []
        self.regions = ['us-east', 'eu-central']
        # Patch the Messaging class to avoid real RabbitMQ interactions - Remove this to test with a Server Instance
        with unittest.mock.patch('src.cache.geocache.Messaging') as MockMessaging:
            self.mock_messaging = MockMessaging.return_value
        self.geo_cache = GeoDistributedLRUCache(self.regions)

    # @patch('src.cache.geocache.Messaging.publish_update')
    # def test_replication_on_put(self, mock_publish_update):
    #     """
    #     Test that a put operation in one region triggers replication to other regions.
    #     """
    #     key, value, region = 'key1', 'value1', 'us-east'
    #     self.geo_cache.put(key, value, region)
    #
    #     # Verify that publish_update is called to replicate the data
    #     mock_publish_update.assert_called_once()

    @patch('src.cache.geocache.GeoDistributedLRUCache.update_cache')
    def test_update_cache_called_on_replication(self, mock_update_cache):
        """
        Test that the update_cache method is called when data is replicated.
        """
        # Simulate receiving a replication message
        message = json.dumps({'key': 'key1', 'value': 'value1', 'region': 'us-east'}).encode('utf-8')  # Serialize
        # and encode to bytes
        mock_method = MagicMock()  # Mock method object

        self.geo_cache.messaging.on_message(mock_method, message)

        # Verify that update_cache is called to update the local cache
        mock_update_cache.assert_called_once_with(message, mock_method.routing_key)

    # def test_data_consistency_across_regions(self):
    #     """
    #     Test that after replication, data is consistent across regions.
    #     """
    #     key, value, region = 'key1', 'value1', 'us-east'
    #
    #     # Directly call update_cache to simulate replication
    #     for reg in self.regions:
    #         self.geo_cache.update_cache({'key': key, 'value': value}, reg)
    #
    #     # Check that data is consistent across regions
    #     for reg in self.regions:
    #         self.assertEqual(self.geo_cache.get(key, reg), value, f"Data inconsistency in region {reg}")

    # def test_handling_network_failures_during_replication(self):
    #     """
    #     Test how the system handles network failures during replication.
    #     """
    #     key, value, region = 'key1', 'value1', 'us-east'
    #
    #     # Simulate a network failure by raising an exception in the publish_update method
    #     self.mock_messaging.publish_update.side_effect = Exception("Network failure")
    #
    #     with self.assertRaises(Exception):
    #         self.geo_cache.put(key, value, region)
    #
    #     # Verify that the system attempted to replicate the data despite the network failure
    #     self.mock_messaging.publish_update.assert_called_once()


if __name__ == '__main__':
    unittest.main()
