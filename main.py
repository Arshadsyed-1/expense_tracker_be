from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE CONNECTION
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT"))
)

cursor = conn.cursor(dictionary=True)

# CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    amount DECIMAL(10,2),
    category VARCHAR(100),
    date DATE
)
""")

conn.commit()

# HOME ROUTE
@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}

# ADD EXPENSE
@app.post("/expense")
def add_expense(new_data: dict):

    title = new_data["t"]
    amount = new_data["a"]
    category = new_data["c"]
    date = new_data["d"]

    query = """
    INSERT INTO expenses(title, amount, category, date)
    VALUES(%s,%s,%s,%s)
    """

    values = (title, amount, category, date)

    cursor.execute(query, values)
    conn.commit()

    return {"message": "Expense added successfully"}

# VIEW EXPENSES
@app.get("/expense")
def view_expenses():

    query = "SELECT * FROM expenses"

    cursor.execute(query)

    data = cursor.fetchall()

    return data

# UPDATE EXPENSE
@app.put("/expense/{expense_id}")
def update_expense(expense_id: int, update_data: dict):

    try:

        title = update_data["t"]
        amount = update_data["a"]
        category = update_data["c"]
        date = update_data["d"]

        query = """
        UPDATE expenses
        SET title=%s,
            amount=%s,
            category=%s,
            date=%s
        WHERE expense_id=%s
        """

        values = (title, amount, category, date, expense_id)

        cursor.execute(query, values)

        conn.commit()

        return {"message": "Updated successfully"}

    except Exception as e:

        return {"error": str(e)}

# DELETE EXPENSE
@app.delete("/expense/{expense_id}")
def delete_expense(expense_id: int):

    query = "DELETE FROM expenses WHERE expense_id=%s"

    values = (expense_id,)

    cursor.execute(query, values)

    conn.commit()

    return {"message": "Deleted successfully"}

# SEARCH EXPENSES
@app.get("/expense/search/{keyword}")
def search_expenses(keyword: str):

    query = """
    SELECT * FROM expenses
    WHERE title LIKE %s
    OR category LIKE %s
    """

    values = (f"%{keyword}%", f"%{keyword}%")

    cursor.execute(query, values)

    data = cursor.fetchall()

    return data

# SORT EXPENSES
@app.get("/expense/sort/{sort_by}")
def sort_expenses(sort_by: str):

    allowed = ["amount", "date", "category", "title"]

    if sort_by not in allowed:

        return {"error": "Invalid sort option"}

    query = f"SELECT * FROM expenses ORDER BY {sort_by}"

    cursor.execute(query)

    data = cursor.fetchall()

    return data

# FILTER EXPENSES
@app.get("/expense/filter/{category}")
def filter_expenses(category: str):

    query = "SELECT * FROM expenses WHERE category=%s"

    values = (category,)

    cursor.execute(query, values)

    data = cursor.fetchall()

    return data

# ANALYZE SPENDING
@app.get("/expense/analyze")
def analyze_spending():

    query = """
    SELECT category,
    SUM(amount) AS total_amount
    FROM expenses
    GROUP BY category
    """

    cursor.execute(query)

    data = cursor.fetchall()

    return data