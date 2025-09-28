#!/bin/bash

# Script de despliegue completo para CRUD App
echo "=== Iniciando despliegue de CRUD App ==="

# Variables
APP_DIR="/home/samyag/crud-app"
SERVICE_NAME="crud-app"

# Detener servicios existentes
echo "Deteniendo servicios existentes..."
sudo systemctl stop $SERVICE_NAME 2>/dev/null || echo "Servicio no estaba corriendo"
sudo pkill -f "gunicorn.*app:app" 2>/dev/null || echo "No hay procesos gunicorn corriendo"

# Crear directorio si no existe
echo "Creando directorio de aplicación..."
sudo mkdir -p $APP_DIR
sudo chown samyag:samyag $APP_DIR

# Navegar al directorio
cd $APP_DIR

# Instalar dependencias del sistema
echo "Instalando dependencias del sistema..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv postgresql-client nginx

# Crear entorno virtual
echo "Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias Python
echo "Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear directorios para logs
sudo mkdir -p /var/log/crud-app
sudo chown samyag:samyag /var/log/crud-app

# Crear las tablas de la base de datos
echo "Inicializando base de datos..."
python3 src/db.py

# Configurar servicio systemd
echo "Configurando servicio systemd..."
sudo cp crud-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable crud-app

# Configurar Nginx
echo "Configurando Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/crud-app
sudo ln -sf /etc/nginx/sites-available/crud-app /etc/nginx/sites-enabled/
sudo nginx -t

# Iniciar servicios
echo "Iniciando servicios..."
sudo systemctl start crud-app
sudo systemctl reload nginx

# Verificar estado
echo "=== Estado de servicios ==="
sudo systemctl status crud-app --no-pager
echo ""
echo "=== Despliegue completado ==="
echo "La aplicación debería estar disponible en: http://tu-servidor:81"
echo ""
echo "Para verificar logs:"
echo "  sudo journalctl -u crud-app -f"
echo "  tail -f /var/log/crud-app/error.log"