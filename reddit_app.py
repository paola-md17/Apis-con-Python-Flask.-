from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('reddit.html')

@app.route('/api/reddit/posts')
def obtener_posts_reddit():
    subreddit = request.args.get('subreddit', 'python')
    filtro = request.args.get('filtro', 'hot')
    limit = request.args.get('limit', 10, type=int)
    
    url = f'https://www.reddit.com/r/{subreddit}/{filtro}.json'
    headers = {'User-Agent': 'Mozilla/5.0 (FlaskApp/1.0)'}     
    try:
        response = requests.get(url, headers=headers, params={'limit': limit})
        if response.status_code == 404:
            return jsonify({'error': 'Subreddit no encontrado'}), 404
            
        data = response.json()
        posts = []
        for post in data['data']['children']:
            p = post['data']
            fecha = datetime.fromtimestamp(p['created_utc']).strftime('%Y-%m-%d %H:%M')
            
            posts.append({
                'titulo': p['title'],
                'autor': p['author'],
                'puntos': p['score'],
                'comentarios': p['num_comments'],
                'url': f"https://reddit.com{p['permalink']}",
                'fecha': fecha,
                'thumbnail': p.get('thumbnail') if p.get('thumbnail') not in ['self', 'default', ''] else None,
                'selftext': p.get('selftext', '')[:200] + '...' if p.get('selftext') else ''
            })
        return jsonify({'subreddit': subreddit, 'posts': posts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)