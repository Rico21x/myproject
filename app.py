from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'inventory.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory')
def inventory():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items WHERE name = ?', ('Tomato',)).fetchall()
    conn.close()
    items_list = [{'id': row['id'], 'name': row['name'], 'quantity': row['quantity'], 'image': row['image_url']} for row in items]
    return jsonify(items_list)

@app.route('/order', methods=['POST'])
def order():
    data = request.get_json()
    quantity = data['quantity']
    
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE name = ?', ('Tomato',)).fetchone()
    
    if item and item['quantity'] >= quantity:
        new_quantity = item['quantity'] - quantity
        conn.execute('UPDATE items SET quantity = ? WHERE id = ?', (new_quantity, item['id']))
        conn.commit()
        conn.close()
        response = {'success': True, 'message': f'Ordered {quantity} tomatoes. New quantity: {new_quantity}'}
    else:
        conn.close()
        response = {'success': False, 'message': 'Not enough stock or item does not exist.'}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
