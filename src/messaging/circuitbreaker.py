import time
from ..utils.config import CIRCUIT_BREAKER_MAX_FAILURES, CIRCUIT_BREAKER_RESET_TIME


class CircuitBreaker:
    def __init__(self, max_failures=CIRCUIT_BREAKER_MAX_FAILURES, reset_time=CIRCUIT_BREAKER_RESET_TIME):
        """
        Initialize the Circuit Breaker.

        :param max_failures: The maximum number of failures before the breaker opens.
        :param reset_time: The time in seconds to wait before resetting the breaker state.
        """
        self.max_failures = max_failures
        self.reset_time = reset_time
        self.failures = 0
        self.last_failure_time = None

    def record_failure(self):
        """
        Record a failure. Open the circuit breaker if the failure threshold is reached.
        """
        self.failures += 1
        self.last_failure_time = time.time()

        if self.failures >= self.max_failures:
            self.open()

    def reset(self):
        """
        Reset the circuit breaker to the closed state.
        """
        self.failures = 0
        self.last_failure_time = None

    def is_open(self):
        """
        Check if the circuit breaker is open.

        :return: True if the circuit breaker is open, False otherwise.
        """
        if self.failures < self.max_failures:
            return False
        return (time.time() - self.last_failure_time) < self.reset_time

    def open(self):
        """
        Open the circuit breaker.
        """
        self.failures = self.max_failures
        self.last_failure_time = time.time()
