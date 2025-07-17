import mysql.connector
from mysql.connector import Error
from config.settings import db_config

class DatabaseConnector:

    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**db_config, consume_results=True)
            if self.connection.is_connected():
                return True

        except Error as e:
            print(f"Error connecting to MySQL: {e}") 
            return False
        return False

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None, fetch=False):
        cursor = None

        try:
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            cursor.execute(query, params or ())
            self.connection.commit()
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            cursor.close()
            return True
        
        except Error as e:
            print(f"Error executing query: {e}")
            if cursor:
                cursor.close()
            return False