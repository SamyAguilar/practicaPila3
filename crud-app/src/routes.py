from flask import Blueprint, request, jsonify render_template
from .db import get_db

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/items', methods=['GET'])
def get_items():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM items;')
    items = cursor.fetchall()
    cursor.close()
    return jsonify(items)

@bp.route('/items', methods=['POST'])
def create_item():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;', (data['name'], data['description']))
    item_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return jsonify({'id': item_id}), 201

@bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE items SET name = %s, description = %s WHERE id = %s;', (data['name'], data['description'], item_id))
    db.commit()
    cursor.close()
    return jsonify({'id': item_id})

@bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM items WHERE id = %s;', (item_id,))
    db.commit()
    cursor.close()
    return jsonify({'result': True})