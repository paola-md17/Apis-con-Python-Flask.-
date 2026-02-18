"""
API REST para Gestión de Inventarios.
Base de Datos: SQLite (productos.db).
Puerto: 5004
"""
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    """Establece conexión con la base de datos local."""
    conn = sqlite3.connect('productos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Carga la interfaz principal."""
    return render_template('productos.html')

@app.route('/api/productos', methods=['GET'])
def listar_productos():
    """Obtiene productos filtrados opcionalmente por categoría."""
    categoria = request.args.get('categoria')
    conn = get_db_connection()
    if categoria:
        productos = conn.execute('SELECT * FROM productos WHERE categoria = ?', (categoria,)).fetchall()
    else:
        productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return jsonify([dict(p) for p in productos])

@app.route('/api/productos/stats')
def obtener_stats():
    """Calcula estadísticas para los indicadores del dashboard."""
    conn = get_db_connection()
    total = conn.execute('SELECT COUNT(*) FROM productos').fetchone()[0]
    promedio = conn.execute('SELECT AVG(precio) FROM productos').fetchone()[0] or 0
    stock = conn.execute('SELECT SUM(stock) FROM productos').fetchone()[0] or 0
    conn.close()
    return jsonify({
        "generales": {
            "total": total,
            "precio_promedio": promedio,
            "stock_total": stock
        }
    })

@app.route('/api/categorias')
def listar_categorias():
    """Extrae categorías únicas para el filtro del frontend."""
    conn = get_db_connection()
    cats = conn.execute('SELECT DISTINCT categoria FROM productos').fetchall()
    conn.close()
    return jsonify([c['categoria'] for c in cats if c['categoria']])

@app.route('/api/productos', methods=['POST'])
def crear_producto():
    """Registra un nuevo producto en la base de datos."""
    nuevo = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO productos (nombre, descripcion, precio, stock, categoria) VALUES (?, ?, ?, ?, ?)',
                 (nuevo['nombre'], nuevo['descripcion'], nuevo['precio'], nuevo['stock'], nuevo['categoria']))
    conn.commit()
    conn.close()
    return jsonify({"status": "creado"}), 201

# Rutas adicionales para PUT (editar) y DELETE (eliminar) requeridas por el HTML

if __name__ == '__main__':
    app.run(debug=True, port=5004)