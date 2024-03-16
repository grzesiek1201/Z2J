import psycopg2
from psycopg2 import Error
import queue
import threading
import time


class ConnectionPool:
    def __init__(self, max_connections=100):
        self.max_connections = max_connections
        self.connection_lock = threading.Lock()
        self.current_connections = 0
        self.released_connections = 0
        self.initialize_connections()

    def initialize_connections(self):
        self.connection_pool = queue.Queue(maxsize=self.max_connections)
        for _ in range(self.max_connections):
            connection = self.create_connection()
            if connection:
                self.connection_pool.put(connection)
                self.current_connections += 1

    def create_connection(self):
        try:
            connection = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="postgres",
                dbname="postgres",
                port=5433,
                client_encoding="utf-8"
            )
            return connection
        except (Exception, Error) as e:
            print("Error creating connection:", e)
            return None

    def get_connection(self, max_retries=3, retry_interval=1):
        retries = 0
        while retries < max_retries:
            try:
                with self.connection_lock:
                    if self.current_connections >= self.max_connections:
                        print("Connection limit reached. Unable to acquire connection.")
                        return None
                    if self.connection_pool.empty():
                        self.add_connection()
                connection = self.connection_pool.get_nowait()
                self.current_connections += 1
                return connection
            except queue.Empty:
                print("No available connections in the pool. Retrying...")
                retries += 1
                time.sleep(retry_interval)
        print("Unable to acquire connection after retries.")
        return None

    def add_connection(self):
        with self.connection_lock:
            if self.current_connections < self.max_connections:
                connection = self.create_connection()
                if connection:
                    self.connection_pool.put_nowait(connection)
                    self.current_connections += 1
            else:
                print("Cannot add more connections. Maximum limit reached.")

    def release_connection(self, connection):
        if connection:
            with self.connection_lock:
                self.connection_pool.put(connection)
                self.current_connections -= 1
                self.released_connections += 1

    def remove_inactive_connections(self):
        with self.connection_lock:
            removed_count = 0
            while self.current_connections > 10:
                try:
                    connection = self.connection_pool.get_nowait()
                    connection.close()
                    removed_count += 1
                    self.current_connections -= 1
                except queue.Empty:
                    # Queue is empty, no more connections to remove
                    break
            self.released_connections += removed_count

    def stop(self):
        with self.connection_lock:
            while not self.connection_pool.empty():
                connection = self.connection_pool.get()
                connection.close()
                self.current_connections -= 1
            self.current_connections = 0

    def print_connection_status(self):
        with self.connection_lock:
            active_connections = self.max_connections - self.connection_pool.qsize()
            queue_size = self.connection_pool.qsize()
            released_connections = self.released_connections
            print(
                f"Connections in queue: {queue_size}. Active connections: {active_connections}. Released connections: {released_connections}.")

    def destroy_error_connections(self):
        with self.connection_lock:
            while not self.connection_pool.empty():
                connection = self.connection_pool.get_nowait()
                connection.close()
                self.current_connections -= 1
            print("Destroyed connections with errors.")


if __name__ == "__main__":
    pool = ConnectionPool(max_connections=100)
