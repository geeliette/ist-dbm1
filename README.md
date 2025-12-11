## 1. Requirements

Please install the following:

### System Requirements

- Python 3.10+
- PostgreSQL 14+
- pip (Python package manager)

### Python Libraries

The project uses:

```
Flask
psycopg2
```

Install them via:

```bash
pip install -r requirements.txt
```

---

## 3. Setting Up the PostgreSQL Database

### Step 1 — Open PostgreSQL (psql)

Open a terminal and run:

```bash
psql -U postgres
```

(If your username is different, replace `postgres`.)

---

### Step 2 — Create a new database

Inside `psql`:

```bash
\i sql/00_create_database.sql
```

Then switch into it:

```sql
\c dbm1_citta_liao;
```

---

### Step 3 — Create tables

Run the SQL file:

```bash
\i sql/01_create_raw_data.sql
```

This will create:

* Customer
* Category
* Product
* PaymentMethod
* Location
* Transaction
* TransactionLine

---

### Step 4 — Load the CSV data

Make sure your CSV file path is correct and accessible by PostgreSQL. Keep the retail_store_sales.csb outisde of the sql folder.

Then inside psql:

```bash
\i sql/02_load_raw_data.sql
```

Your database is now fully loaded.

---

## 4. Configuring the Database Connection (db.py)

Your `db.py` file should contain:

```python
import psycopg2
import psycopg2.extras

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="retail_store",
        user="postgres",
        password="YOUR_PASSWORD"
    )
    return conn

def query_db(sql, args=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql, args or ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
```

➡️ **Prof only needs to update `YOUR_PASSWORD`.**

---

## ▶️ 5. Running the Flask App

From the project root directory:

```bash
python app.py
```

If Flask runs successfully, you will see:

```
Running on http://127.0.0.1:5000/
```

Open this link in your browser.

---

## 🌐 6. Features of the Web App

The homepage displays **10 analytical questions**, such as:

1. Top revenue-generating categories
2. Best-selling products
3. Top customers by spending
4. Most-used payment methods
5. Highest revenue locations
6. Average discount rate
7. Top product by revenue within each category
8. Monthly revenue trend
9. Customers buying from most categories
10. Revenue by payment method and location

Each question has:

* A dedicated route (`/q1`, `/q2`, …)
* A SQL query in Python
* A Bootstrap table view in Jinja2

---

## 📦 7. Requirements File

Include this in `requirements.txt`:

```
Flask==3.0.0
psycopg2==2.9.9
```

---

## ❗ 8. Common Issues & Fixes

### **• Permission error when loading CSV**

If PostgreSQL cannot read your CSV file:

1. Move the CSV into the project folder (same folder as the SQL files)
2. Use a relative path in SQL:

   ```
   \copy raw_data FROM 'retail_store_sales.csv' WITH (FORMAT csv, HEADER true);
   ```

### **• psycopg2 errors**

Install:

```
pip install psycopg2-binary
```

---

## 🎉 9. Done!

Your professor should now be able to:

1. Create the database
2. Load the tables
3. Import the data
4. Run the Flask website locally

---

If you’d like, I can also generate:

✅ A zipped version of the whole project
✅ Screenshots for the README
✅ GIF demo for extra marks

Just tell me!
