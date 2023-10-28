import unittest
import socket
import threading


class TestServerClientConnection(unittest.TestCase):

    def setUp(self):
        self.server = threading.Thread(target=self.start_server)
        self.server.daemon = True
        self.server.start()

    def start_server(self):
        print("Starting the server...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("127.0.0.1", 61247))
        self.server_socket.listen(1)

        connection, client_address = self.server_socket.accept()

        received_data = connection.recv(1024)
        if received_data:
            connection.sendall(b"Received data")
            print(f"Received data: {received_data.decode()}")

        connection.close()
        print("Server closed")

    def tearDown(self):
        self.server_socket.close()

    def test_server_client_connection(self):
        print("Testing server-client connection")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("127.0.0.1", 61247)

        try:
            client.connect(server_address)
            print("Connection established")
            client.sendall(b"Test data")
            received_response = client.recv(1024)
            print(f"Received response: {received_response.decode()}")
            self.assertEqual(received_response, b"Received data", "Invalid server response")

        except ConnectionRefusedError as e:
            self.fail(f"Connection to the server failed: {e}")
        finally:
            client.close()


if __name__ == '__main__':
    unittest.main()
