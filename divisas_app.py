from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# CONFIGURACIÓN: Pega aquí tu llave
API_KEY = '62d2cfec311c6b45fe452d42' 
BASE_URL = 'https://v6.exchangerate-api.com/v6'

@app.route('/')
def index():
    return render_template('divisas.html')

# ESTA RUTA ES NECESARIA PARA QUE LOS SELECTORES NO ESTÉN VACÍOS
@app.route('/api/divisas/monedas')
def obtener_monedas():
    # Este catálogo permite que el JS de tu HTML llene los selects
    monedas = {
        "USD": {"nombre": "Dólar", "simbolo": "$"},
        "MXN": {"nombre": "Peso Mexicano", "simbolo": "$"},
        "EUR": {"nombre": "Euro", "simbolo": "€"},
        "GBP": {"nombre": "Libra", "simbolo": "£"}
    }
    return jsonify(monedas)

@app.route('/api/divisas/convertir')
def convertir():
    # Tu HTML envía estos nombres: monto, de, a
    monto = request.args.get('monto', type=float)
    de = request.args.get('de')
    a = request.args.get('a')

    if not monto or not de or not a:
        return jsonify({'error': 'Faltan datos'}), 400

    try:
        # Llamada a la API externa
        url = f"{BASE_URL}/{API_KEY}/pair/{de}/{a}/{monto}"
        response = requests.get(url)
        data = response.json()

        if data.get('result') == 'success':
            # Retornamos los nombres exactos que tu JS espera (monto_convertido, tasa_conversion)
            return jsonify({
                'monto_convertido': data['conversion_result'],
                'tasa_conversion': data['conversion_rate'],
                'ultima_actualizacion': data['time_last_update_utc']
            })
        return jsonify({'error': 'Error en API externa'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5007)