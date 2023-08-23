import socket
import json
import sys


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", 61247))
        self.logged_in = False
        self.logged_in_client = None

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

        if "help" in response:
            print(response["help"])
        elif "uptime" in response:
            print(response["uptime"])
        elif "info" in response:
            print(response["info"])
        elif "register" in response:
            print(response["register"])
        elif "login" in response:
            if response["login"] == "Login successful.":
                self.logged_in = True
                print("Login successful.")
            else:
                print("Login failed.")
        elif "send" in response:
            print(response["send"])
        elif "read" in response:
            print("Messages:")
            for msg in response["read"]:
                print(f"From: {msg['sender']}")
                print(f"Message: {msg['message']}")
        elif "show_all_m" in response:
            print(response["show_all_m"])
        elif "show_all_u" in response:
            print(response["show_all_u"])
        elif "delete" in response:
            print(response["delete"])
        elif "stop" in response:
            print(response["stop"])
            self.s.close()
            sys.exit(0)
        else:
            print("Unknown response:", response)


if __name__ == "__main__":
    client = Client()
    logged_in = False

    while True:
        command = input("Enter command (help, uptime, info, register, login, "
                        "send, read, show_all_m(admin only), show_all_u(admin only), delete(admin only)), "
                        "stop: ")
        client.send_response(command.lower())

        if command.lower() == "stop":
            break
