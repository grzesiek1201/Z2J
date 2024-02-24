import psycopg2
from psycopg2 import Error
import queue
import threading
import time
import random


class ConnectionPool:
    def __init__(self, max_connections=100):
        self.max_connections = max_connections
        self.connection_pool = queue.Queue(maxsize=max_connections)
        self.connection_lock = threading.Lock()
        self.current_connections = 0
        self.initialize_connections()
        self.semaphore = threading.Semaphore(max_connections)
        self.running = True

    def initialize_connections(self):
        for _ in range(10):
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
            self.execute_simple_select(connection)
            return connection
        except (Exception, Error) as e:
            print("Error creating connection:", e)
            pass
            return None

    def execute_simple_select(self, connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
        except Exception as e:
            print("Error executing select:", e)

    def get_connection(self):
        try:
            with self.connection_lock:
                if self.connection_pool.empty() and self.current_connections < self.max_connections:
                    self.add_connection()
            self.semaphore.acquire()
            connection = self.connection_pool.get(timeout=5)
            return connection
        except queue.Empty:
            print("No available connections in the pool. Retrying...")
            return None

    def add_connection(self):
        connection = self.create_connection()
        if connection:
            with self.connection_lock:
                self.connection_pool.put(connection)
                self.current_connections += 1

    def release_connection(self, connection):
        if connection:
            with self.connection_lock:
                self.connection_pool.put(connection)
                if self.connection_pool.full():
                    self.semaphore.release()
                    
    def check_conn(self):
        while self.running:
            time.sleep(2)
            with self.connection_lock:
                print(
                    f"Current connections: {self.current_connections}\nReleased connections: {self.max_connections - self.connection_pool.qsize()}\nQueue size: {self.connection_pool.qsize()}\n")

    def add_random_connections(self):
        start_time = time.time()
        while self.running and time.time() - start_time < 300:
            time.sleep(2)
            random_connections = random.randint(10, 30)
            for _ in range(random_connections):
                self.add_connection()

    def cleanup_connections(self):
        while self.running:
            time.sleep(5)
            with self.connection_lock:
                min_connections = 10 
                connections_to_release = max(self.current_connections - min_connections, 0)
                for _ in range(connections_to_release):
                    connection = self.connection_pool.get()
                    connection.close()
                    self.current_connections -= 1

    def stop(self):
        self.running = False


if __name__ == "__main__":
    pool = ConnectionPool(max_connections=100)

    check_conn_thread = threading.Thread(target=pool.check_conn)
    check_conn_thread.start()

    add_random_connections_thread = threading.Thread(target=pool.add_random_connections)
    add_random_connections_thread.start()

    cleanup_connections_thread = threading.Thread(target=pool.cleanup_connections)
    cleanup_connections_thread.start()

    check_conn_thread.join()
    add_random_connections_thread.join()
    cleanup_connections_thread.join()
    
