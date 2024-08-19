from flask import Flask, jsonify, request
# Importa Flask para crear la aplicación, jsonify para devolver respuestas JSON, y request para manejar solicitudes HTTP.

from flask_cors import CORS
# Importa CORS para habilitar Cross-Origin Resource Sharing, lo que permite que la API sea accesible desde otros dominios.

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# Importa JWTManager para manejar JWT en la aplicación, create_access_token para crear tokens, jwt_required para proteger rutas, y get_jwt_identity para obtener la identidad del token.

from dotenv import load_dotenv
# Importa load_dotenv para cargar variables de entorno desde un archivo .env.

import os
# Importa os para acceder a las variables de entorno del sistema.

import requests
# Importa requests para realizar solicitudes HTTP a otras API.

import random
# Importa random para seleccionar elementos aleatorios de una lista.

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
# Carga las variables de entorno definidas en un archivo .env en el entorno de ejecución.

app = Flask(__name__)
# Crea una instancia de la aplicación Flask.

# Configuración de la clave secreta para JWT desde una variable de entorno
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
# Configura la clave secreta para JWT, obteniéndola de las variables de entorno.

# Verificar que la clave secreta esté configurada
if not app.config['JWT_SECRET_KEY']:
    raise ValueError("JWT_SECRET_KEY no está configurada. Establezca la variable de entorno antes de iniciar la aplicación.")
# Verifica que la clave secreta esté configurada; si no lo está, lanza un error.

# Inicializar JWTManager
jwt = JWTManager(app)
# Inicializa JWTManager con la aplicación Flask para manejar JWT.

# Habilitar CORS para toda la aplicación
CORS(app)
# Habilita CORS en toda la aplicación Flask, permitiendo que la API sea accesible desde cualquier origen.

# Define un endpoint /login para la autenticación y obtención de token que acepta solicitudes POST para autenticar usuarios y devolver un token JWT.
@app.route('/login', methods=['POST'])
def login():

    
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Obtiene el nombre de usuario y la contraseña del cuerpo de la solicitud JSON.

# Verifica si el usuario y la contraseña son correctos. Si no coinciden, devuelve un error 401.
    if username != 'admin' or password != 'password':
        return jsonify({"msg": "Bad username or password"}), 401
    

# Si las credenciales son correctas, se crea un token de acceso
    access_token = create_access_token(identity=username)
    

    return jsonify(access_token=access_token)
# Devuelve el token de acceso en una respuesta JSON.

# Define un endpoint /pokemon/tipo/<nombre> que requiere autenticación JWT y devuelve el tipo de un Pokémon según su nombre.
@app.route('/pokemon/tipo/<nombre>', methods=['GET'])
@jwt_required()  # Requiere autenticación JWT
def obtener_tipo(nombre):

    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
        response = requests.get(url)
        response.raise_for_status()  # Se genera una excepción para códigos de estado 4xx/5xx
# Construye la URL para consultar la API de PokeAPI con el nombre del Pokémon y realiza una solicitud GET. Si la respuesta tiene un código de error, lanza una excepción.

        data = response.json()
        # Convierte la respuesta en un objeto JSON.

        tipos = [tipo['type']['name'] for tipo in data['types']]
        # Extrae los tipos del Pokémon desde la respuesta JSON.

        if tipos:
            return jsonify({'nombre': nombre, 'tipos': tipos})
        else:
            return jsonify({'error': 'No se encontraron tipos para el Pokémon especificado'}), 404
        # Si se encontraron tipos, los devuelve en una respuesta JSON. Si no, devuelve un error 404.

    except requests.exceptions.HTTPError as e:
        return jsonify({'error': f'Error al conectar con PokeAPI: {e.response.status_code}', 'details': str(e)}), e.response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error al conectar con PokeAPI', 'details': str(e)}), 500
    except (KeyError, TypeError):
        return jsonify({'error': 'Datos inesperados recibidos de PokeAPI'}), 500
    # Maneja errores que pueden ocurrir durante la solicitud HTTP o al procesar la respuesta JSON.


@app.route('/pokemon/aleatorio/<tipo>', methods=['GET'])
@jwt_required()  # Requiere autenticación JWT
def pokemon_aleatorio(tipo):
    # Define un endpoint /pokemon/aleatorio/<tipo> que requiere autenticación JWT y devuelve un Pokémon aleatorio de un tipo específico.

    try:
        url = f"https://pokeapi.co/api/v2/type/{tipo.lower()}"
        response = requests.get(url)
        response.raise_for_status()
        # Construye la URL para consultar la API de PokeAPI con el tipo de Pokémon y realiza una solicitud GET. Si la respuesta tiene un código de error, lanza una excepción.

        data = response.json()
        # Convierte la respuesta en un objeto JSON.

        pokemons = [poke['pokemon']['name'] for poke in data['pokemon']]
        # Extrae los nombres de los Pokémon del tipo especificado desde la respuesta JSON.

        if pokemons:
            pokemon_aleatorio = random.choice(pokemons)
            return jsonify({'tipo': tipo, 'pokemon_aleatorio': pokemon_aleatorio})
        else:
            return jsonify({'error': f'No se encontraron Pokémon para el tipo {tipo}'}), 404
        # Si se encontraron Pokémon, selecciona uno al azar y lo devuelve en una respuesta JSON. Si no, devuelve un error 404.

    except requests.exceptions.HTTPError as e:
        return jsonify({'error': f'Error al conectar con PokeAPI: {e.response.status_code}', 'details': str(e)}), e.response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error al conectar con PokeAPI', 'details': str(e)}), 500
    except (KeyError, TypeError, IndexError):
        return jsonify({'error': 'Datos inesperados recibidos de PokeAPI o no se encontró ningún Pokémon'}), 500
    # Maneja errores que pueden ocurrir durante la solicitud HTTP o al procesar la respuesta JSON.

