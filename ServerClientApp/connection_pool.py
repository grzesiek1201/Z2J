import psycopg2
from psycopg2 import Error
import queue
import threading
import time
from multiprocessing import Value

class ConnectionPool:
    def __init__(self, max_connections=300):
        self.max_connections = max_connections
        self.connection_pool = queue.Queue(maxsize=max_connections)
        self.connection_lock = threading.Lock()
        self.current_connections = Value('i', 0)
        self.connections_released = Value('i', 0)
        self.initialize_connections()

    def initialize_connections(self):
        for _ in range(self.max_connections):
            connection = self.create_connection()
            if connection:
                self.connection_pool.put(connection)
                with self.current_connections.get_lock():
                    self.current_connections.value += 1

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
            self.execute_simple_select(connection)
            return connection
        except (Exception, Error) as e:
            print("Error creating connection:", e)
            return None

    def execute_simple_select(self, connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
        except Exception as e:
            print("Error executing select:", e)

    def get_connection(self):
        while True:
            try:
                with self.connection_lock:
                    connection = self.connection_pool.get(timeout=5)
                return connection
            except queue.Empty:
                print("No available connections in the pool. Retrying...")
                time.sleep(1)

    def release_connection(self, connection):
        if connection:
            with self.connection_lock:
                self.connection_pool.put(connection)
                with self.connections_released.get_lock():
                    self.connections_released.value += 1

    def check_conn(self):
        while True:
            time.sleep(2.0)
            with self.current_connections.get_lock():
                with self.connections_released.get_lock():
                    print(f"Active conn: {self.current_connections.value}\nReleased conn: {self.connections_released.value}\nQueue size: {self.connection_pool.qsize()}\n")


