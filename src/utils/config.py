# Configuration for the Geo Distributed LRU Cache

# Cache Settings
CACHE_CAPACITY = 100  # Default capacity of the LRU Cache
CACHE_EXPIRATION_TIME = 300  # Time in seconds after which a cache item expires
CACHE_ELEMENT_TTL = 'ttl'  # Cache element expiration time

# RabbitMQ Settings
RABBITMQ_HOST = 'localhost'  # Hostname of the RabbitMQ server
RABBITMQ_PORT = 5672  # Port number for RabbitMQ
RABBITMQ_USERNAME = 'guest'  # Username for RabbitMQ
RABBITMQ_PASSWORD = 'guest'  # Password for RabbitMQ

# Circuit Breaker Settings
CIRCUIT_BREAKER_MAX_FAILURES = 3  # Number of failures before the circuit opens
CIRCUIT_BREAKER_RESET_TIME = 60  # Time in seconds to reset the circuit breaker

# Regions Configuration
REGIONS = ['us-east', 'eu-central', 'asia-south']  # List of regions in the distributed cache system

# Logging Settings
LOG_LEVEL = 'ERROR'  # Logging level (e.g., DEBUG, INFO, WARNING, ERROR)
