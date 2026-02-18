from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os

app = Flask(__name__)

# CONFIGURACIÓN DE FIREBASE
if not firebase_admin._apps:
    if os.path.exists('firebase-credentials.json'):
        cred = credentials.Certificate('firebase-credentials.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://TU-PROYECTO.firebaseio.com' # REEMPLAZA CON TU URL REAL
        })
    else:
        print("⚠️ Error: Falta firebase-credentials.json")

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/api/mensajes', methods=['GET', 'POST'])
def gestionar_mensajes():
    ref = db.reference('mensajes')
    if request.method == 'POST':
        data = request.json
        nuevo_mensaje = {
            'usuario': data['usuario'],
            'texto': data['texto'],
            'timestamp': datetime.now().isoformat(),
            'avatar': data.get('avatar', '👤')
        }
        ref.push(nuevo_mensaje)
        return jsonify({'status': 'enviado'}), 201
    
    # Obtener los últimos 50 mensajes
    mensajes = ref.order_by_child('timestamp').limit_to_last(50).get()
    return jsonify(list(mensajes.values()) if mensajes else [])

if __name__ == '__main__':
    app.run(debug=True, port=5005)