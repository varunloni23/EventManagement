import mysql.connector
from mysql.connector import Error
import os
from flask import current_app
import time

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Varunloni@12',
                database='event_management',
                autocommit=True,
                consume_results=True  # Add this to automatically consume unread results
            )
            if self.connection.is_connected():
                print("Database connection successful")
            else:
                print("Failed to establish database connection")
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            self.connection = None
    
    def ensure_connection(self):
        """Ensure that the connection is active, reconnect if necessary."""
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                if self.connection is None or not self.connection.is_connected():
                    print("Connection lost, attempting to reconnect...")
                    self.connect()
                
                if self.connection and self.connection.is_connected():
                    return True
                    
            except Error as e:
                print(f"Error checking connection: {e}")
            
            attempts += 1
            if attempts < max_attempts:
                time.sleep(1)  # Wait before retrying
        
        return False
    
    def execute_query(self, query, params=None):
        if not self.ensure_connection():
            print("Failed to establish database connection after multiple attempts")
            return None
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            # Try to reconnect and execute again
            if self.ensure_connection():
                try:
                    cursor = self.connection.cursor(dictionary=True)
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    
                    return cursor
                except Error as e2:
                    print(f"Error executing query after reconnection: {e2}")
            return None
    
    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            result = cursor.fetchall()
            cursor.close()
            return result
        return []
    
    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            result = cursor.fetchone()
            cursor.close()
            return result
        return None
    
    def execute_and_get_id(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        return None
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

# Create a function to get the database instance
def get_db():
    if 'db' not in current_app.config:
        current_app.config['db'] = Database()
    return current_app.config['db']

# Create a function to close the database connection
def close_db(e=None):
    db = current_app.config.pop('db', None)
    if db is not None:
        db.close() 