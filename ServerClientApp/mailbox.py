from sql_table import DbBase


class Mailbox:
    def __init__(self, username):
        self.username = username
        self.max_messages = 5
        self.max_message_length = 255
        self.db = DbBase()

    def send_message(self, sender, recipient, message):
        if len(message) > self.max_message_length:
            return f"Message exceeds maximum length of {self.max_message_length} characters. Try again"

        try:
            with self.db as db:
                db.send_message(sender, recipient, message)
            return "Message sent."
        except Exception as e:
            return f"Error sending message: {str(e)}"

    def read_messages_to(self, reader):
        try:
            with self.db as db:
                messages = db.read_messages_to(reader)
            return messages
        except Exception as e:
            return f"Error reading messages: {str(e)}"
