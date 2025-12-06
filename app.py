# app.py
from flask import Flask, render_template
from db import query_db

app = Flask(__name__)

# ------------- Home page -------------
@app.route("/")
def index():
    questions = [
        (1, "Which product categories generate the highest total revenue?"),
        (2, "Which customers spend the most, and how much have they spent?"),
        # add (3, "..."), ... up to (8, "...")
    ]
    return render_template("index.html", questions=questions)

# ------------- Q1: category revenue -------------
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

# ------------- Q2: top customers by spend -------------
@app.route("/q2")
def q2():
    sql = """
        SELECT
            t.customerid,
            SUM(tl.totalspent) AS total_spent,
            COUNT(DISTINCT t.transactionid) AS num_transactions
        FROM transaction t
        JOIN transactionline tl ON t.transactionid = tl.transactionid
        GROUP BY t.customerid
        ORDER BY total_spent DESC
        LIMIT 10;
    """
    rows = query_db(sql)
    return render_template("q2.html", rows=rows)

# Add /q3 ... /q8 here with their own SQL

if __name__ == "__main__":
    app.run(debug=True)
