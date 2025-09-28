from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from psycopg2.extras import RealDictCursor
from db import get_db
import psycopg2

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Página principal que muestra todos los items"""
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM items ORDER BY created_at DESC;')
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', records=items)
    except Exception as e:
        return f"Error: {str(e)}", 500

@main.route('/items', methods=['GET'])
def get_items():
    """API para obtener todos los items en JSON"""
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM items ORDER BY created_at DESC;')
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convertir a lista de diccionarios
        items_list = []
        for item in items:
            items_list.append({
                'id': item['id'],
                'name': item['name'],
                'description': item['description'],
                'created_at': item['created_at'].isoformat() if item['created_at'] else None
            })
        
        return jsonify(items_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/items', methods=['POST'])
def create_item():
    """API para crear un nuevo item"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;',
            (name, description)
        )
        item_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'id': item_id, 'message': 'Item created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/create', methods=['POST'])
def create_item_form():
    """Crear item desde formulario HTML"""
    try:
        name = request.form.get('name')  # Cambié de 'data' a 'name'
        description = request.form.get('description', '')  # Agregué descripción
        
        if not name:
            return "Error: El nombre es requerido", 400
            
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO items (name, description) VALUES (%s, %s);',
            (name, description)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('main.index'))
    except Exception as e:
        return f"Error: {str(e)}", 500

@main.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """API para actualizar un item"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE items SET name = %s, description = %s WHERE id = %s;',
            (name, description, item_id)
        )
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Item not found'}), 404
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'id': item_id, 'message': 'Item updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """API para eliminar un item"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = %s;', (item_id,))
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Item not found'}), 404
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'result': True, 'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400