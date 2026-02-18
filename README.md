# Apis-con-Python-Flask.-
Practica paginas web implementando apis con Python Flask. 

# 🚀 EJERCICIOS-APIS - Master Portfolio Flask 2026

Este repositorio contiene una colección robusta de **10 microservicios funcionales** desarrollados con Python y Flask. El proyecto demuestra el dominio en el consumo de APIs REST de terceros, persistencia de datos (SQL/NoSQL) y el desarrollo de interfaces dinámicas asíncronas utilizando JavaScript (Fetch API).

## 🚀 Características Principales
* **🌐 Ecosistema de APIs:** Integración con Spotify, TMDb, GitHub, Reddit y Google Books.
* **💾 Persistencia Dual:** Gestión de datos locales con **SQLite** y en la nube con **Firebase Realtime Database**.
* **⚡ Interfaces Asíncronas:** Uso extensivo de **Fetch API** para actualizaciones en tiempo real sin recarga de página.
* **📂 Arquitectura Modular:** Gestión de puertos independientes para cada aplicación (5000-5009).

## 🛠 Stack Tecnológico
| Categoría | Tecnología |
| :--- | :--- |
| **Lenguaje** | Python 3.12+ |
| **Framework** | Flask (Backend) |
| **Bases de Datos** | SQLite & Firebase |
| **UI** | HTML5 / CSS3 / JS (ES6+) |

## 📂 Estructura del Proyecto
```text
EJERCICIOS-APIS/
├── 📂 static/            # Recursos estáticos (CSS, JS e Imágenes)
│   └── 📂 img/           # Capturas de pantalla (.jpeg)
├── 📂 templates/         # Vistas dinámicas (Plantillas HTML)
├── 📂 venv/              # Entorno virtual de Python
├── 📄 productos.db       # Base de datos relacional local
└── 📄 requirements.txt   # Dependencias del proyecto

```

## 📸 Capturas de Pantalla

| Chat Realtime | Spotify Search | CRUD Productos |
|:---:|:---:|:---:|
| <img src="img/chat.jpeg" width="350"> | <img src="img/spotify.jpeg" width="350"> | <img src="img/productos.jpeg" width="350"> |

| Películas | Clima | Divisas |
|:---:|:---:|:---:|
| <img src="img/peliculas.jpeg" width="350"> | <img src="img/clima.jpeg" width="350"> | <img src="img/divisas.jpeg" width="350"> |

| GitHub | Lugares | Libros |
|:---:|:---:|:---:|
| <img src="img/github.jpeg" width="350"> | <img src="img/lugares.jpeg" width="350"> | <img src="img/libros.jpeg" width="350"> |

| Reddit | | |
|:---:|:---:|:---:|
| <img src="img/reddit.jpeg" width="350"> | 


## 📂 ANEXO: Código Fuente Completo
A continuación se adjunta el código fuente de los archivos principales de las APIS para su revisión directa en este documento.

<details>
<summary><b>Chat_app.py</b></summary>

```
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
```

