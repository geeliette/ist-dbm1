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
        (2, "What are the top 5 best-selling products by quantity sold?"),
        (3, "Who are the top 10 customers by total spending?"),
        (4, "Which payment methods are used most frequently?"),
        (5, "Which locations generate the highest revenue?"),
        (6, "What is the average discount application rate across all transactions?"),
        (7, "What is the highest revenue-generating product in each category?"),
        (8, "How has monthly revenue trended over the past year?"),
        (9, "Who are the top 10 customers purchasing from the most diverse product categories?"),
        (10, "How does revenue vary by payment method and location?"),
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
    rows = query_db(sql)  # returns dict-like rows
    return render_template("q1.html", rows=rows)

# Add other qns here with their own SQL
@app.route("/q2")
def q2():
    sql = """
        SELECT
            p.ItemName,
        SUM(tl.Quantity) AS total_quantity_sold
        FROM TransactionLine tl
        JOIN Product p ON tl.ProductID = p.ProductID
        GROUP BY p.ItemName
        ORDER BY total_quantity_sold DESC
        LIMIT 5;
    """
    rows = query_db(sql)  # returns dict-like rows
    return render_template("q2.html", rows=rows)

@app.route("/q3")
def q3():
    sql = """
        SELECT
            t.CustomerID,
            SUM(tl.TotalSpent) AS total_spent
        FROM TransactionLine tl
        JOIN Transaction t ON tl.TransactionID = t.TransactionID
        GROUP BY t.CustomerID
        ORDER BY total_spent DESC
        LIMIT 10;
    """
    rows = query_db(sql)  # returns dict-like rows
    return render_template("q3.html", rows=rows)

@app.route("/q4")
def q4():
    sql = """
        SELECT
            pm.MethodName,
            COUNT(t.TransactionID) AS usage_count
        FROM Transaction t
        JOIN PaymentMethod pm ON t.PaymentMethodID = pm.PaymentMethodID
        GROUP BY pm.MethodName
        ORDER BY usage_count DESC;
    """
    rows = query_db(sql)  # returns dict-like rows
    return render_template("q4.html", rows=rows)

@app.route("/q5")
def q5():
    sql = """
        SELECT
            l.LocationName,
            SUM(tl.TotalSpent) AS revenue
        FROM TransactionLine tl
        JOIN Transaction t ON tl.TransactionID = t.TransactionID
        JOIN Location l ON t.LocationID = l.LocationID
        GROUP BY l.LocationName
        ORDER BY revenue DESC;
    """
    rows = query_db(sql)  # returns dict-like rows
    return render_template("q5.html", rows=rows)

@app.route("/q6")
def q6():
    sql = """
        SELECT
        AVG(CASE WHEN DiscountApplied THEN 1 ELSE 0 END) AS avg_discount_applied
        FROM Transaction;
    """
    rows = query_db(sql)  # returns dict-like rows
    return render_template("q6.html", rows=rows)

@app.route("/q7")
def q7():
    sql = """
        WITH ranked_products AS (
            SELECT
                c.CategoryName,
                p.ItemName,
                SUM(tl.TotalSpent) AS revenue,
                ROW_NUMBER() OVER (PARTITION BY c.CategoryName ORDER BY SUM(tl.TotalSpent) DESC) AS rn
            FROM TransactionLine tl
            JOIN Product p ON tl.ProductID = p.ProductID
            JOIN Category c ON p.CategoryID = c.CategoryID
            GROUP BY c.CategoryName, p.ItemName
        )
        SELECT CategoryName, ItemName, revenue
        FROM ranked_products
        WHERE rn = 1
        ORDER BY CategoryName;
    """
    rows = query_db(sql)  # returns dict-like rows
    return render_template("q7.html", rows=rows)

@app.route("/q8")
def q8():
    sql = """
        SELECT
            DATE_TRUNC('month', t.TransactionDate) AS month,
            SUM(tl.TotalSpent) AS revenue
        FROM TransactionLine tl
        JOIN Transaction t ON tl.TransactionID = t.TransactionID
        WHERE t.TransactionDate >= (CURRENT_DATE - INTERVAL '12 months')
        GROUP BY month
        ORDER BY month;
    """
    rows = query_db(sql)  # returns dict-like rows
    return render_template("q8.html", rows=rows)

@app.route("/q9")
def q9():
    sql = """
        SELECT
            t.CustomerID,
            COUNT(DISTINCT p.CategoryID) AS num_categories
        FROM TransactionLine tl
        JOIN Transaction t ON tl.TransactionID = t.TransactionID
        JOIN Product p ON tl.ProductID = p.ProductID
        GROUP BY t.CustomerID
        ORDER BY num_categories DESC
        LIMIT 10;
    """
    rows = query_db(sql)  # returns dict-like rows
    return render_template("q9.html", rows=rows)

@app.route("/q10")
def q10():
    sql = """
        SELECT
            pm.MethodName,
            l.LocationName,
            SUM(tl.TotalSpent) AS revenue
        FROM TransactionLine tl
        JOIN Transaction t ON tl.TransactionID = t.TransactionID
        JOIN PaymentMethod pm ON t.PaymentMethodID = pm.PaymentMethodID
        JOIN Location l ON t.LocationID = l.LocationID
        GROUP BY pm.MethodName, l.LocationName
        ORDER BY pm.MethodName, revenue DESC;
    """
    rows = query_db(sql)  # returns dict-like rows
    return render_template("q10.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
