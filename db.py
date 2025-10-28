import mysql.connector

class Database:
    def __init__(self, host = 'localhost', user = 'root', password = '', database = 'nlp_app'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.create_database() #The moment the Database  is instantiated, it should connect to the database

    #a generic method that will be used to connect to the database in other methods
    def connect(self):
        return mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
    
    def create_database(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        conn.commit()
        cursor.close()
        conn.close()

    def create_user_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

    def add_user(self, first_name, email, password):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (first_name, email, password) VALUES (%s, %s, %s)", (first_name, email, password))
        conn.commit()
        cursor.close()
        conn.close()

    def get_user_by_email(self, email):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    
    def validate_user(self, email, password):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user