<details>
<summary><b>Chat.html</b></summary>

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Realtime - Firebase</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .chat-container {
            width: 90%;
            max-width: 600px;
            height: 500px;
            background: white;
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .chat-header { background: #667eea; color: white; padding: 15px; text-align: center; }
        .messages-container { flex: 1; padding: 20px; overflow-y: auto; background: #f5f5f5; }
        .message { margin-bottom: 15px; display: flex; gap: 10px; }
        .message.own { flex-direction: row-reverse; }
        .message-bubble { 
            padding: 10px 15px; 
            border-radius: 15px; 
            background: white; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            max-width: 80%;
        }
        .message.own .message-bubble { background: #667eea; color: white; }
        .chat-input { padding: 15px; background: white; border-top: 1px solid #ddd; display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 20px; outline: none; }
        button { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer; font-weight: bold; }
        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center; z-index: 100; }
        .modal-content { background: white; padding: 30px; border-radius: 15px; text-align: center; }
        .avatar-option { font-size: 30px; cursor: pointer; padding: 5px; border: 2px solid transparent; border-radius: 5px; }
        .avatar-option.selected { border-color: #667eea; background: #f0f0f0; }
    </style>
</head>
<body>
    <div id="loginModal" class="modal">
        <div class="modal-content">
            <h2>🔥 Entrar al Chat</h2>
            <div style="margin: 20px 0; display: flex; justify-content: center; gap: 10px;">
                <span class="avatar-option selected" onclick="selAvatar(this, '👤')">👤</span>
                <span class="avatar-option" onclick="selAvatar(this, '🦊')">🦊</span>
                <span class="avatar-option" onclick="selAvatar(this, '🐱')">🐱</span>
                <span class="avatar-option" onclick="selAvatar(this, '🦁')">🦁</span>
            </div>
            <input type="text" id="nombreUsuario" placeholder="Tu nombre..." style="width: 100%; padding: 10px; margin-bottom: 20px;">
            <button onclick="iniciarChat()">Comenzar</button>
        </div>
    </div>

    <div class="chat-container" id="chatApp" style="display: none;">
        <div class="chat-header">
            <h3 id="userDisplay">Usuario</h3>
            <div id="status" style="font-size: 12px; opacity: 0.8;">Conectado</div>
        </div>
        <div class="messages-container" id="msgContainer"></div>
        <div class="chat-input">
            <input type="text" id="msgInput" placeholder="Escribe un mensaje..." onkeypress="if(event.key === 'Enter') enviar()">
            <button onclick="enviar()">Enviar</button>
        </div>
    </div>

    <script>
        let miUsuario = '';
        let miAvatar = '👤';

        function selAvatar(el, av) {
            miAvatar = av;
            document.querySelectorAll('.avatar-option').forEach(opt => opt.classList.remove('selected'));
            el.classList.add('selected');
        }

        function iniciarChat() {
            miUsuario = document.getElementById('nombreUsuario').value.trim();
            if (!miUsuario) return alert("Ingresa un nombre");
            document.getElementById('loginModal').style.display = 'none';
            document.getElementById('chatApp').style.display = 'flex';
            document.getElementById('userDisplay').textContent = `${miAvatar} ${miUsuario}`;
            
            cargarMensajes();
            setInterval(cargarMensajes, 2000); // Actualización constante cada 2 segundos
        }

        async function cargarMensajes() {
            try {
                const res = await fetch('/api/mensajes');
                const mensajes = await res.json();
                const container = document.getElementById('msgContainer');
                
                container.innerHTML = mensajes.map(m => `
                    <div class="message ${m.usuario === miUsuario ? 'own' : ''}">
                        <div style="font-size: 24px;">${m.avatar || '👤'}</div>
                        <div class="message-content">
                            <div style="font-size: 11px; color: #666;">${m.usuario}</div>
                            <div class="message-bubble">${m.texto}</div>
                        </div>
                    </div>
                `).join('');
                container.scrollTop = container.scrollHeight;
            } catch (e) { console.error("Error cargando mensajes", e); }
        }

        async function enviar() {
            const input = document.getElementById('msgInput');
            if (!input.value.trim()) return;

            await fetch('/api/mensajes', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    usuario: miUsuario,
                    texto: input.value,
                    avatar: miAvatar
                })
            });
            input.value = '';
            cargarMensajes();
        }
    </script>
</body>
</html>
```


<details>
<summary><b>Clima_app.py</b></summary>

```
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
```



<details>
<summary><b>Clima.html</b></summary>

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clima por Ubicación</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .clima-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            color: white;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: white;
            color: #667eea;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: scale(1.05);
        }
        
        button:active {
            transform: scale(0.98);
        }
        
        #resultado {
            margin-top: 30px;
            text-align: center;
        }
        
        .temperatura {
            font-size: 72px;
            font-weight: bold;
            margin: 20px 0;
        }
        
        .ciudad {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .descripcion {
            font-size: 20px;
            margin-bottom: 20px;
            text-transform: capitalize;
        }
        
        .detalles {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .detalle-item {
            text-align: center;
        }
        
        .detalle-valor {
            font-size: 24px;
            font-weight: bold;
        }
        
        .detalle-label {
            font-size: 14px;
            opacity: 0.8;
            margin-top: 5px;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: rgba(255, 0, 0, 0.2);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="clima-card">
        <h1>🌍 Clima en tu Ubicación</h1>
        <button onclick="obtenerClima()">Obtener Clima Actual</button>
        <div id="resultado"></div>
    </div>

    <script>
        async function obtenerClima() {
            const resultado = document.getElementById('resultado');
            
            // Mostrar loading
            resultado.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Obteniendo tu ubicación y clima...</p>
                </div>
            `;
            
            try {
                const response = await fetch('/api/clima');
                const data = await response.json();
                
                if (data.error) {
                    resultado.innerHTML = `
                        <div class="error">
                            <p>❌ Error: ${data.error}</p>
                        </div>
                    `;
                    return;
                }
                
                resultado.innerHTML = `
                    <div class="ciudad">${data.ciudad}, ${data.pais}</div>
                    <div class="temperatura">${Math.round(data.temperatura)}°C</div>
                    <div class="descripcion">${data.descripcion}</div>
                    <img src="https://openweathermap.org/img/wn/${data.icono}@2x.png" alt="Clima">
                    <div class="detalles">
                        <div class="detalle-item">
                            <div class="detalle-valor">💧 ${data.humedad}%</div>
                            <div class="detalle-label">Humedad</div>
                        </div>
                        <div class="detalle-item">
                            <div class="detalle-valor">💨 ${data.viento} m/s</div>
                            <div class="detalle-label">Viento</div>
                        </div>
                    </div>
                `;
            } catch (error) {
                resultado.innerHTML = `
                    <div class="error">
                        <p>❌ Error al obtener datos del clima</p>
                        <p style="font-size: 14px; margin-top: 10px;">${error.message}</p>
                    </div>
                `;
            }
        }
    </script>
</body>
</html>
```


<details>
<summary><b>Divisas_app.py</b></summary>

```
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
```
<details>
<summary><b>Divisas.html</b></summary>

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversor de Divisas</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .converter-container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
        }
        
        h1 { text-align: center; color: #11998e; margin-bottom: 10px; }
        .subtitle { text-align: center; color: #666; margin-bottom: 30px; font-size: 14px; }
        
        .input-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #333; }
        
        input[type="number"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 24px;
            text-align: center;
            font-weight: bold;
            color: #11998e;
        }
        
        select {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            background: white;
            cursor: pointer;
        }
        
        .swap-button {
            width: 100%;
            padding: 10px;
            background: #f0f0f0;
            border: none;
            border-radius: 10px;
            font-size: 24px;
            cursor: pointer;
            margin: 15px 0;
            transition: background 0.3s;
        }
        
        .swap-button:hover { background: #e0e0e0; }
        
        .convert-button {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .result {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 15px;
            text-align: center;
            display: none;
        }
        
        .result.show { display: block; }
        .result-amount { font-size: 32px; font-weight: bold; color: #11998e; }
        .result-rate { color: #666; font-size: 13px; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="converter-container">
        <h1>💰 Conversor de Divisas</h1>
        <p class="subtitle">Tasas de cambio en tiempo real</p>
        
        <div class="input-group">
            <label>Monto</label>
            <input type="number" id="monto" value="100" step="0.01">
        </div>
        
        <div class="input-group">
            <label>De</label>
            <select id="monedaDe"></select>
        </div>
        
        <button class="swap-button" onclick="intercambiarMonedas()">⇅</button>
        
        <div class="input-group">
            <label>A</label>
            <select id="monedaA"></select>
        </div>
        
        <button class="convert-button" onclick="convertir()">Convertir ahora</button>
        
        <div id="resultado" class="result"></div>
    </div>

    <script>
        let infoMonedas = {};
        
        // Cargar catálogo de monedas al iniciar
        window.onload = async () => {
            try {
                const response = await fetch('/api/divisas/monedas');
                infoMonedas = await response.json();
                
                const selectDe = document.getElementById('monedaDe');
                const selectA = document.getElementById('monedaA');
                
                Object.keys(infoMonedas).forEach(codigo => {
                    const info = infoMonedas[codigo];
                    const texto = `${info.bandera} ${codigo} - ${info.nombre}`;
                    
                    selectDe.options.add(new Option(texto, codigo));
                    selectA.options.add(new Option(texto, codigo));
                });
                
                selectDe.value = 'USD';
                selectA.value = 'MXN';
            } catch (e) { console.error("Error cargando monedas", e); }
        };

        function intercambiarMonedas() {
            const de = document.getElementById('monedaDe');
            const a = document.getElementById('monedaA');
            [de.value, a.value] = [a.value, de.value];
            convertir();
        }

        async function convertir() {
            const monto = document.getElementById('monto').value;
            const de = document.getElementById('monedaDe').value;
            const a = document.getElementById('monedaA').value;
            const resDiv = document.getElementById('resultado');

            if (!monto || monto <= 0) return;

            resDiv.innerHTML = "Convirtiendo...";
            resDiv.classList.add('show');

            try {
                const response = await fetch(`/api/divisas/convertir?monto=${monto}&de=${de}&a=${a}`);
                const data = await response.json();
                
                const simbolo = infoMonedas[a].simbolo;
                resDiv.innerHTML = `
                    <div class="result-amount">
                        ${simbolo} ${data.monto_convertido.toLocaleString('es-MX', {minimumFractionDigits: 2})} ${a}
                    </div>
                    <div class="result-rate">Tasa: 1 ${de} = ${data.tasa_conversion.toFixed(4)} ${a}</div>
                    <div style="font-size: 10px; color: #999; margin-top: 10px;">
                        Actualizado: ${new Date(data.ultima_actualizacion).toLocaleString()}
                    </div>
                `;
            } catch (e) { resDiv.innerHTML = "Error en la conversión"; }
        }

        // Eventos para conversión automática
        document.getElementById('monto').addEventListener('input', convertir);
        document.getElementById('monedaDe').addEventListener('change', convertir);
        document.getElementById('monedaA').addEventListener('change', convertir);
    </script>
</body>
</html>
```


<details>
<summary><b>Github_app.py</b></summary>

```
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
```

<details>
<summary><b>Github.html</b></summary>

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>GitHub Dashboard</title>
    <style>
        body { font-family: sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .card { background: #161b22; padding: 20px; border-radius: 6px; border: 1px solid #30363d; margin-bottom: 20px; }
        input { width: 70%; padding: 10px; background: #0d1117; color: white; border: 1px solid #30363d; border-radius: 6px; }
        button { padding: 10px 20px; background: #238636; color: white; border: none; border-radius: 6px; cursor: pointer; }
        .avatar { width: 80px; height: 80px; border-radius: 50%; border: 2px solid #58a6ff; }
        .stats { display: flex; gap: 20px; margin-top: 15px; }
        .stat-box { background: #0d1117; padding: 10px; border-radius: 6px; flex: 1; text-align: center; border: 1px solid #30363d; }
        .repo-card { background: #0d1117; padding: 10px; margin-top: 10px; border-radius: 6px; border: 1px solid #30363d; }
        a { color: #58a6ff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🐙 GitHub Dashboard</h1>
            <input type="text" id="username" placeholder="Usuario (ej: torvalds)">
            <button onclick="buscar()">Buscar</button>
        </div>
        <div id="res"></div>
    </div>

    <script>
        async function buscar() {
            const user = document.getElementById('username').value;
            const res = document.getElementById('res');
            res.innerHTML = 'Cargando...';
            
            try {
                const response = await fetch(`/api/github/usuario/${user}`);
                const d = await response.json();
                if (d.error) { res.innerHTML = `Error: ${d.error}`; return; }

                res.innerHTML = `
                    <div class="card">
                        <div style="display:flex; gap:20px; align-items:center;">
                            <img src="${d.avatar}" class="avatar">
                            <h2>${d.nombre}</h2>
                        </div>
                        <div class="stats">
                            <div class="stat-box"><b>${d.repositorios}</b><br>Repos</div>
                            <div class="stat-box"><b>${d.seguidores}</b><br>Seguidores</div>
                            <div class="stat-box"><b>⭐ ${d.total_stars}</b><br>Stars</div>
                        </div>
                    </div>
                    <div class="card">
                        <h3>🌟 Top Repositorios</h3>
                        ${d.repos_destacados.map(r => `
                            <div class="repo-card">
                                <a href="${r.url}" target="_blank"><b>${r.nombre}</b></a> - ⭐ ${r.stars} (${r.lenguaje})
                            </div>
                        `).join('')}
                    </div>
                `;
            } catch (e) { res.innerHTML = 'Error de conexión'; }
        }
    </script>
</body>
</html>
```

<details>
<summary><b>Libros_app.py</b></summary>

```
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
```


<details>
<summary><b>Libros.html</b></summary>

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Buscador de Libros</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; }
        header { background: linear-gradient(135deg, #6B46C1, #9333EA); color: white; padding: 40px; text-align: center; }
        .search-container { max-width: 800px; margin: -30px auto 30px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: flex; gap: 10px; }
        input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 12px 25px; background: #9333EA; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .libros-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; padding: 20px; max-width: 1200px; margin: 0 auto; }
        .card { background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: 0.3s; cursor: pointer; }
        .card:hover { transform: translateY(-5px); }
        .card img { width: 100%; height: 250px; object-fit: cover; }
        .card-info { padding: 15px; }
    </style>
</head>
<body>
    <header><h1>📚 Buscador de Libros</h1></header>
    <div class="search-container">
        <input type="text" id="busqueda" placeholder="Título, autor o tema...">
        <button onclick="buscar()">Buscar</button>
    </div>
    <div id="resultados" class="libros-grid"></div>

    <script>
        async function buscar() {
            const query = document.getElementById('busqueda').value;
            const resDiv = document.getElementById('resultados');
            resDiv.innerHTML = 'Buscando...';
            
            const response = await fetch(`/api/libros/buscar?q=${encodeURIComponent(query)}`);
            const libros = await response.json();
            
            resDiv.innerHTML = libros.map(l => `
                <div class="card" onclick="window.open('${l.preview_link}', '_blank')">
                    <img src="${l.imagen || 'https://via.placeholder.com/128x192?text=Sin+Portada'}" alt="${l.titulo}">
                    <div class="card-info">
                        <div style="font-weight:bold; font-size:14px; margin-bottom:5px;">${l.titulo}</div>
                        <div style="font-size:12px; color:#666;">${l.autores.join(', ')}</div>
                        <div style="margin-top:10px; font-size:12px;">⭐ ${l.rating || 'N/A'} | 📖 ${l.paginas} pág.</div>
                    </div>
                </div>
            `).join('');
        }
    </script>
</body>
</html>
```


<details>
<summary><b>Lugares_app.py</b></summary>

```
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('lugares.html')

@app.route('/api/lugares')
def buscar_lugares():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    tipo = request.args.get('tipo', 'restaurant')
    radio = request.args.get('radio', 1000, type=int)
    
    # Mapeo de tipos a queries de OSM
    tipos_osm = {
        'restaurant': 'amenity=restaurant',
        'hospital': 'amenity=hospital',
        'cafe': 'amenity=cafe',
        'farmacia': 'amenity=pharmacy',
        'tienda': 'shop=supermarket',
        'gasolinera': 'amenity=fuel',
        'banco': 'amenity=bank',
        'hotel': 'tourism=hotel'
    }
    
    query = tipos_osm.get(tipo, 'amenity=restaurant')
    
    # Consulta Overpass API
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node[{query}](around:{radio},{lat},{lon});
      way[{query}](around:{radio},{lat},{lon});
    );
    out center;
    """
    
    try:
        response = requests.get(overpass_url, params={'data': overpass_query}, timeout=30)
        data = response.json()
        
        lugares = []
        for elemento in data['elements'][:20]:  # Limitar a 20 resultados
            if 'center' in elemento:
                coords = elemento['center']
            elif 'lat' in elemento:
                coords = {'lat': elemento['lat'], 'lon': elemento['lon']}
            else:
                continue
            
            tags = elemento.get('tags', {})
            lugares.append({
                'nombre': tags.get('name', 'Sin nombre'),
                'direccion': tags.get('addr:street', '') + ' ' + tags.get('addr:housenumber', ''),
                'lat': coords['lat'],
                'lon': coords['lon'],
                'tipo': tags.get('amenity') or tags.get('shop') or tags.get('tourism', ''),
                'telefono': tags.get('phone', ''),
                'horario': tags.get('opening_hours', '')
            })
        
        return jsonify(lugares)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
```


<details>
<summary><b>Lugares.html</b></summary>

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buscador de Lugares Cercanos</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: linear-gradient(135deg, #2196F3, #1976D2);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .controles {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .control-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        
        select, input {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: #2196F3;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        button:hover {
            background: #1976D2;
        }
        
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        #resultados {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .lugar-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        
        .lugar-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .lugar-nombre {
            font-size: 20px;
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 10px;
        }
        
        .lugar-info {
            color: #666;
            margin: 5px 0;
            display: flex;
            align-items: center;
        }
        
        .lugar-info span {
            margin-right: 5px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            font-size: 18px;
            color: #666;
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        
        .no-resultados {
            text-align: center;
            padding: 40px;
            color: #666;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📍 Buscador de Lugares Cercanos</h1>
            <p>Encuentra restaurantes, hospitales, tiendas y más cerca de ti</p>
        </header>
        
        <div class="controles">
            <div class="control-group">
                <div>
                    <label for="tipo">Tipo de Lugar:</label>
                    <select id="tipo">
                        <option value="restaurant">🍽️ Restaurantes</option>
                        <option value="cafe">☕ Cafeterías</option>
                        <option value="hospital">🏥 Hospitales</option>
                        <option value="farmacia">💊 Farmacias</option>
                        <option value="tienda">🛒 Supermercados</option>
                        <option value="gasolinera">⛽ Gasolineras</option>
                        <option value="banco">🏦 Bancos</option>
                        <option value="hotel">🏨 Hoteles</option>
                    </select>
                </div>
                
                <div>
                    <label for="radio">Radio de búsqueda:</label>
                    <select id="radio">
                        <option value="500">500 metros</option>
                        <option value="1000" selected>1 kilómetro</option>
                        <option value="2000">2 kilómetros</option>
                        <option value="5000">5 kilómetros</option>
                    </select>
                </div>
            </div>
            
            <button onclick="buscarLugares()" id="btnBuscar">Buscar Lugares Cercanos</button>
        </div>
        
        <div id="resultados"></div>
    </div>

    <script>
        let miUbicacion = null;
        
        // Obtener ubicación al cargar la página
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    miUbicacion = {
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    };
                    console.log('Ubicación obtenida:', miUbicacion);
                },
                error => {
                    console.error('Error al obtener ubicación:', error);
                    // Ubicación por defecto (ejemplo: Ciudad de México)
                    miUbicacion = { lat: 19.4326, lon: -99.1332 };
                }
            );
        }
        
        async function buscarLugares() {
            const resultados = document.getElementById('resultados');
            const btnBuscar = document.getElementById('btnBuscar');
            
            if (!miUbicacion) {
                alert('No se pudo obtener tu ubicación. Por favor, permite el acceso a la ubicación.');
                return;
            }
            
            const tipo = document.getElementById('tipo').value;
            const radio = document.getElementById('radio').value;
            
            btnBuscar.disabled = true;
            resultados.innerHTML = '<div class="loading">🔍 Buscando lugares cercanos...</div>';
            
            try {
                const url = `/api/lugares?lat=${miUbicacion.lat}&lon=${miUbicacion.lon}&tipo=${tipo}&radio=${radio}`;
                const response = await fetch(url);
                const data = await response.json();
                
                if (data.error) {
                    resultados.innerHTML = `<div class="error">❌ Error: ${data.error}</div>`;
                    return;
                }
                
                if (data.length === 0) {
                    resultados.innerHTML = `
                        <div class="no-resultados">
                            😔 No se encontraron lugares de este tipo en el radio especificado.
                            <br>Intenta ampliar el radio de búsqueda.
                        </div>
                    `;
                    return;
                }
                
                resultados.innerHTML = data.map(lugar => `
                    <div class="lugar-card">
                        <div class="lugar-nombre">${lugar.nombre}</div>
                        ${lugar.direccion ? `<div class="lugar-info"><span>📍</span>${lugar.direccion}</div>` : ''}
                        ${lugar.telefono ? `<div class="lugar-info"><span>📞</span>${lugar.telefono}</div>` : ''}
                        ${lugar.horario ? `<div class="lugar-info"><span>🕐</span>${lugar.horario}</div>` : ''}
                        <div class="lugar-info">
                            <span>🗺️</span>
                            <a href="https://www.google.com/maps?q=${lugar.lat},${lugar.lon}" target="_blank">
                                Ver en Google Maps
                            </a>
                        </div>
                    </div>
                `).join('');
                
            } catch (error) {
                resultados.innerHTML = `<div class="error">❌ Error al buscar lugares: ${error.message}</div>`;
            } finally {
                btnBuscar.disabled = false;
            }
        }
    </script>
</body>
</html>
```


<details>
<summary><b>Peliculas_app.py</b></summary>

```
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
```


<details>
<summary><b>Peliculas.html</b></summary>

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Buscador de Películas</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #0b0e11; color: white; padding: 20px; }
        header { text-align: center; padding: 40px 0; background: linear-gradient(to bottom, #1a1f24, #0b0e11); }
        .search-container { max-width: 600px; margin: 20px auto; display: flex; gap: 10px; }
        input { flex: 1; padding: 12px; border-radius: 25px; border: none; background: #252d35; color: white; outline: none; }
        button { padding: 12px 25px; border-radius: 25px; border: none; background: #e50914; color: white; font-weight: bold; cursor: pointer; }
        .movie-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 25px; max-width: 1200px; margin: 40px auto; }
        .movie-card { background: #1a1f24; border-radius: 10px; overflow: hidden; transition: 0.3s; }
        .movie-card:hover { transform: scale(1.05); box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
        .movie-card img { width: 100%; height: 300px; object-fit: cover; }
        .movie-info { padding: 15px; }
        .rating { color: #f5c518; font-weight: bold; font-size: 14px; }
    </style>
</head>
<body>
    <header>
        <h1>🎬 MovieFinder</h1>
        <p>Explora el mundo del cine con TMDB API</p>
        <div class="search-container">
            <input type="text" id="query" placeholder="Escribe el nombre de una película...">
            <button onclick="buscar()">Buscar</button>
        </div>
    </header>
    <div id="resultados" class="movie-grid"></div>

    <script>
        async function buscar() {
            const q = document.getElementById('query').value;
            const res = document.getElementById('resultados');
            if(!q) return;

            res.innerHTML = "Buscando...";
            const response = await fetch(`/api/peliculas/buscar?q=${encodeURIComponent(q)}`);
            const data = await response.json();

            res.innerHTML = data.map(p => `
                <div class="movie-card">
                    <img src="${p.poster || 'https://via.placeholder.com/500x750?text=No+Poster'}" alt="${p.titulo}">
                    <div class="movie-info">
                        <div style="font-weight:bold; margin-bottom:5px;">${p.titulo}</div>
                        <div class="rating">⭐ ${p.voto}</div>
                        <div style="font-size:12px; color:#aaa; margin-top:5px;">${p.fecha}</div>
                    </div>
                </div>
            `).join('');
        }
    </script>
</body>
</html>
```


<details>
<summary><b>Productos_api.py</b></summary>

```
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
```


<details>
<summary><b>Productos.html</b></summary>

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API REST - Gestión de Productos</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .stat-value { font-size: 32px; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; margin-top: 5px; }
        .controls { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold; margin-right: 10px; }
        .btn-primary { background: #667eea; color: white; }
        .btn-success { background: #10b981; color: white; }
        .btn-danger { background: #ef4444; color: white; }
        table { width: 100%; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-collapse: collapse; }
        th, td { padding: 15px; text-align: left; }
        th { background: #667eea; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; }
        .modal-content { background: white; max-width: 500px; margin: 100px auto; padding: 30px; border-radius: 10px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>💾 API REST - Gestión de Productos</h1>
            <p>Sistema CRUD completo con SQLite</p>
        </header>
        
        <div class="stats-grid" id="stats"></div>
        
        <div class="controls">
            <button class="btn btn-success" onclick="abrirModalNuevo()">➕ Nuevo Producto</button>
            <button class="btn btn-primary" onclick="cargarProductos()">🔄 Recargar</button>
            <select id="filtroCategoria" onchange="cargarProductos()" style="padding: 10px; border-radius: 5px;">
                <option value="">Todas las categorías</option>
            </select>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Precio</th>
                    <th>Stock</th>
                    <th>Categoría</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody id="productosTable">
                <tr><td colspan="6" style="text-align: center;">Cargando...</td></tr>
            </tbody>
        </table>
    </div>
    
    <div id="modal" class="modal">
        <div class="modal-content">
            <h2 id="modalTitulo">Nuevo Producto</h2>
            <form id="productoForm">
                <input type="hidden" id="productoId">
                <div class="form-group"><label>Nombre *</label><input type="text" id="nombre" required></div>
                <div class="form-group"><label>Descripción</label><textarea id="descripcion"></textarea></div>
                <div class="form-group"><label>Precio *</label><input type="number" id="precio" step="0.01" required></div>
                <div class="form-group"><label>Stock</label><input type="number" id="stock" value="0"></div>
                <div class="form-group"><label>Categoría</label><input type="text" id="categoria"></div>
                <div style="margin-top: 20px;">
                    <button type="submit" class="btn btn-success">Guardar</button>
                    <button type="button" class="btn" onclick="cerrarModal()">Cancelar</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // Funciones principales
        window.onload = () => { cargarEstadisticas(); cargarCategorias(); cargarProductos(); };

        async function cargarEstadisticas() {
            const response = await fetch('/api/productos/stats');
            const data = await response.json();
            document.getElementById('stats').innerHTML = `
                <div class="stat-card"><div class="stat-value">${data.generales.total}</div><div class="stat-label">Total Productos</div></div>
                <div class="stat-card"><div class="stat-value">$${data.generales.precio_promedio.toFixed(2)}</div><div class="stat-label">Precio Promedio</div></div>
                <div class="stat-card"><div class="stat-value">${data.generales.stock_total}</div><div class="stat-label">Stock Total</div></div>
            `;
        }

        async function cargarProductos() {
            const cat = document.getElementById('filtroCategoria').value;
            const url = cat ? `/api/productos?categoria=${cat}` : '/api/productos';
            const response = await fetch(url);
            const productos = await response.json();
            document.getElementById('productosTable').innerHTML = productos.map(p => `
                <tr>
                    <td>${p.id}</td>
                    <td><b>${p.nombre}</b></td>
                    <td>$${p.precio.toFixed(2)}</td>
                    <td>${p.stock}</td>
                    <td><span style="background:#667eea; color:white; padding:3px 8px; border-radius:10px;">${p.categoria}</span></td>
                    <td>
                        <button class="btn btn-primary" onclick="editarProducto(${p.id})">✏️</button>
                        <button class="btn btn-danger" onclick="eliminarProducto(${p.id})">🗑️</button>
                    </td>
                </tr>
            `).join('');
            cargarEstadisticas();
        }

        function abrirModalNuevo() { 
            document.getElementById('productoForm').reset(); 
            document.getElementById('productoId').value = ''; 
            document.getElementById('modal').style.display = 'block'; 
        }

        function cerrarModal() { document.getElementById('modal').style.display = 'none'; }

        document.getElementById('productoForm').onsubmit = async (e) => {
            e.preventDefault();
            const id = document.getElementById('productoId').value;
            const data = {
                nombre: document.getElementById('nombre').value,
                descripcion: document.getElementById('descripcion').value,
                precio: parseFloat(document.getElementById('precio').value),
                stock: parseInt(document.getElementById('stock').value),
                categoria: document.getElementById('categoria').value
            };
            const method = id ? 'PUT' : 'POST';
            const url = id ? `/api/productos/${id}` : '/api/productos';
            
            await fetch(url, {
                method: method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            cerrarModal(); cargarProductos();
        };

        async function eliminarProducto(id) {
            if (confirm('¿Eliminar producto?')) {
                await fetch(`/api/productos/${id}`, { method: 'DELETE' });
                cargarProductos();
            }
        }

        async function editarProducto(id) {
            const response = await fetch(`/api/productos/${id}`);
            const p = await response.json();
            document.getElementById('productoId').value = p.id;
            document.getElementById('nombre').value = p.nombre;
            document.getElementById('descripcion').value = p.descripcion;
            document.getElementById('precio').value = p.precio;
            document.getElementById('stock').value = p.stock;
            document.getElementById('categoria').value = p.categoria;
            document.getElementById('modal').style.display = 'block';
        }
        
        async function cargarCategorias() {
            const response = await fetch('/api/categorias');
            const cats = await response.json();
            const select = document.getElementById('filtroCategoria');
            cats.forEach(c => {
                const opt = document.createElement('option');
                opt.value = opt.textContent = c;
                select.appendChild(opt);
            });
        }
    </script>
</body>
</html>
```


<details>
<summary><b>Reddit_app.py</b></summary>

```
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
```


<details>
<summary><b>Reddit.html</b></summary>

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Analizador de Reddit</title>
    <style>
        body { font-family: Arial, sans-serif; background: #DAE0E6; padding: 20px; }
        header { background: #FF4500; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .controles { background: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        input, select, button { padding: 8px; margin-right: 5px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #FF4500; color: white; border: none; cursor: pointer; font-weight: bold; }
        .post { background: white; padding: 15px; margin-bottom: 10px; border-radius: 5px; border-left: 4px solid #FF4500; }
        .post-titulo { font-size: 18px; font-weight: bold; color: #1c1c1c; text-decoration: none; }
        .post-meta { font-size: 12px; color: #7c7c7c; margin-top: 5px; }
    </style>
</head>
<body>
    <header>
        <h1>🤖 Analizador de Reddit</h1>
    </header>
    
    <div class="controles">
        <input type="text" id="subreddit" placeholder="Subreddit (ej: python)" value="python">
        <select id="filtro">
            <option value="hot">Hot</option>
            <option value="new">New</option>
            <option value="top">Top</option>
        </select>
        <button onclick="cargarPosts()">Cargar Posts</button>
    </div>
    
    <div id="resultados"></div>

    <script>
        async function cargarPosts() {
            const resDiv = document.getElementById('resultados');
            const sub = document.getElementById('subreddit').value;
            const fil = document.getElementById('filtro').value;
            
            resDiv.innerHTML = 'Cargando...';
            
            try {
                const response = await fetch(`/api/reddit/posts?subreddit=${sub}&filtro=${fil}`);
                const data = await response.json();
                
                if (data.error) { resDiv.innerHTML = `Error: ${data.error}`; return; }
                
                resDiv.innerHTML = data.posts.map(p => `
                    <div class="post">
                        <a href="${p.url}" target="_blank" class="post-titulo">${p.titulo}</a>
                        <div class="post-meta">
                            u/${p.autor} | ⬆️ ${p.puntos} | 💬 ${p.comentarios} | ${p.fecha}
                        </div>
                    </div>
                `).join('');
            } catch (e) { resDiv.innerHTML = 'Error de conexión'; }
        }
        window.onload = cargarPosts;
    </script>
</body>
</html>
```


<details>
<summary><b>Spotify_app.py</b></summary>

```


```


<details>
<summary><b>Spotify.html</b></summary>

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buscador de Música - Spotify</title>
    <style>
        /* Estilos Base */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1DB954 0%, #191414 100%);
            min-height: 100vh;
            color: white;
            padding-bottom: 100px; /* Espacio para el reproductor */
        }
        
        header {
            background: rgba(0, 0, 0, 0.9);
            padding: 20px;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid #282828;
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        h1 { color: #1DB954; font-size: 1.8em; }

        /* Controles de Búsqueda */
        .search-box {
            display: flex;
            gap: 10px;
            flex: 1;
            max-width: 600px;
        }

        input[type="text"], select {
            padding: 12px 20px;
            border: none;
            border-radius: 25px;
            background: #282828;
            color: white;
            outline: none;
        }

        input[type="text"] { flex: 1; }

        button {
            padding: 12px 25px;
            background: #1DB954;
            color: white;
            border: none;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover { background: #1ed760; transform: scale(1.05); }

        /* Cuadrícula de Resultados */
        .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 25px;
        }

        .card {
            background: rgba(40, 40, 40, 0.6);
            padding: 15px;
            border-radius: 10px;
            transition: 0.3s;
            cursor: pointer;
            position: relative;
        }

        .card:hover { background: rgba(40, 40, 40, 1); transform: translateY(-5px); }

        .card img {
            width: 100%;
            aspect-ratio: 1;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }

        .track-name { font-weight: bold; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .artist-name { color: #b3b3b3; font-size: 14px; }

        /* Reproductor Flotante */
        .player-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #181818;
            padding: 15px 30px;
            display: none;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid #282828;
            z-index: 1000;
        }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>🎵 Spotify App</h1>
            <div class="search-box">
                <input type="text" id="query" placeholder="¿Qué quieres escuchar?">
                <select id="tipo">
                    <option value="track">Canciones</option>
                    <option value="artist">Artistas</option>
                    <option value="album">Álbumes</option>
                </select>
                <button onclick="buscar()">Buscar</button>
            </div>
        </div>
    </header>

    <div class="container">
        <div id="resultados" class="grid"></div>
    </div>

    <div id="player" class="player-bar">
        <div style="display: flex; align-items: center; gap: 15px; width: 300px;">
            <img id="p-img" src="" style="width: 50px; height: 50px; border-radius: 4px;">
            <div style="overflow: hidden;">
                <div id="p-name" style="font-weight: bold; font-size: 14px; white-space: nowrap;"></div>
                <div id="p-artist" style="color: #b3b3b3; font-size: 12px;"></div>
            </div>
        </div>
        <audio id="audio-ctrl" controls style="width: 100%; max-width: 500px;"></audio>
        <div style="width: 300px;"></div>
    </div>

    <script>
        async function buscar() {
            const q = document.getElementById('query').value;
            const t = document.getElementById('tipo').value;
            const resDiv = document.getElementById('resultados');
            if(!q) return;

            resDiv.innerHTML = '<div style="grid-column: 1/-1; text-align: center;">Buscando en Spotify...</div>';
            
            try {
                const response = await fetch(`/api/spotify/buscar?q=${encodeURIComponent(q)}&tipo=${t}`);
                const data = await response.json();
                
                resDiv.innerHTML = data.map(item => `
                    <div class="card" onclick="${t === 'track' ? `play('${item.preview}', '${item.nombre.replace(/'/g, "\\'")}', '${item.artista.replace(/'/g, "\\'")}', '${item.imagen}')` : `window.open('${item.spotify_url}', '_blank')`}">
                        <img src="${item.imagen || 'https://via.placeholder.com/300?text=No+Image'}" alt="${item.nombre}">
                        <div class="track-name">${item.nombre}</div>
                        <div class="artist-name">${item.artista || item.seguidores + ' seguidores'}</div>
                    </div>
                `).join('');
            } catch (e) { resDiv.innerHTML = "Error al conectar con el servidor."; }
        }

        function play(url, name, artist, img) {
            if(!url) return alert("Spotify no ofrece fragmento para esta canción.");
            
            document.getElementById('player').style.display = 'flex';
            document.getElementById('p-img').src = img;
            document.getElementById('p-name').textContent = name;
            document.getElementById('p-artist').textContent = artist;
            
            const audio = document.getElementById('audio-ctrl');
            audio.src = url;
            audio.play();
        }
    </script>
</body>
</html>
```



<details>
<summary><b>Requirements.txt</b></summary>

```
blinker==1.9.0
certifi==2026.1.4
charset-normalizer==3.4.4
click==8.3.1
colorama==0.4.6
Flask==3.1.2
idna==3.11
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
requests==2.32.5
urllib3==2.6.3
Werkzeug==3.1.5
```




