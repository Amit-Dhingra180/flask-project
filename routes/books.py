from flask import Blueprint, request, jsonify
from typing import List, Dict
from database.db_utils import get_db_connection

books_bp = Blueprint('books', __name__)

@books_bp.route("/books", methods=["GET"])
def get_books():
    page = request.args.get("page", 1, type=int)  
    per_page = request.args.get("per_page", 10, type=int)  
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?", (per_page, (page - 1) * per_page))
        books = cursor.fetchall()
        return jsonify([{"id": book[0], "name": book[1]} for book in books])

@books_bp.route("/books", methods=["POST"])
def add_book() -> Dict[str, str]:
    """
    Adds a new book to the database.
    :return: A dictionary containing a success message
    """
    data = request.get_json()
    book_name = data.get("name")
    
    if not book_name:
        return jsonify({"error": "Book name is required"}), 400
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (name) VALUES (?)", (book_name,))
        conn.commit()
        return jsonify({"message": f"Book '{book_name}' added successfully!"}), 201
