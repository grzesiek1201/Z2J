import json
import os
from datetime import datetime
from mailbox import Mailbox


class Options:
    def __init__(self):
        self.start_time = datetime.now()
        self.logged_in_client = None

    def get_help(self):
        help_commands_list = [
            "uptime - server work time",
            "info - version of the server",
            "help - the list of available commands",
            "stop - stopping server and client",
            "register - allows to register new user",
            "login - allows to login",
            "msg - allows to send a message",
            "read - allows to read your mailbox",
            "delete(admin only) - deletes user",
            "show_u(admin only) - shows all users",
            "show_m(admin only) - shows all messages"
        ]
        help_text = "\n".join(help_commands_list)
        return json.dumps({"help": help_text})

    def get_time(self):
        current_time = datetime.now()
        return str(current_time - self.start_time)

    def uptime(self):
        uptime = self.get_time()
        return json.dumps({"uptime": uptime})

    def info(self, server_info):
        return json.dumps({"info": server_info})

    def help(self):
        return self.get_help()

    def stop(self, conn):
        response = {"stop": "Server and client stopped."}
        conn.sendall(json.dumps(response).encode("utf-8"))
        conn.close()
        return None

    def register(self, username, password):
        users = self.load_users()
        for user in users['users']:
            if user['nick'] == username:
                return json.dumps({"register": "Username already exists."})

        new_user = {
            "nick": username,
            "password": password,
            "messages": [],
            "role": "user"
        }

        users['users'].append(new_user)
        self.save_users(users)
        return json.dumps({"register": "Registration successful."})

    def load_users(self):
        try:
            with open("users_login.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_users(self, users):
        with open("users_login.json", "w") as file:
            json.dump(users, file)

    def login(self, username, password):
        users_data = self.load_users()
        for user in users_data['users']:
            if user['nick'] == username and user['password'] == password:
                self.logged_in_client = username
                return json.dumps({"login": "Login successful."})
        return json.dumps({"login": "Invalid username or password."})

    def get_user_role(self, username):
        with open('user_info.json', 'r', encoding='utf-8') as file:
            user_data = json.load(file)
        if username in user_data:
            return user_data[username]["role"]
        return None

    def send_message(self, sender, recipient, message):
        if self.logged_in_client != sender:
            return json.dumps({"send": "You are not logged in."})
        recipient_mailbox = Mailbox(recipient)
        response = recipient_mailbox.send_message(sender, recipient, message)
        return json.dumps({"send": response})

    def read_messages(self, username):
        if self.logged_in_client != username:
            return "You are not logged in."
        recipient_mailbox = Mailbox(username)
        return recipient_mailbox.read_messages_to(username)

    def show_all_m(self, username, recipient):
        if username == "admin":
            messages_filename = f"{recipient}_messages.json"
            try:
                with open(messages_filename, "r") as messages_file:
                    messages_data = json.load(messages_file)
                    return json.dumps(messages_data, indent=4)
            except FileNotFoundError:
                return "User does not exist."
        else:
            return "You do not have permission to read messages."

    def show_all_u(self, username):
        if username == "admin":
            with open("users_login.json", "r") as file:
                users_data = json.load(file)
            formatted_users = []
            for user in users_data["users"]:
                formatted_user = f"nick: {user['nick']}, password: {user['password']}, role: {user['role']}"
                formatted_users.append(formatted_user)
            return "\n".join(formatted_users)
        else:
            return "Only admin can do that."

    def delete_user(self, username, user_to_delete):
        if username == "admin":
            users_data = self.load_users()
            user_exists = False
            for user in users_data["users"]:
                if user["nick"] == user_to_delete:
                    user_exists = True
                    break

            if user_exists:
                messages_filename = f"{user_to_delete}_messages.json"
                if os.path.exists(messages_filename):
                    os.rename(messages_filename, os.path.join("archives", messages_filename))
                users_data["users"] = [user for user in users_data["users"] if user["nick"] != user_to_delete]
                self.save_users(users_data)
                return f"User {user_to_delete} has been deleted."
            else:
                return "User does not exist."
        else:
            return "Only admin can do that."
