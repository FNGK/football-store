import sqlite3

def get_connection():
    return sqlite3.connect("data/store.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            image_url TEXT,
            available INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            discount_percent INTEGER,
            expiry TEXT,
            usage_limit INTEGER
        )
    """)
    conn.commit()
    conn.close()