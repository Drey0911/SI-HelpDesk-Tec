import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno 
load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.port = int(os.getenv("DB_PORT", 3306))  
        self.connection = None
    
    def get_connection(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port
                )
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

# Instancia para la bd
db = Database()