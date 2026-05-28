import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )

cursor = conn.cursor(dictionary=True)

cursor.execute("""
CREATE TABLE expenses(
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    amount DECIMAL(10,2),
    category VARCHAR(100),
    date DATE
); """)

conn.commit()

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}

app = FastAPI()
@app.post("/expense")
def add_expense(new_data: dict):
    title = new_data["t"]
    amount = new_data["a"]
    category = new_data["c"]
    date = new_data["d"]
    query = "insert into expenses(title,amount,category,date) values (%s,%s,%s,%s)"
    values = (title,amount,category,date)
    cursor.execute(query,values)
    conn.commit()
    return{"message":"expenses add succesfully"}
@app.get("/expense")
def view_expenses():
    query = "select * from expenses "
    cursor.execute(query)
    data = cursor.fetchall()
    return data
@app.put("/expense/{expense_id}")
def update_expense(expense_id:int, update_data: dict):

    try:
        title = update_data["t"]
        amount = (update_data["a"])
        category = update_data["c"]
        date = str(update_data["d"])

        query = """
        update expenses
        set title=%s, amount=%s, category=%s, date=%s
        where expense_id=%s
        """

        values = (title, amount, category, date, expense_id)

        cursor.execute(query, values)
        conn.commit()

        return {"message":"updated successfully"}

    except Exception as e:
        return {"error": str(e)}
@app.delete("/expense/{expense_id}")
def delete_expenses(expense_id:int):
    query = "delete from expenses where expense_id = %s"
    values = (expense_id,)
    cursor.execute(query,values)
    conn.commit()
    return {"message":" deleted succesfully"}
@app.get("/expense/search/{keyword}")
def search_expenses(keyword: str):
    query = "select * from expenses where title like %s or category like %s"
    values = (f"%{keyword}%", f"%{keyword}%")
    cursor.execute(query, values)
    data = cursor.fetchall()
    return data
@app.get("/expense/sort/{sort_by}")
def sort_expenses(sort_by: str):
    allowed = ["amount", "date", "category", "title"]
    if sort_by not in allowed:
        return {"error": "invalid sort option"}
    query = f"select * from expenses order by {sort_by}"
    cursor.execute(query)
    data = cursor.fetchall()
    return data
@app.get("/expense/filter/{category}")
def filter_expenses(category: str):
    query = "select * from expenses where category=%s"
    values = (category,)
    cursor.execute(query, values)
    data = cursor.fetchall()
    return data
@app.get("/expense/analyze")
def analyze_spending():
    query = "select category, sum(amount) from expenses group by category"
    cursor.execute(query)
    data = cursor.fetchall()
    return data





