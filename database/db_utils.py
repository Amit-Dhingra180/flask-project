import sqlite3
from typing import Optional

# Define a type for the database connection
DbConnection = sqlite3.Connection

def get_db_connection() -> DbConnection:
    """
    Establishes a connection to the SQLite database.
    :return: SQLite connection object
    """
    return sqlite3.connect('library.db')

def init_db() -> None:
    """
    Initializes the database by creating the necessary tables if they do not exist.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                author TEXT NOT NULL,
                published_date TEXT,
                genre TEXT,
                isbn TEXT UNIQUE,
                description TEXT,
                available BOOLEAN NOT NULL DEFAULT 1
            )
        ''')
        
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone_number TEXT,
                membership_start_date TEXT NOT NULL,
                membership_end_date TEXT
            )
        ''')
        
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrow_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (member_id) REFERENCES members (id),
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        ''')
        
        conn.commit()
