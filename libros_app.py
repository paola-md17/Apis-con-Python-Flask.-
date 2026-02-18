from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Endpoint gratuito de Google Books
GOOGLE_BOOKS_API = 'https://www.googleapis.com/books/v1/volumes'

@app.route('/')
def index():
    return render_template('libros.html')

@app.route('/api/libros/buscar')
def buscar_libros():
    query = request.args.get('q', '')
    categoria = request.args.get('categoria', '')
    
    if not query:
        return jsonify({'error': 'Consulta requerida'}), 400
    
    # Construcción de la consulta técnica
    search_query = query
    if categoria:
        search_query += f'+subject:{categoria}'
    
    params = {
        'q': search_query,
        'maxResults': 20,
        'langRestrict': 'es' # Restringimos a libros en español
    }
    
    try:
        response = requests.get(GOOGLE_BOOKS_API, params=params)
        data = response.json()
        
        if 'items' not in data: return jsonify([])
        
        libros = []
        for item in data['items']:
            info = item.get('volumeInfo', {})
            libros.append({
                'id': item['id'],
                'titulo': info.get('title', 'Sin título'),
                'autores': info.get('authors', ['Anónimo']),
                'imagen': info.get('imageLinks', {}).get('thumbnail', ''),
                'paginas': info.get('pageCount', 0),
                'rating': info.get('averageRating', 0),
                'preview_link': info.get('previewLink', '')
            })
        return jsonify(libros)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5006)