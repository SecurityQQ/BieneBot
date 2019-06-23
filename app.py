from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

import generate_gifs

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


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=80)