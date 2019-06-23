import os
import requests
from flask import Flask, jsonify, request

from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)

import generate_gifs

CHANNEL_CHAT_ID = -1001338525741
CLARIFY_TOKEN = '7f757c7d67a0478aa81c49fd01595b2c'

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
    if request.args.get('rotate'):
        rotate = int(request.args.get('rotate'))
    else:
        rotate = 10

    result_url = generate_gifs.filter_image(image_url, template, rotate)
    return jsonify({'url': result_url})


@app.route('/filter_with_ai', methods=['GET'])
def filter_using_ai():
    image_url = request.args.get('url')

    template_sequence = generate_gifs.random_walk()

    next_url = image_url

    res = {}
    worked_iteration = 0
    for templ in template_sequence:
        try:
            next_url = generate_gifs.filter_image(
                next_url, 
                templ, 
            )
            res[worked_iteration] = {
                "url": next_url,
                "template": int(templ)
            }
            worked_iteration += 1
        except:
            pass

    return jsonify({
        'steps': res,
        'url': next_url
    })


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


from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
clapp = ClarifaiApp(api_key=CLARIFY_TOKEN)
model = clapp.public_models.general_model
model.model_version = 'aa7f35c01e0642fda5cf400f543e7c40'


@app.route('/clarify', methods=['GET'])
def clarify():
    content_url = request.args.get('url')
    image = ClImage(url=content_url)
    prediction = model.predict([image])
    return jsonify(prediction)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0", 
        debug=True, 
        threaded=True, 
        port=80
    )