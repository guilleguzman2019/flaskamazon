from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  # Importa la extensión CORS

app = Flask(__name__)

CORS(app)

@app.route('/')
def home():
    return "¡La API de Flask está funcionando!"

@app.route('/productos', methods=['POST'])
def obtener_productos():
    # Obtener el JSON del cuerpo de la solicitud
    data = request.json

    # Estructurar el payload según el formato anterior
    payload = {
        'source': 'amazon_search',
        'domain': 'com',
        'query': data.get('query', ''),
        'start_page': 1,
        'pages': 10,
        'parse': True,
    }

    # Realizar la solicitud a la API externa
    response = requests.post(
        'https://realtime.oxylabs.io/v1/queries',
        auth=('guillermo2020', 'Guillermo2020'),
        json=payload,
    )

    # Procesar la respuesta y estructurar los resultados
    results_array = []
    data = response.json()

    if 'results' in data:
        for result in data['results']:
            if 'content' in result:
                for result_type in ['paid', 'organic', 'suggested']:
                    if result_type in result['content']['results']:
                        for paid_result in result['content']['results'][result_type]:
                            url = paid_result.get('url', '')
                            asin = paid_result.get('asin', '')
                            price = paid_result.get('price', '')
                            title = paid_result.get('title', '')
                            url_image = paid_result.get('url_image', '')

                            result_dict = {
                                'url': url,
                                'asin': asin,
                                'price': price,
                                'title': title,
                                'url_image': url_image,
                            }

                            results_array.append(result_dict)

    return jsonify(results_array)

if __name__ == '__main__':
    app.run(debug=True)

