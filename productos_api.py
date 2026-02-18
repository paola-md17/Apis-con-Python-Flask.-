from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'productos.db'

def init_db():
    """Crea la tabla si no existe"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            categoria TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    """Conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Permite acceder por nombre de columna
    return conn

@app.route('/')
def index():
    return render_template('productos.html')

# Endpoint para LEER productos
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(productos)

if __name__ == '__main__':
    init_db() # Inicializamos la DB al arrancar
    app.run(debug=True, port=5004)