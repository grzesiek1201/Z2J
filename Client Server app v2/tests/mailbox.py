import json


class Mailbox:
    def __init__(self, username):
        self.username = username
        self.max_messages = 5
        self.max_message_length = 255
        self.messages = []
        self.load_messages()

    def send_message(self, sender, recipient, message):
        if len(message) > self.max_message_length:
            return "Message exceeds maximum length of {self.max_message_length} characters. Try again"
        self.messages.append({"recipient": recipient, "message": message, "sender": sender})
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
            return (f"{recipient} mailbox is full, the oldest message will be overwritten.")
        self.save_messages()
        return "Message sent."

    def read_messages_to(self, reader):
        messages = [msg for msg in self.messages if msg["recipient"] == reader]
        return messages

    def save_messages(self):
        with open(f"{self.username}_messages.json", 'w') as f:
            json.dump(self.messages, f)

    def load_messages(self):
        try:
            with open(f"{self.username}_messages.json", 'r') as f:
                self.messages = json.load(f)
        except FileNotFoundError:
            self.messages = []
