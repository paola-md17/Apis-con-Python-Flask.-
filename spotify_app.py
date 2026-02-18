from flask import Flask, render_template, request, jsonify, session
import requests
import base64
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'clave_para_sesion_spotify' # Necesario para guardar el token

# Credenciales de Spotify
CLIENT_ID = 'TU_CLIENT_ID_AQUI'
CLIENT_SECRET = 'TU_CLIENT_SECRET_AQUI'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_URL = 'https://api.spotify.com/v1'

def get_access_token():
    """Solicita un token de acceso usando Client Credentials Flow"""
    if 'access_token' in session and 'token_expiry' in session:
        if datetime.now() < datetime.fromisoformat(session['token_expiry']):
            return session['access_token']
    
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
    headers = {'Authorization': f'Basic {auth_base64}', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}
    
    try:
        response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
        token_data = response.json()
        session['access_token'] = token_data['access_token']
        session['token_expiry'] = (datetime.now() + timedelta(seconds=token_data['expires_in'] - 60)).isoformat()
        return token_data['access_token']
    except:
        return None

@app.route('/')
def index():
    return render_template('spotify.html')

@app.route('/api/spotify/buscar')
def buscar_spotify():
    query = request.args.get('q', '')
    tipo = request.args.get('tipo', 'track')
    token = get_access_token()
    
    if not token: return jsonify({'error': 'Error de autenticación'}), 500
    
    headers = {'Authorization': f'Bearer {token}'}
    params = {'q': query, 'type': tipo, 'limit': 20, 'market': 'MX'}
    
    response = requests.get(f'{SPOTIFY_API_URL}/search', headers=headers, params=params)
    data = response.json()
    
    # Procesamiento dinámico de resultados (Canciones, Artistas, etc.)
    resultados = []
    items = data.get(f'{tipo}s', {}).get('items', [])
    for item in items:
        res = {'id': item['id'], 'nombre': item['name'], 'spotify_url': item['external_urls']['spotify']}
        if tipo == 'track':
            res.update({'artista': item['artists'][0]['name'], 'imagen': item['album']['images'][0]['url'], 'preview': item['preview_url']})
        elif tipo == 'artist':
            res.update({'imagen': item['images'][0]['url'] if item['images'] else None, 'seguidores': item['followers']['total']})
        resultados.append(res)
    
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port=5009)