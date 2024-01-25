import socket
import json
from sql_table import DbBase


class Server:
    def __init__(self, host, port, server_info, options, mailbox, db):
        self.host = host
        self.port = port
        self.server_info = server_info
        self.options = options
        self.mailbox = mailbox
        self.max_messages = 5
        self.max_message_length = 255
        self.db = db

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Server listening on {self.host}:{self.port}")
            try:
                while True:
                    conn, addr = s.accept()
                    with conn:
                        print(f"Connected to {addr}")
                        while True:
                            data = conn.recv(1024).decode("utf-8")
                            if not data:
                                break
                            response = self.handle_command(data, conn, addr)
                            if response is None:
                                print("disconnected")
                                break

                            conn.sendall(response.encode("utf-8"))
            except KeyboardInterrupt:
                print("Server interrupted. Stopping...")
                return

    def handle_command(self, command, conn, addr):
        command_parts = command.split()
        command_name = command_parts[0].lower()

        command_handlers = {
            "uptime": self.options.uptime,
            "info": self.options.info,
            "help": self.options.help,
            "register": lambda: self.options.register(*command_parts[1:]),
            "login": lambda: self.options.login(*command_parts[1:]),
            "send": lambda: self.options.send_message(self.options.logged_in_client, *command_parts[1:]),
            "read": lambda: json.dumps({"read": self.options.read_messages(self.options.logged_in_client)}),
            "show_all_m": lambda: self.options.show_all_m(self.options.logged_in_client, *command_parts[1:]),
            "show_all_u": lambda: self.options.show_all_u(self.options.logged_in_client, *command_parts[1:]),
            "delete": lambda: self.options.delete_user(self.options.logged_in_client, *command_parts[1:]),
            "stop": self.options.stop
        }

        return command_handlers.get(command_name, lambda: "Unknown command")()
