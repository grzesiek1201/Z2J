import unittest
import time
from threading import Thread
from connection_pool import ConnectionPool


class TestConnectionPool(unittest.TestCase):
    def setUp(self):
        self.pool = ConnectionPool(max_connections=100)
        self.stop_threads = False

    def test_connection_operations(self):
        connection_thread = Thread(target=self.make_connections)
        removal_thread = Thread(target=self.remove_connections)

        connection_thread.start()
        removal_thread.start()

        connection_thread.join()
        removal_thread.join()

    def make_connections(self):
        while not self.stop_threads:
            for _ in range(20):
                self.pool.add_connection()
                self.pool.print_connection_status()
            time.sleep(0.5)

    def remove_connections(self):
        while not self.stop_threads:
            self.pool.remove_inactive_connections()
            self.pool.print_connection_status()
            time.sleep(2)

    def tearDown(self):
        self.stop_threads = True
        self.pool.stop()


if __name__ == "__main__":
    unittest.main()
