import socket
import json


class Server:
    def __init__(self, host, port, server_info, options, mailbox):
        self.host = host
        self.port = port
        self.server_info = server_info
        self.options = options
        self.mailbox = mailbox
        self.max_messages = 5
        self.max_message_length = 255

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
                            response = self.handle_command(data, conn)
                            if response is None:
                                print("disconnected")
                                break

                            conn.sendall(response.encode("utf-8"))
            except KeyboardInterrupt:
                print("Server interrupted. Stopping...")
                return

    def handle_command(self, command, conn):
        print("Received command:", command)
        if command == "uptime":
            return self.options.uptime()

        elif command == "info":
            return self.options.info(self.server_info)

        elif command == "help":
            return self.options.help()

        elif command.startswith("register"):
            _, username, password = command.split()
            return self.options.register(username, password)

        elif command.startswith("login"):
            _, username, password = command.split()
            return self.options.login(username, password)

        elif command.startswith("send"):
            _, recipient, *message_parts = command.split()
            message = " ".join(message_parts)
            response = self.options.send_message(self.options.logged_in_client, recipient, message)
            if "mailbox is full" in response:
                return json.dumps({"send": f"{recipient} mailbox is full. The oldest message will be overwritten"})
            if response == "Invalid user.":
                return json.dumps({"send": "Invalid user."})
            return response

        elif command == "read":
            print("Handling read command")
            if self.options.logged_in_client:
                response = self.options.read_messages(self.options.logged_in_client)
                response_dict = {"read": response}
                print("Sending response:", response_dict)
                conn.sendall(json.dumps(response_dict).encode("utf-8"))
            else:
                response = {"error": "You need to be logged in to read messages."}
                print("Sending response:", response)
                conn.sendall(json.dumps(response).encode("utf-8"))

        elif command.startswith("show_all_m"):
            _, recipient = command.split()
            response = self.options.show_all_m(self.options.logged_in_client, recipient)
            return json.dumps({"show_all_m": response})

        elif command.startswith("show_all_u"):
            response = self.options.show_all_u(self.options.logged_in_client)
            return json.dumps({"show_all_u": response})

        elif command.startswith("delete"):
            _, user_to_delete = command.split()
            response = self.options.delete_user(self.options.logged_in_client, user_to_delete)
            return json.dumps({"delete": response})

        elif command == "stop":
            return self.options.stop(conn)

        else:
            return "Unknown command"
