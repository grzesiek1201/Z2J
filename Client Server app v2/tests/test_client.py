import unittest
import socket
from client import Client
from unittest.mock import patch


class Client:
    def __init__(self):
        self.server = None

    def connect_to_server(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def send_command(self, command):
        if self.server:
            self.server.sendall(command.encode())

    def receive_data(self):
        if self.server:
            return self.server.recv(1024).decode()


class TestClientServerInteraction(unittest.TestCase):

    @patch('socket.socket')
    def test_client_server_interaction(self, mock_socket):
        print("Test 1 - Connecting to server")
        client = Client()
        client.connect_to_server('localhost', 8888)

        # Test sending a 'help' command from the client to the server
        print("Test 2 - Sending a 'help' command")
        command = "help"
        client.send_command(command)
        mock_socket.return_value.sendall.assert_called_once_with(command.encode())

        # Simulating the server response for 'help' command
        print("Test 3 - Simulating server response for 'help' command")
        mock_socket.return_value.recv.return_value = b'Help response'
        response = client.receive_data()
        self.assertEqual(response, "Help response")

        # Test sending an 'uptime' command from the client to the server
        print("Test 4 - Sending an 'uptime' command")
        command = "uptime"
        client.send_command(command)
        mock_socket.return_value.sendall.assert_called_with(command.encode())

        # Simulating the server response for 'uptime' command
        print("Test 5 - Simulating server response for 'uptime' command")
        mock_socket.return_value.recv.return_value = b'Uptime response'
        response = client.receive_data()
        self.assertEqual(response, "Uptime response")

        # Test sending an 'info' command from the client to the server
        print("Test 6 - Sending an 'info' command")
        command = "info"
        client.send_command(command)
        mock_socket.return_value.sendall.assert_called_with(command.encode())

        # Simulating the server response for 'info' command
        print("Test 7 - Simulating server response for 'info' command")
        mock_socket.return_value.recv.return_value = b'Info response'
        response = client.receive_data()
        self.assertEqual(response, "Info response")


if __name__ == '__main__':
    unittest.main()
