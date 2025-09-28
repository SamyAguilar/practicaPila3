from flask import Flask
from routes import main as routes

app = Flask(__name__)

# Registrar las rutas
app.register_blueprint(routes)

if __name__ == '__main__':
    # Para desarrollo local en Windows
    app.run(host='0.0.0.0', port=81, debug=True)