# Obtener el Pokémon con el nombre más largo de cierto tipo
@app.route('/pokemon/mas_largo/<tipo>', methods=['GET'])
@jwt_required()  # Requiere autenticación JWT
def pokemon_mas_largo(tipo):
    # Define un endpoint /pokemon/mas_largo/<tipo> que requiere autenticación JWT y devuelve el Pokémon con el nombre más largo de un tipo específico.

    try:
        url = f"https://pokeapi.co/api/v2/type/{tipo.lower()}"
        response = requests.get(url)
        response.raise_for_status()
        # Construye la URL para consultar la API de PokeAPI con el tipo de Pokémon y realiza una solicitud GET. Si la respuesta tiene un código de error, lanza una excepción.

        data = response.json()
        # Convierte la respuesta en un objeto JSON.

        pokemons = [poke['pokemon']['name'] for poke in data['pokemon']]
        # Extrae los nombres de los Pokémon del tipo especificado desde la respuesta JSON.

        if pokemons:
            pokemon_mas_largo = max(pokemons, key=len)
            return jsonify({'tipo': tipo, 'pokemon_mas_largo': pokemon_mas_largo})
        else:
            return jsonify({'error': f'No se encontraron Pokémon para el tipo {tipo}'}), 404
        # Si se encontraron Pokémon, selecciona el de nombre más largo y lo devuelve en una respuesta JSON. Si no, devuelve un error 404.

    except requests.exceptions.HTTPError as e:
        return jsonify({'error': f'Error al conectar con PokeAPI: {e.response.status_code}', 'details': str(e)}), e.response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error al conectar con PokeAPI', 'details': str(e)}), 500
    except (KeyError, TypeError, ValueError):
        return jsonify({'error': 'Datos inesperados recibidos de PokeAPI o no se encontró ningún Pokémon'}), 500
    # Maneja errores que pueden ocurrir durante la solicitud HTTP o al procesar la respuesta JSON.

# Obtener un Pokémon al azar que contenga alguna de las letras ‘I’,’A’,’M’ en su nombre y sea del tipo más fuerte basado en el clima de Bogotá
@app.route('/pokemon/fuerte', methods=['GET'])
@jwt_required()  # Requiere autenticación JWT
def pokemon_fuerte():
    # Define un endpoint /pokemon/fuerte que requiere autenticación JWT y devuelve un Pokémon al azar que contenga alguna de las letras 'I', 'A', 'M' en su nombre y sea del tipo más fuerte según el clima de Bogotá.

    try:
        # Obtener el clima actual en Bogotá usando la API de open-meteo
        weather_url = "https://api.open-meteo.com/v1/forecast?latitude=4.7110&longitude=-74.0721&current_weather=true"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        # Construye la URL para consultar la API de open-meteo con la ubicación de Bogotá y realiza una solicitud GET. Si la respuesta tiene un código de error, lanza una excepción.

        weather_data = weather_response.json()
        temperatura = weather_data['current_weather']['temperature']
        # Convierte la respuesta en un objeto JSON y extrae la temperatura actual.

        # Determinar el tipo más fuerte basado en la temperatura
        if temperatura >= 30:
            tipo_fuerte = 'fire'
        elif 20 <= temperatura < 30:
            tipo_fuerte = 'ground'
        elif 10 <= temperatura < 20:
            tipo_fuerte = 'normal'
        elif 0 <= temperatura < 10:
            tipo_fuerte = 'water'
        else:
            tipo_fuerte = 'ice'
        # Determina el tipo de Pokémon más fuerte basado en la temperatura actual según la tabla proporcionada.

        # Obtener los Pokémon de ese tipo
        url = f"https://pokeapi.co/api/v2/type/{tipo_fuerte}"
        response = requests.get(url)
        response.raise_for_status()
        # Construye la URL para consultar la API de PokeAPI con el tipo de Pokémon determinado y realiza una solicitud GET. Si la respuesta tiene un código de error, lanza una excepción.

        data = response.json()
        pokemons = [poke['pokemon']['name'] for poke in data['pokemon']]
        # Extrae los nombres de los Pokémon del tipo determinado desde la respuesta JSON.

        # Filtrar Pokémon que contengan las letras 'I', 'A', 'M'
        filtrados = [poke for poke in pokemons if any(letra in poke.upper() for letra in 'IAM')]
        # Filtra los Pokémon cuyos nombres contengan alguna de las letras 'I', 'A', 'M'.

        if filtrados:
            pokemon_aleatorio = random.choice(filtrados)
            return jsonify({'tipo_fuerte': tipo_fuerte, 'pokemon_fuerte': pokemon_aleatorio})
        else:
            return jsonify({'error': f'No se encontró ningún Pokémon con las letras I, A, M para el tipo {tipo_fuerte}'}), 404
        # Si se encontraron Pokémon que cumplen con los criterios, selecciona uno al azar y lo devuelve en una respuesta JSON. Si no, devuelve un error 404.

    except requests.exceptions.HTTPError as e:
        return jsonify({'error': f'Error al conectar con la API externa: {e.response.status_code}', 'details': str(e)}), e.response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error al conectar con la API externa', 'details': str(e)}), 500
    except (KeyError, TypeError):
        return jsonify({'error': 'Datos inesperados recibidos de la API externa'}), 500
    # Maneja errores que pueden ocurrir durante la solicitud HTTP o al procesar la respuesta JSON.

if __name__ == '__main__':
    app.run(debug=True)
# Inicia la aplicación Flask en modo debug, lo que permite la depuración interactiva y reinicios automáticos en caso de cambios en el código.
