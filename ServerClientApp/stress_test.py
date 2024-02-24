import threading
import time
from connection_pool import ConnectionPool
from multiprocessing import Value

def worker(pool, completed_threads, completed_threads_lock, semaphore):
    while True:
        conn = None
        try:
            conn = pool.get_connection()
            if conn:
                with completed_threads_lock:
                    completed_threads.value += 1
                pool.release_connection(conn)
        finally:
            if conn:
                conn.close()
                semaphore.release()


def run_test(num_threads, pool):
    threads = []
    completed_threads = Value('i', 0)
    completed_threads_lock = threading.Lock()

    semaphore = threading.Semaphore(num_threads)

    for i in range(num_threads):
        semaphore.acquire()
        thread = threading.Thread(target=worker, args=(pool, completed_threads, completed_threads_lock, semaphore))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while completed_threads.value < num_threads:
        time.sleep(2.0)


if __name__ == "__main__":
    pool = ConnectionPool(max_connections=100)
    num_threads = 10

    check_conn_thread = threading.Thread(target=pool.check_conn)
    check_conn_thread.start()

    run_test(num_threads, pool)
