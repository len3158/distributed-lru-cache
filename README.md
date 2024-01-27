## Geo Distributed LRU Cache System
Introduction
The Geo Distributed LRU (Least Recently Used) Cache System is designed to optimize data retrieval across geographically
distributed locations, ensuring data consistency, high availability, and fault tolerance. 
By implementing an LRU eviction policy combined with time expiration for cache entries, 
the system provides an efficient caching solution that is resilient to network failures and ensures data is served from 
the closest region to reduce latency.

## Features
Geo-Distributed Caching: Cache data is replicated across multiple geographic locations to ensure fast access times and high availability.
LRU Eviction: Utilizes a Least Recently Used (LRU) policy for cache eviction, ensuring the most frequently accessed data is always available.
Time Expiration: Cache entries have a configurable time-to-live (TTL), after which they are automatically invalidated.
Resilience to Network Failures: Designed with robust error handling to gracefully handle network interruptions and maintain data consistency.
Flexible Schema: Supports caching of diverse data types with a flexible schema.
Real-Time Replication: Ensures near real-time replication of data across all geographical locations to maintain consistency.

## Project Structure

````
src/
│   main.py
│   __init__.py
├───cache/
│     geocache.py
│     lrucache.py
│     __init__.py
├───exceptions/
│     exceptions.py
│     __init__.py
├───messaging/
│     circuitbreaker.py
│     messaging.py
│     __init__.py
├───utils/
      config.py
      utils.py
      __init__.py
tests/
│   test_geocache.py
│   __init__.py
````

**cache/**: Contains the core caching logic, including the geo-distributed cache and LRU cache implementations.
**exceptions/**: Custom exception classes used throughout the project.
**messaging/**: Components responsible for handling inter-service communication and data replication.
**utils/**: Utility functions and common configurations.
**tests/**: Unit and integration tests for the project components.

## Getting Started
Prerequisites
Python 3.8+
RabbitMQ Server

## Installation
Clone the repository:

``
git clone https://github.com/yourusername/geo-distributed-lru-cache.git
``

Navigate to the project directory:

``
cd geo-distributed-lru-cache
``

Install the required dependencies:

``
pip install -r requirements.txt
``

### Configuration
Configure the system by editing the src/utils/config.py file to set cache capacities, expiration times, and RabbitMQ server details.

### Running the Application
Start the application by running the main.py script:

## Usage
Example usage of the Geo Distributed LRU Cache can be found in main.py. Here's a basic example:


from src.cache.geocache import GeoDistributedLRUCache

## Initialize the cache
``
cache = GeoDistributedLRUCache(regions=['us-east', 'eu-central'])
``

## Add an item to the cache
``
cache.put(key='myKey', value='myValue', region='us-east')
``

## Retrieve an item from the cache
``value = cache.get(key='myKey', region='eu-central')
print(value)  # Output: 'myValue'
``

## Testing
Run the unit tests to verify the system's functionality:

``
python -m unittest discover -s tests
``

## License
This project is licensed under the MIT License - see the LICENSE file for details.