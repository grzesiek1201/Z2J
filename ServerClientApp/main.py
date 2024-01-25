from server import Server
from options import Options
from mailbox import Mailbox
from sql_table import DbBase
import psycopg2
from psycopg2 import Error


class MAIN:
    HOST = "localhost"
    PORT = 5022
    INFO = "version: 0.7."


if __name__ == "__main__":
    options_instance = Options(MAIN.INFO)

    db = DbBase()
    db.db_server_start()

    mailbox_instance = Mailbox(username=options_instance.logged_in_client)
    server = Server(MAIN.HOST, MAIN.PORT, MAIN.INFO, options_instance, mailbox_instance, db)
    server.start()
