"""
Inventory Management System Backend
A simple Flask API for managing phone and accessories inventory
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE = 'inventory.db'

def get_db():
    """Get database connection"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize the database with tables"""
    db = get_db()
    cursor = db.cursor()
    
    # Create phones table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create accessories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accessories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    db.commit()
    db.close()

def dict_from_row(row):
    """Convert sqlite3.Row to dictionary"""
    if row is None:
        return None
    return dict(row)

# Initialize database on startup
init_db()

# ============== HEALTH CHECK ==============
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint to wake up the server"""
    return jsonify({"status": "ok"}), 200

# ============== PHONES ENDPOINTS ==============
@app.route('/phones', methods=['POST'])
def add_phone():
    """Add a new phone to inventory"""
    data = request.get_json()
    
    # Validation
    if not data or not all(key in data for key in ['model', 'price', 'quantity']):
        return jsonify({"error": "Missing required fields: model, price, quantity"}), 400
    
    try:
        model = data['model'].strip()
        price = float(data['price'])
        quantity = int(data['quantity'])
        
        if not model:
            return jsonify({"error": "Model cannot be empty"}), 400
        if price < 0:
            return jsonify({"error": "Price cannot be negative"}), 400
        if quantity < 0:
            return jsonify({"error": "Quantity cannot be negative"}), 400
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO phones (model, price, quantity) VALUES (?, ?, ?)',
            (model, price, quantity)
        )
        db.commit()
        phone_id = cursor.lastrowid
        db.close()
        
        return jsonify({
            "id": phone_id,
            "model": model,
            "price": price,
            "quantity": quantity
        }), 201
    
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid data type: {str(e)}"}), 400

@app.route('/phones', methods=['GET'])
def get_phones():
    """Get all phones from inventory"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, model, price, quantity, created_at FROM phones ORDER BY created_at DESC')
    phones = [dict(row) for row in cursor.fetchall()]
    db.close()
    return jsonify(phones), 200

@app.route('/phones/<int:phone_id>', methods=['DELETE'])
def delete_phone(phone_id):
    """Delete a phone from inventory"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM phones WHERE id = ?', (phone_id,))
    db.commit()
    db.close()
    return jsonify({"message": "Phone deleted"}), 200

# ============== ACCESSORIES ENDPOINTS ==============
@app.route('/accessories', methods=['POST'])
def add_accessory():
    """Add a new accessory to inventory"""
    data = request.get_json()
    
    # Validation
    if not data or not all(key in data for key in ['name', 'price', 'quantity']):
        return jsonify({"error": "Missing required fields: name, price, quantity"}), 400
    
    try:
        name = data['name'].strip()
        price = float(data['price'])
        quantity = int(data['quantity'])
        
        if not name:
            return jsonify({"error": "Name cannot be empty"}), 400
        if price < 0:
            return jsonify({"error": "Price cannot be negative"}), 400
        if quantity < 0:
            return jsonify({"error": "Quantity cannot be negative"}), 400
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO accessories (name, price, quantity) VALUES (?, ?, ?)',
            (name, price, quantity)
        )
        db.commit()
        accessory_id = cursor.lastrowid
        db.close()
        
        return jsonify({
            "id": accessory_id,
            "name": name,
            "price": price,
            "quantity": quantity
        }), 201
    
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid data type: {str(e)}"}), 400

@app.route('/accessories', methods=['GET'])
def get_accessories():
    """Get all accessories from inventory"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, price, quantity, created_at FROM accessories ORDER BY created_at DESC')
    accessories = [dict(row) for row in cursor.fetchall()]
    db.close()
    return jsonify(accessories), 200

@app.route('/accessories/<int:accessory_id>', methods=['DELETE'])
def delete_accessory(accessory_id):
    """Delete an accessory from inventory"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM accessories WHERE id = ?', (accessory_id,))
    db.commit()
    db.close()
    return jsonify({"message": "Accessory deleted"}), 200

# ============== SUMMARY ENDPOINT ==============
@app.route('/summary', methods=['GET'])
def get_summary():
    """Get stock summary with total values in KES"""
    db = get_db()
    cursor = db.cursor()
    
    # Calculate phones total
    cursor.execute('SELECT SUM(price * quantity) as total FROM phones')
    phones_total = cursor.fetchone()['total'] or 0
    
    # Calculate accessories total
    cursor.execute('SELECT SUM(price * quantity) as total FROM accessories')
    accessories_total = cursor.fetchone()['total'] or 0
    
    db.close()
    
    grand_total = phones_total + accessories_total
    
    return jsonify({
        "phones_total": round(phones_total, 2),
        "accessories_total": round(accessories_total, 2),
        "grand_total": round(grand_total, 2)
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Use port 5000 for local development, PORT env var for production
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
