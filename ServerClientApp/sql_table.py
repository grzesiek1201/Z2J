import psycopg2
from psycopg2 import Error

class DbBase:
    def __init__(self):
        self.DB_HOST = "127.0.0.1"
        self.DB_DATABASE = "UsersBase"
        self.DB_USER = "franek"
        self.DB_PASSWORD = "kimono"
        self.DB_PORT = 5432
        self.connection = psycopg2.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            dbname=self.DB_DATABASE,
            port=self.DB_PORT,
            sslmode = 'disable'
        )

    def __enter__(self):
        self.connection = psycopg2.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            dbname=self.DB_DATABASE,
            port=self.DB_PORT,
            sslmode='disable'
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection is closed")

    def db_server_start(self):
        try:
            connection = self.connection
            print("Connected to UsersBase - DB")

            cursor = connection.cursor()

            create_table_users_base = '''
                CREATE TABLE UsersBase (
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(255) NOT NULL DEFAULT 'USER'
                );
            '''
            cursor.execute(create_table_users_base)
            connection.commit()

            create_table_users_messages = '''
                CREATE TABLE UsersMessages (
                    sender VARCHAR(255) NOT NULL,
                    recipient VARCHAR(255) NOT NULL,
                    message VARCHAR(255) NOT NULL
                );
            '''
            cursor.execute(create_table_users_messages)
            connection.commit()

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    def register_user(self, username, password):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO UsersBase (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

    def authenticate_user(self, username, password):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT role FROM UsersBase WHERE username = %s AND password = %s", (username, password))
            role = cursor.fetchone()
            return role[0] if role else None
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def get_user_role(self, username):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT role FROM UsersBase WHERE username = %s", (username,))
            role = cursor.fetchone()
            return role[0] if role else None
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def register_user(self, username, password):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO UsersBase (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

    def authenticate_user(self, username, password):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT role FROM UsersBase WHERE username = %s AND password = %s", (username, password))
            role = cursor.fetchone()
            return role[0] if role else None
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def get_user_role(self, username):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT role FROM UsersBase WHERE username = %s", (username,))
            role = cursor.fetchone()
            return role[0] if role else None
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def delete_user(self, username):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM UsersBase WHERE username = %s", (username,))
            connection.commit()
        except psycopg2.Error as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

    def send_message(self, sender, recipient, message):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO UsersMessages (sender, recipient, message) VALUES (%s, %s, %s)",
                           (sender, recipient, message))
            connection.commit()
            return "Message sent."
        except psycopg2.Error as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

    def read_messages(self, username):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT sender, message FROM UsersMessages WHERE recipient = %s", (username,))
            messages = cursor.fetchall()
            return messages
        except psycopg2.Error as e:
            raise e
        finally:
            cursor.close()

    def show_all_messages(self, recipient):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT sender, message FROM UsersMessages WHERE recipient = %s", (recipient,))
            messages = cursor.fetchall()
            return messages
        except psycopg2.Error as e:
            raise e
        finally:
            cursor.close()

    def show_all_users(self):
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT username, role FROM UsersBase")
            users = cursor.fetchall()
            return users
        except psycopg2.Error as e:
            raise e
        finally:
            cursor.close()

    def db_server_close(self):
        connection = self.connection
        connection.close()
        print('Server DB - CLOSED')
