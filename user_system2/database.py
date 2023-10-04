import psycopg2
from psycopg2 import sql
from configs.config import dbconfig

import psycopg2


class DatabaseHandler:
    # Class-level connection variable
    connection = None
    host = dbconfig["host"]
    database = dbconfig["database"]
    user = dbconfig["user"]
    password = dbconfig["password"]
    port = dbconfig["port"]

    # def __init__(self, host, database, user, password, port):
    #     self.host = host
    #     self.database = database
    #     self.user = user
    #     self.password = password
    #     self.port = port

    @staticmethod
    def connect():
        try:
            DatabaseHandler.connection = psycopg2.connect(
                host=DatabaseHandler.host,
                database=DatabaseHandler.database,
                user=DatabaseHandler.user,
                password=DatabaseHandler.password,
                port=DatabaseHandler.port
            )
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)

    @staticmethod
    def close_connection():
        if DatabaseHandler.connection:
            DatabaseHandler.connection.close()

    @staticmethod
    def create_table(tablename):
        try:
            cursor = DatabaseHandler.connection.cursor()
            create_table_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS {} (
                        user_id SERIAL PRIMARY KEY,
                        username VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL
                    )
                """).format(sql.Identifier(tablename))

            cursor.execute(create_table_query)
            DatabaseHandler.connection.commit()
            cursor.close()
            print(f"Table {tablename} created successfully.")
        except Exception as e:
            raise Exception(f"Error: Unable to create table - {str(e)}")

    @staticmethod
    def insert_record(username, password):
        try:
            cursor = DatabaseHandler.connection.cursor()

            insert_user_query = sql.SQL("""
                INSERT INTO user_data (username, password)
                VALUES (%s, %s)
                RETURNING user_id
            """)

            cursor.execute(insert_user_query, (username, password))
            user_id = cursor.fetchone()[0]
            DatabaseHandler.connection.commit()
            cursor.close()
            print(f"User with ID {user_id} created successfully.")
            return user_id
        except Exception as e:
            raise Exception(f"Error creating user - {str(e)}")

    @staticmethod
    def check_user_existence(username):
        try:
            cursor = DatabaseHandler.connection.cursor()
            check_user_exist = sql.SQL("""
                SELECT 1
                FROM user_data
                WHERE username = %s
            """)
            cursor.execute(check_user_exist, (username,))
            return bool(cursor.fetchone())
        except Exception as e:
            raise Exception(f"Error checking username - {str(e)}")


    @staticmethod
    def check_password_existence(password):
        try:
            cursor = DatabaseHandler.connection.cursor()
            check_user_exist = sql.SQL("""
                SELECT 1
                FROM user_data
                WHERE password = %s
            """)
            cursor.execute(check_user_exist, (password,))
            return bool(cursor.fetchone())
        except Exception as e:
            raise Exception(f"Error checking password - {str(e)}")


    @staticmethod
    def create_record(table_name, data):
        try:
            cursor = DatabaseHandler.connection.cursor()
            insert_query = f"INSERT INTO {table_name} (column1, column2) VALUES (%s, %s)"
            cursor.execute(insert_query, data)
            DatabaseHandler.connection.commit()
            cursor.close()
            print("Record inserted successfully.")
        except psycopg2.Error as e:
            DatabaseHandler.connection.rollback()
            print("Error inserting record:", e)

    @staticmethod
    def read_records(table_name):
        try:
            cursor = DatabaseHandler.connection.cursor()
            select_query = f"SELECT * FROM {table_name}"
            cursor.execute(select_query)
            results = cursor.fetchall()
            cursor.close()
            for row in results:
                print(row)
        except psycopg2.Error as e:
            print("Error reading records:", e)

    @staticmethod
    def update_record(table_name, new_value, condition_value):
        try:
            cursor = DatabaseHandler.connection.cursor()
            update_query = f"UPDATE {table_name} SET column1 = %s WHERE column2 = %s"
            cursor.execute(update_query, (new_value, condition_value))
            DatabaseHandler.connection.commit()
            cursor.close()
            print("Record updated successfully.")
        except psycopg2.Error as e:
            DatabaseHandler.connection.rollback()
            print("Error updating record:", e)

    @staticmethod
    def delete_record(table_name, value_to_delete):
        try:
            cursor = DatabaseHandler.connection.cursor()
            delete_query = f"DELETE FROM {table_name} WHERE column = %s"
            cursor.execute(delete_query, (value_to_delete,))
            DatabaseHandler.connection.commit()
            cursor.close()
            print("Record deleted successfully.")
        except psycopg2.Error as e:
            DatabaseHandler.connection.rollback()
            print("Error deleting record:", e)


db = DatabaseHandler()
db.connect()
