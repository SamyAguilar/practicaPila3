from flask import Flask
from routes import main as routes

app = Flask(__name__)

# Registrar las rutas
app.register_blueprint(routes)

if __name__ == '__main__':
    # Para desarrollo local
    app.run(host='0.0.0.0', port=5000, debug=True)
else:
    # Para producción con Gunicorn
    # Inicializar la base de datos al importar
    from db import init_db
    try:
        init_db()
        print("Aplicación iniciada correctamente con Gunicorn")
    except Exception as e:
        print(f"Warning: No se pudo inicializar la base de datos: {e}")