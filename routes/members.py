from flask import Blueprint, request, jsonify
from typing import List, Dict
from database.db_utils import get_db_connection

members_bp = Blueprint('members', __name__)

@members_bp.route("/members", methods=["GET"])
def get_members():
    page = request.args.get("page", 1, type=int)  
    per_page = request.args.get("per_page", 10, type=int)  
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members LIMIT ? OFFSET ?", (per_page, (page - 1) * per_page))
        members = cursor.fetchall()
        return jsonify([{"id": member[0], "name": member[1]} for member in members])

@members_bp.route("/members", methods=["POST"])
def add_member() -> Dict[str, str]:
    """
    Adds a new member to the database.
    :return: A dictionary containing a success message
    """
    data = request.get_json()
    member_name = data.get("name")
    
    if not member_name:
        return jsonify({"error": "Member name is required"}), 400
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO members (name) VALUES (?)", (member_name,))
        conn.commit()
        return jsonify({"message": f"Member '{member_name}' added successfully!"}), 201
