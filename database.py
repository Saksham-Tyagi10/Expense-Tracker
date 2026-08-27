import sqlite3
import os

# Check if running in Vercel or cloud environment
DB_PATH = '/tmp/expense_tracker.db' if os.environ.get('VERCEL') else 'expense_tracker.db'

def get_db_connection():
    conn = sqlite3.connect('expense_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL,
            icon_url TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER,
            type TEXT CHECK(type IN ('INCOME', 'EXPENSE')) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            date DATE NOT NULL,
            description TEXT,
            payment_method TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
    ''')

    default_categories = ['Food', 'Rent', 'Salary', 'Entertainment', 'Utilities', 'Travel']
    for cat in default_categories:
        cursor.execute("INSERT OR IGNORE INTO categories (category_id, category_name) VALUES ((SELECT category_id FROM categories WHERE category_name = ?), ?)", (cat, cat))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()