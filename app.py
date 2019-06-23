import os
import requests
from flask import Flask, jsonify, request

from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)

import generate_gifs

CHANNEL_CHAT_ID = -1001338525741

template_numbers = generate_gifs.get_template_numbers()

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/templates', methods=['GET'])
def get_template():
    return jsonify({'templates': template_numbers})


@app.route('/filter', methods=['GET'])
def filter_image():
    image_url = request.args.get('url')
    template = int(request.args.get('template'))
    rotate = int(request.args.get('rotate'))

    result_url = generate_gifs.filter_image(image_url, template, rotate)
    return jsonify({'url': result_url})


@app.route('/publish', methods=['GET'])
def publist_to_telegram():
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    content_url = request.args.get('url')

    r = requests.get(
        "https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}".format(
            token=TELEGRAM_TOKEN,
            chat_id=CHANNEL_CHAT_ID,
            text=content_url
        )
    )

    return jsonify({'status': r.ok, 'desc': r.text})


if __name__ == '__main__':
    app.run(
        host="0.0.0.0", 
        debug=True, 
        threaded=True, 
        port=80
    )