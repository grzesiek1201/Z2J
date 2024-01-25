import psycopg2
from psycopg2 import Error

class DbBase:
    def __init__(self):
        self.connection = None
        self.connected = False
        self.DB_HOST = "localhost"
        self.DB_DATABASE = "postgres"
        self.DB_USER = "postgres"
        self.DB_PASSWORD = "postgres"
        self.DB_PORT = 5433

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
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

    def disconnect(self):
        try:
            if self.connected and self.connection:
                print("Before closing PostgreSQL connection:", self.connection)
        finally:
            if self.connection is not None:
                self.connection.close()
                print("PostgreSQL connection is closed.")
                self.connected = False

    def execute_sql(self, sql, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            self.connection.commit()
        except (Exception, Error) as error:
            print(f"Error executing SQL query: {error}")
            print(f"SQL Query: {sql}")
            print(f"Params: {params}")
            raise
        finally:
            cursor.close()

    def db_server_start(self):
        try:
            self.connect()

            print("Connected to UsersBase - DB")

            print("Before executing SQL queries:", self.connection)
            create_table_users_base = '''
                CREATE TABLE IF NOT EXISTS UsersBase (
                    id SERIAL PRIMARY KEY,
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
            print("After executing SQL queries:", self.connection)

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL:", error)
        finally:
            pass

    def register_user(self, username, password):
        try:
            sql = "INSERT INTO UsersBase (username, password) VALUES (%s, %s)"
            params = (username, password)
            self.execute_sql(sql, params)
        except psycopg2.Error as e:
            self.connection.rollback()
            raise e

    def authenticate_user(self, username, password):
        try:
            with psycopg2.connect(
                    host=self.DB_HOST,
                    user=self.DB_USER,
                    password=self.DB_PASSWORD,
                    dbname=self.DB_DATABASE,
                    port=self.DB_PORT,
                    sslmode='disable'
            ) as connection:
                connection.autocommit = True
                sql = "SELECT role FROM UsersBase WHERE username = %s AND password = %s"
                params = (username, password)
                with connection.cursor() as cursor:
                    cursor.execute(sql, params)
                    role = cursor.fetchone()
                    print(f"SQL Query: {cursor.query}")
                    print(f"Params: {params}")
                    print(f"Retrieved Role: {role}")
                    return role[0] if role else None
        except psycopg2.Error as e:
            print(f"Error during authentication: {str(e)}")
            return None

    def get_user_role(self, username):
        try:
            sql = "SELECT role FROM UsersBase WHERE username = %s"
            params = (username,)
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                role = cursor.fetchone()
                return role[0] if role else None
        except psycopg2.Error as e:
            raise e

    def delete_user(self, username):
        try:
            sql = "DELETE FROM UsersBase WHERE username = %s"
            params = (username,)
            self.execute_sql(sql, params)
        except psycopg2.Error as e:
            self.connection.rollback()
            raise e

    def send_message(self, sender, recipient, message):
        try:
            sql = "INSERT INTO UsersMessages (sender, recipient, message) VALUES (%s, %s, %s)"
            params = (sender, recipient, message)
            self.execute_sql(sql, params)
            return "Message sent."
        except psycopg2.Error as e:
            print(f"Error sending message: {str(e)}")
            return f"Error sending message: {str(e)}"

    def read_messages(self, username):
        try:
            sql = "SELECT sender, message FROM UsersMessages WHERE recipient = %s"
            params = (username,)
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            messages = cursor.fetchall()
            cursor.close()
            return messages
        except psycopg2.Error as e:
            print(f"Error reading messages: {str(e)}")
            return f"Error reading messages: {str(e)}"

    def show_all_messages(self, recipient):
        try:
            sql = "SELECT sender, message FROM UsersMessages WHERE recipient = %s"
            params = (recipient,)
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                messages = cursor.fetchall()
                return messages
        except psycopg2.Error as e:
            raise e

    def show_all_users(self):
        try:
            sql = "SELECT username, role FROM UsersBase"
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                users = cursor.fetchall()
                return users
        except psycopg2.Error as e:
            raise e

    def db_server_close(self):
        self.disconnect()
        print('Server DB - CLOSED')
