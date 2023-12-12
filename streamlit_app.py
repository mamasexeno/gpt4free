from flask import Flask, jsonify, request
from flask_cors import CORS
import g4f
from g4f import BaseProvider, models, Provider
from random import choice
import multiprocessing
logging = True

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, resources={r"/*": {"origins": "*"}})
g4f.logging = True

_providers = [
    g4f.Provider.MyShell,
    g4f.Provider.GPTalk,
    g4f.Provider.FakeGpt,
    g4f.Provider.FreeGpt
]
def process_content(content):
    try:
        response = g4f.ChatCompletion.create(
           model=g4f.models.default,
            messages=[{"role": "user", "content": content}],
            timeout=120,
        )
    except:
        response = g4f.ChatCompletion.create(
             model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": content}],
            timeout=120,
        )
    return response

@app.route('/', methods=['POST'])
def main():
    content = request.form.get('content', '')

    response = process_content(content)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run()
