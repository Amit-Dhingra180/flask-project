from flask import Blueprint, request, jsonify
from database.db_utils import get_db_connection
from datetime import datetime
from typing import Dict

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route("/borrow", methods=["POST"])
def borrow_book() -> Dict[str, str]:
    """
    Allows a member to borrow a book.
    :return: A dictionary containing a success or error message
    """
    data = request.get_json()
    book_id = data.get("book_id")
    
    if not book_id:
        return jsonify({"error": "Book ID is required"}), 400

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        if not book:
            return jsonify({"error": "Book not found"}), 404
        if not book[0]:
            return jsonify({"error": "Book is already borrowed"}), 400
        
        cursor.execute(''' 
            INSERT INTO transactions (book_id, borrow_date)
            VALUES (?, ?)
        ''', (book_id, datetime.now().isoformat()))
        
        cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
        
        conn.commit()
        return jsonify({"message": f"Book {book_id} borrowed successfully!"}), 201

@transactions_bp.route("/return", methods=["POST"])
def return_book() -> Dict[str, str]:
    """
    Allows a member to return a borrowed book.
    :return: A dictionary containing a success or error message
    """
    data = request.get_json()
    transaction_id = data.get("transaction_id")
    
    if not transaction_id:
        return jsonify({"error": "Transaction ID is required"}), 400

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute(''' 
            SELECT book_id, return_date FROM transactions
            WHERE id = ?
        ''', (transaction_id,))
        transaction = cursor.fetchone()
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        if transaction[1]:
            return jsonify({"error": "Book is already returned"}), 400
        
        book_id = transaction[0]
        
        cursor.execute(''' 
            UPDATE transactions SET return_date = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), transaction_id))
        
        cursor.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
        
        conn.commit()
        return jsonify({"message": f"Book {book_id} returned successfully!"}), 200
