from server import Server
from options import Options
from mailbox import Mailbox


class MAIN:
    HOST = "127.0.0.1"
    PORT = 61247
    INFO = "version: 0.0.2. ALPHA, from 24.08.2023"


if __name__ == "__main__":
    options_instance = Options()
    mailbox_instance = Mailbox(username=options_instance.logged_in_client)
    server = Server(MAIN.HOST, MAIN.PORT, MAIN.INFO, options_instance, mailbox_instance)
    server.start()
