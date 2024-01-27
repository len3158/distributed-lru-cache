import pika
from pika import exceptions
import json
import threading
import logging


class Messaging:
    def __init__(self, cache_instance, host='localhost'):
        """
        Initialize the Messaging system for the cache.

        :param cache_instance: The instance of the GeoDistributedLRUCache.
        :param host: The host of the RabbitMQ server.
        """
        self.host = host
        self.connection_params = pika.ConnectionParameters(self.host)
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()
        self.cache_instance = cache_instance
        self.setup_queues()
        self.setup_messaging()

    def setup_queues(self):
        for region in self.cache_instance.regions:
            self.channel.queue_declare(queue=region)

    def start_consumer_thread(self):
        for region in self.cache_instance.regions:
            thread = threading.Thread(target=self.consume_messages, args=(region,))
            thread.daemon = True
            thread.start()

    def consume_messages(self, region):
        channel = self.connection.channel()  # Create a new channel for this thread
        channel.basic_consume(queue=region, on_message_callback=self.on_message, auto_ack=True)
        try:
            channel.start_consuming()
        finally:
            channel.close()
            self.connection.close()

    def setup_messaging(self):
        """
        Setup the messaging system with RabbitMQ.
        """
        try:
            self.connection_params = pika.ConnectionParameters(self.host)
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()

            for region in self.cache_instance.regions:
                self.setup_region_queue(region)
        except pika.exceptions.AMQPConnectionError as e:
            logging.error("Failed to connect to RabbitMQ: %s", e)
            # Handle connection error here, possibly retry

    def setup_region_queue(self, region):
        """
        Set up a queue for a specific region.

        :param region: The name of the region.
        """
        try:
            self.channel.queue_declare(queue=region)
            self.channel.basic_consume(queue=region, on_message_callback=self.on_message, auto_ack=True)

            thread = threading.Thread(target=self.start_consuming, args=(region,))
            thread.daemon = True
            thread.start()
        except pika.exceptions.ChannelError as e:
            logging.error("Failed to declare queue or start consumer for region %s: %s", region, e)
            # Handle channel error here

    def start_consuming(self, region):
        """
        Start consuming messages from the queue.

        :param region: The name of the region.
        """
        try:
            self.channel.start_consuming()
        except pika.exceptions.ConnectionClosedByBroker:
            logging.error("Connection closed by broker for region: %s", region)
        except pika.exceptions.AMQPChannelError as e:
            logging.error("Channel error for region %s: %s", region, e)
        except pika.exceptions.AMQPConnectionError as e:
            logging.error("Connection error for region %s: %s", region, e)

    def on_message(self, ch, method, properties, body):
        """
        Callback function for handling incoming messages.

        :param ch: The channel.
        :param method: The method frame.
        :param properties: Properties.
        :param body: The message body.
        """
        self.cache_instance.update_cache(body, method.routing_key)

    def publish_update(self, message, region):
        """
        Publish an update to all region queues except the originating region.

        :param message: The message to be published.
        :param region: The originating region.
        """
        try:
            for reg in self.cache_instance.regions:
                if reg != region:
                    self.channel.basic_publish(exchange='', routing_key=reg, body=message)
        except pika.exceptions.AMQPConnectionError as e:
            logging.error("Failed to publish message: %s", e)
            # Handle publishing error here, possibly retry
