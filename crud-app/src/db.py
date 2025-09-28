import psycopg2
from psycopg2.extras import RealDictCursor

# Cambia 'localhost' por la IP de tu servidor PostgreSQL
DATABASE_IP = '192.168.0.106'  # Cambia esto por la IP de tu servidor
DATABASE_URL = f"postgresql://samyag:contra123456@{DATABASE_IP}:5432/pila3"

def get_db():
    """Obtiene una conexión a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        raise

def init_db():
    """Crea las tablas necesarias si no existen"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Crear tabla items si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Base de datos inicializada correctamente")

if __name__ == '__main__':
    init_db()