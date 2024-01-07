import json
import os
from datetime import datetime
from mailbox import Mailbox
from sql_table import DbBase
import psycopg2
from psycopg2 import Error


class Options:
    def __init__(self, server_info):
        self.start_time = datetime.now()
        self.logged_in_client = None
        self.server_info = server_info
        self.db = DbBase()

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
            "show_all_u(admin only) - shows all users",
            "show_all_m(admin only) - shows all messages"
        ]
        help_text = "\n".join(help_commands_list)
        return json.dumps({"help": help_text})

    def get_time(self):
        current_time = datetime.now()
        return str(current_time - self.start_time)

    def uptime(self):
        uptime = self.get_time()
        return json.dumps({"uptime": uptime})

    def get_info(self, server_info):
        return {"info": str(server_info)}

    def info(self):
        return json.dumps(self.get_info(self.server_info))

    def help(self):
        return self.get_help()

    def stop(self, conn):
        response = {"stop": "Server and client stopped."}
        conn.sendall(json.dumps(response).encode("utf-8"))
        conn.close()
        return None

    def register(self, username, password):
        try:
            self.db.register_user(username, password)
            return json.dumps({"register": "Registration successful."})
        except Exception as e:
            return json.dumps({"register": f"Error during registration: {str(e)}"})

    def login(self, username, password):
        try:
            role = self.db.authenticate_user(username, password)
            if role:
                self.logged_in_client = username
                return json.dumps({"login": "Login successful."})
            else:
                return json.dumps({"login": "Invalid username or password."})
        except Exception as e:
            return json.dumps({"login": f"Error during login: {str(e)}"})

    def get_user_role(self, username):
        try:
            role = self.db.get_user_role(username)
            return role
        except Exception as e:
            return None

    def send_message(self, sender, recipient, message):
        if self.logged_in_client != sender:
            return json.dumps({"send": "You are not logged in."})

        try:
            with self.db as db:
                response = db.send_message(sender, recipient, message)
        except Exception as e:
            response = f"Error sending message: {str(e)}"

        return json.dumps({"send": response})

    def read_messages(self, username):
        if self.logged_in_client != username:
            return "You are not logged in."

        try:
            with self.db as db:
                messages = db.read_messages(username)
                return json.dumps({"read_messages": messages}, indent=4)
        except Exception as e:
            return json.dumps({"error": f"Error reading messages: {str(e)}"})

    def show_all_m(self, username, recipient):
        if username == "admin":
            try:
                with self.db as db:
                    messages = db.show_all_messages(recipient)
                    return json.dumps({"show_all_m": messages}, indent=4)
            except Exception as e:
                return json.dumps({"error": f"Error showing all messages: {str(e)}"})
        else:
            return json.dumps({"error": "You do not have permission to read messages."})

    def show_all_u(self, username):
        if username == "admin":
            try:
                with self.db as db:
                    users = db.show_all_users()
                    return json.dumps({"show_all_u": users}, indent=4)
            except Exception as e:
                return json.dumps({"error": f"Error showing all users: {str(e)}"})
        else:
            return json.dumps({"error": "Only admin can do that."})

    def delete_user(self, username, user_to_delete):
        if username == "admin":
            try:
                with self.db as db:
                    db.delete_user(user_to_delete)
                response = f"User {user_to_delete} has been deleted."
            except Exception as e:
                response = f"Error deleting user {user_to_delete}: {str(e)}"
        else:
            response = "Only admin can do that."

        return json.dumps({"delete": response})
