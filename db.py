# db.py
import psycopg2
import psycopg2.extras

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="dbm1_citta_liao",
        user="postgres",
        password="postgres"
    )
    return conn

def query_db(sql, params=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
