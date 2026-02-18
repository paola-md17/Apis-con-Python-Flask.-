from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
GITHUB_API = 'https://api.github.com'

@app.route('/')
def index():
    return render_template('github.html')

@app.route('/api/github/usuario/<username>')
def obtener_usuario_github(username):
    try:
        # 1. Obtener info del perfil
        user_response = requests.get(f'{GITHUB_API}/users/{username}')
        if user_response.status_code == 404:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        usuario = user_response.json()
        
        # 2. Obtener lista de repositorios (hasta 100)
        repos_response = requests.get(f'{GITHUB_API}/users/{username}/repos?per_page=100')
        repos = repos_response.json()
        
        # 3. Procesar estadísticas
        total_stars = sum(repo['stargazers_count'] for repo in repos)
        total_forks = sum(repo['forks_count'] for repo in repos)
        
        lenguajes = {}
        for repo in repos:
            lang = repo['language']
            if lang:
                lenguajes[lang] = lenguajes.get(lang, 0) + 1
        
        top_lenguajes = sorted(lenguajes.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return jsonify({
            'nombre': usuario.get('name') or username,
            'avatar': usuario['avatar_url'],
            'repositorios': usuario['public_repos'],
            'seguidores': usuario['followers'],
            'total_stars': total_stars,
            'total_forks': total_forks,
            'top_lenguajes': [{'lenguaje': l[0], 'repos': l[1]} for l in top_lenguajes],
            'repos_destacados': [
                {
                    'nombre': repo['name'],
                    'stars': repo['stargazers_count'],
                    'url': repo['html_url'],
                    'lenguaje': repo['language']
                }
                for repo in sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)[:5]
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Usamos el puerto 5003 para evitar conflictos
    app.run(debug=True, port=5003)