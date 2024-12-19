# Library Management System API
This is a simple Library Management System built using Flask. It allows users to manage books, members, and transactions, such as borrowing and returning books.

## Table of Contents
How to Run the Project
Design Choices
Assumptions and Limitations

## How to Run the Project
### Prerequisites
Before running the project, make sure you have the following installed:

Python 3.x

Flask

SQLite

### Steps to Run the Project

1. Clone the Repository

2. Install Dependencies: Install the required Python packages using pip:

pip install -r requirements.txt

3. Run the Flask App: After initializing the database, you can start the Flask development server:

python main.py

By default, the app will run on http://127.0.0.1:5000/.

Access the API: You can now access the API endpoints using tools like Postman or curl.

## Design Choices
1. Flask Framework:
Reasoning: Flask was chosen because it's lightweight and easy to use for small projects like this one. It allows for quick development of RESTful APIs.
2. Database:
SQLite: The project uses SQLite for simplicity and ease of use in development. It is a self-contained, serverless database engine that stores data in a single file.
3. RESTful API Design:
Reasoning: The project follows REST principles to expose resources (books, members, transactions) through standard HTTP methods (GET, POST).
 The following endpoints are available:
/books (GET, POST): To get all books and add a new book.
/members (GET, POST): To get all members and add a new member.
/borrow (POST): To borrow a book.
/return (POST): To return a borrowed book.
5. Error Handling:
Reasoning: Basic error handling is implemented for cases such as missing book IDs, invalid transaction IDs, or unavailable books.
Assumptions and Limitations

## Assumptions and Limitations
Database Schema:

The database is assumed to have the following tables:

### books: 
id

name

author

published_date

genre

isbn

description

available

### members: 
id

name

email

phone_number

membership_start_date

membership_end_date

### transactions:
id member_id

book_id

borrow_date

return_date

The project does not include user authentication or authorization, so there is no way to securely manage who can access or modify the system.

The system does not handle overdue books or impose any fines for late returns.
