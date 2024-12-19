import pytest
from flask import Flask
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from routes.books import books_bp
from database.db_utils import get_db_connection, init_db

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    app.register_blueprint(books_bp)
    init_db()  
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_books(client):
    response = client.get('/books')
    assert response.status_code == 200
    assert b"Book" in response.data  


def test_add_book(client):
    new_book = {"title": "New Book", "author": "Author Name", "available": True}
    response = client.post('/books', json=new_book)
    
    assert response.status_code == 201
    assert b"Book 'New Book' added successfully!" in response.data  


    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE title = ?", (new_book["title"],))
        book = cursor.fetchone()
        assert book is not None
        assert book[1] == new_book["title"] 

def test_get_book_by_id(client):
    response = client.get('/books/1')
    assert response.status_code == 200
    assert b"Book 1" in response.data 

def test_get_book_not_found(client):
    response = client.get('/books/999')
    assert response.status_code == 404
    assert b"Book not found" in response.data 

def test_update_book(client):
    updated_data = {"title": "Updated Book", "author": "Updated Author", "available": False}
    response = client.put('/books/1', json=updated_data)
    
    assert response.status_code == 200
    assert b"Book 1 updated successfully!" in response.data  # Assuming this message in response

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = 1")
        book = cursor.fetchone()
        assert book[1] == updated_data["title"]  # Check title update
        assert book[2] == updated_data["author"]  # Check author update

def test_delete_book(client):
    response = client.delete('/books/1')
    assert response.status_code == 200
    assert b"Book 1 deleted successfully!" in response.data  # Assuming this message in response

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = 1")
        book = cursor.fetchone()
        assert book is None
