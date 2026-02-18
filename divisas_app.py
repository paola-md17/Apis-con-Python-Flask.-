from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Configuración de la API externa
API_KEY = 'TU_API_KEY_AQUI' # Coloca aquí tu clave real
BASE_URL = 'https://v6.exchangerate-api.com/v6'

@app.route('/')
def index():
    return render_template('divisas.html')

@app.route('/api/divisas/convertir')
def convertir():
    """Realiza la conversión entre dos monedas usando el endpoint /pair/ de la API"""
    monto = request.args.get('monto', type=float)
    de = request.args.get('de', 'USD').upper()
    a = request.args.get('a', 'MXN').upper()
    
    if not monto:
        return jsonify({'error': 'Monto requerido'}), 400
    
    try:
        # Llamada a la API para obtener la conversión exacta
        url = f'{BASE_URL}/{API_KEY}/pair/{de}/{a}/{monto}'
        response = requests.get(url)
        data = response.json()
        
        if data['result'] != 'success':
            return jsonify({'error': 'Error en la conversión de la API'}), 400
        
        return jsonify({
            'monto_original': monto,
            'monto_convertido': data['conversion_result'],
            'tasa_conversion': data['conversion_rate'],
            'ultima_actualizacion': data['time_last_update_utc']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5007)