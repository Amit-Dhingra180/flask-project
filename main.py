from flask import Flask
from database.db_utils import init_db
from routes.books import books_bp
from routes.members import members_bp
from routes.transactions import transactions_bp

app = Flask(__name__)

app.register_blueprint(books_bp)
app.register_blueprint(members_bp)
app.register_blueprint(transactions_bp)

def main() -> None:
    """
    Initialize the database and run the Flask app.
    :return: None
    """
    init_db()  
    app.run(debug=True)

if __name__ == "__main__":
    main()
