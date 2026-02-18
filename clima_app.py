from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

WEATHER_API_KEY = 'c2b416028d532492a83e28d65c010a11'

@app.route('/')
def index():
    return render_template('clima.html')

@app.route('/api/clima')
def obtener_clima():
    # Usar coordenadas fijas (cambiar por tu ciudad)
    ciudades = {
        'mexico': {'lat': 19.4326, 'lon': -99.1332, 'nombre': 'Ciudad de México'},
        'monterrey': {'lat': 25.6866, 'lon': -100.3161, 'nombre': 'Monterrey'},
        'guadalajara': {'lat': 20.6597, 'lon': -103.3496, 'nombre': 'Guadalajara'}
    }
    
    ciudad = ciudades['monterrey']  # Cambiar según tu ubicación
    
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'lat': ciudad['lat'],
            'lon': ciudad['lon'],
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'es'
        }
        
        response = requests.get(url, params=params)
        clima = response.json()
        
        return jsonify({
            'ciudad': ciudad['nombre'],
            'pais': 'México',
            'temperatura': clima['main']['temp'],
            'descripcion': clima['weather'][0]['description'],
            'humedad': clima['main']['humidity'],
            'viento': clima['wind']['speed'],
            'icono': clima['weather'][0]['icon']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)