import socket
import json
from sql_table import DbBase

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("localhost", 50221))
        self.logged_in = False
        self.logged_in_client = None
        self.db_instance = DbBase()

    def send_response(self, message):
        self.s.sendall(message.encode("utf-8"))
        data = self.s.recv(1024)
        try:
            response = json.loads(data.decode("utf-8"))
            print("Received JSON response:", response)
        except json.JSONDecodeError as e:
            print("Server response:", data.decode("utf-8"))
            print("JSON Decode Error:", e)
            return

    def get_help(self):
        self.send_response("help")

    def send_uptime(self):
        self.send_response("uptime")

    def send_info(self):
        self.send_response("info")

    def send_register(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        self.send_response(f"register {username} {password}")

    def send_login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        self.send_response(f"login {username} {password}")

    def send_message(self):
        recipient = input("Enter recipient: ")
        message = input("Enter message: ")
        self.send_response(f"send {recipient} {message}")

    def send_read(self):
        self.send_response("read")

    def send_show_all_messages(self):
        recipient = input("Enter recipient: ")
        self.send_response(f"show_all_m {recipient}")

    def send_show_all_users(self):
        self.send_response("show_all_u")

    def send_delete(self):
        user_to_delete = input("Enter username to delete: ")
        self.send_response(f"delete {user_to_delete}")

    def send_stop(self):
        self.send_response("stop")


if __name__ == "__main__":
    client = Client()


    command_options = {
        "help": client.get_help,
        "uptime": client.send_uptime,
        "info": client.send_info,
        "register": client.send_register,
        "login": client.send_login,
        "send": client.send_message,
        "read": client.send_read,
        "show_all_m": client.send_show_all_messages,
        "show_all_u": client.send_show_all_users,
        "delete": client.send_delete,
        "stop": client.send_stop
    }

    while True:
        command = input("Enter command: ")
        if command.lower() not in command_options:
            print("Unknown command:", command)
            continue

        command_options[command.lower()]()
        if command.lower() == "stop":
            break
