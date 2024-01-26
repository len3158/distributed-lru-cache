class CacheError(Exception):
    """ Base class for cache-related errors """
    pass


class CacheConnectionError(CacheError):
    """ Raised when a connection error occurs in the cache system """
    pass


class MessagePublishError(CacheError):
    """ Raised when there is an error in publishing a message """
    pass


class MessageConsumeError(CacheError):
    """ Raised when there is an error in consuming a message """
    pass


class CircuitBreakerOpenError(CacheError):
    """ Raised when an operation is attempted while the circuit breaker is open """
    pass


class CacheKeyNotFoundError(CacheError):
    """ Raised when a key is not found in the cache """
    pass


class CacheCapacityError(CacheError):
    """ Raised when an operation exceeds the cache's capacity """
    pass


class CacheExpirationError(CacheError):
    """ Raised when there is an error related to cache expiration logic """
    pass
