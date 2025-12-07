# app.py
from flask import Flask, render_template
from db import query_db

app = Flask(__name__)

# ------------- Home page -------------
@app.route("/")
def index():
    questions = [
        (1, "Which product categories generate the highest total revenue?"),
        # add other qns
    ]
    return render_template("index.html", questions=questions)

# Q1: Which product categories generate the highest total revenue? 
@app.route("/q1")
def q1():
    sql = """
        SELECT
            c.categoryname,
            SUM(tl.totalspent) AS revenue
        FROM transactionline tl
        JOIN product p  ON tl.productid = p.productid
        JOIN category c ON p.categoryid = c.categoryid
        GROUP BY c.categoryname
        ORDER BY revenue DESC;
    """
    rows = query_db(sql)
    return render_template("q1.html", rows=rows)

# Add other qns here with their own SQL

if __name__ == "__main__":
    app.run(debug=True)
