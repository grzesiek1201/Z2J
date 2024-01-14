import psycopg2
from psycopg2 import Error

class DbBase:
    def __init__(self):
        self.connection = None
        self.connected = False

    def __enter__(self):
        self.DB_HOST = "localhost"
        self.DB_DATABASE = "postgres"
        self.DB_USER = "postgres"
        self.DB_PASSWORD = "postgres"
        self.DB_PORT = 5433

        if not self.connected or (self.connection and self.connection.closed):
            try:
                self.connection = psycopg2.connect(
                    host=self.DB_HOST,
                    user=self.DB_USER,
                    password=self.DB_PASSWORD,
                    dbname=self.DB_DATABASE,
                    port=self.DB_PORT,
                    sslmode='disable'
                )
                self.connection.autocommit = True
                self.connected = True
                print("Connected to PostgreSQL")
            except (Exception, Error) as error:
                print("Error while connecting to PostgreSQL:", error)

        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connected and self.connection:
            print("Before closing PostgreSQL connection:", self.connection)
            self.connection.close()
            self.connected = False
            print("PostgreSQL connection is closed")

    def execute_sql(self, sql, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                self.connection.commit()
        except (Exception, Error) as error:
            print(f"Error executing SQL query: {error}")

    def db_server_start(self):
        try:
            connection = self.connection
            if not connection or connection.closed:
                raise Exception("Connection not established or closed.")

            print("Connected to UsersBase - DB")

            print("Before executing SQL queries:", connection)
            create_table_users_base = '''
                CREATE TABLE IF NOT EXISTS UsersBase (
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(255) NOT NULL DEFAULT 'USER'
                );
            '''
            self.execute_sql(create_table_users_base)

            create_table_users_messages = '''
                CREATE TABLE IF NOT EXISTS UsersMessages (
                    sender VARCHAR(255) NOT NULL,
                    recipient VARCHAR(255) NOT NULL,
                    message VARCHAR(255) NOT NULL
                );
            '''
            self.execute_sql(create_table_users_messages)

            print("After executing SQL queries:", connection)

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL:", error)

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
