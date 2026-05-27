from fastapi import FastAPI
import mysql.connector

conn_obj=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Syed@0756",
    database="expense_tracker"
)
cur_obj = conn_obj.cursor()

app = FastAPI()
@app.post("/expense")
def add_expense(new_data: dict):
    title = new_data["t"]
    amount = new_data["a"]
    category = new_data["c"]
    date = new_data["d"]
    query = "insert into expenses(title,amount,category,date) values (%s,%s,%s,%s)"
    values = (title,amount,category,date)
    cur_obj.execute(query,values)
    conn_obj.commit()
    return{"message":"expenses add succesfully"}
@app.get("/expense")
def view_expenses():
    query = "select * from expenses "
    cur_obj.execute(query)
    data = cur_obj.fetchall()
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

        cur_obj.execute(query, values)
        conn_obj.commit()

        return {"message":"updated successfully"}

    except Exception as e:
        return {"error": str(e)}
@app.delete("/expense/{expense_id}")
def delete_expenses(expense_id:int):
    query = "delete from expenses where expense_id = %s"
    values = (expense_id,)
    cur_obj.execute(query,values)
    conn_obj.commit()
    return {"message":" deleted succesfully"}
@app.get("/expense/search/{keyword}")
def search_expenses(keyword: str):
    query = "select * from expenses where title like %s or category like %s"
    values = (f"%{keyword}%", f"%{keyword}%")
    cur_obj.execute(query, values)
    data = cur_obj.fetchall()
    return data
@app.get("/expense/sort/{sort_by}")
def sort_expenses(sort_by: str):
    allowed = ["amount", "date", "category", "title"]
    if sort_by not in allowed:
        return {"error": "invalid sort option"}
    query = f"select * from expenses order by {sort_by}"
    cur_obj.execute(query)
    data = cur_obj.fetchall()
    return data
@app.get("/expense/filter/{category}")
def filter_expenses(category: str):
    query = "select * from expenses where category=%s"
    values = (category,)
    cur_obj.execute(query, values)
    data = cur_obj.fetchall()
    return data
@app.get("/expense/analyze")
def analyze_spending():
    query = "select category, sum(amount) from expenses group by category"
    cur_obj.execute(query)
    data = cur_obj.fetchall()
    return data





