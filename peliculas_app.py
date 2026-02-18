from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Configuración TMDB
TMDB_API_KEY = '75a59fd25cfc85a6ea4cbd716559a7e8'
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE = 'https://image.tmdb.org/t/p/w500'

@app.route('/')
def index():
    return render_template('peliculas.html')

@app.route('/api/peliculas/buscar')
def buscar_peliculas():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Consulta vacía'}), 400
    
    url = f'{BASE_URL}/search/movie'
    params = {'api_key': TMDB_API_KEY, 'query': query, 'language': 'es-MX'}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        resultados = []
        for p in data.get('results', []):
            resultados.append({
                'id': p['id'],
                'titulo': p['title'],
                'sinopsis': p.get('overview', '')[:200] + '...',
                'poster': f"{IMAGE_BASE}{p['poster_path']}" if p.get('poster_path') else None,
                'voto': p.get('vote_average', 0),
                'fecha': p.get('release_date', 'N/A')
            })
        return jsonify(resultados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5008)