import os
from flask import Flask, render_template, request, jsonify
from database import get_db_connection, init_db

app = Flask(__name__)

# Automatically creates tables on startup if they don't exist yet
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    transactions = conn.execute('''
        SELECT t.transaction_id, t.type, t.amount, t.date, t.description, t.payment_method, c.category_name 
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.category_id
        ORDER BY t.date DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(tx) for tx in transactions])

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (user_id, category_id, type, amount, date, description, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (1, data.get('category_id'), data['type'], data['amount'], data['date'], data.get('description'), data.get('payment_method')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Transaction added successfully'}), 201

@app.route('/api/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM transactions WHERE transaction_id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Transaction deleted'})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return jsonify([dict(cat) for cat in categories])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)