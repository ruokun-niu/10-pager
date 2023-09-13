# MIT License

# Copyright (c) 2023 Ruokun Niu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from flask import Flask, request, jsonify, render_template, abort
from flask_caching import Cache
from flask_cors import CORS
from pdf.document import load_pdf_from_dir, split_document
from llm.openai_instance import OpenAIInstance
from utils.utils import allowed_file

import os

UPLOAD_FOLDER = 'uploads'


app = Flask(__name__)
app.config["CACHE_TYPE"] = "SimpleCache"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cache = Cache(app)
CORS(app)


try:
    path = os.path.dirname(os.path.abspath(__file__))
    upload_folder=os.path.join(
    path.replace("/file_folder",""),"tmp")
    os.makedirs(upload_folder, exist_ok=True)
    app.config["upload_folder"] = upload_folder
except Exception as e:
    app.logger.info("An error occurred while creating temp folder")
    app.logger.error("Exception occurred : {}".format(e))

open_ai = OpenAIInstance()

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/pdf/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(404, description="File not found")

    file = request.files['file']

    if file.filename == '':
        abort(404, description="File not found")

    if file and allowed_file(file.filename):
        # Create the uploads directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        return jsonify({"message": file_path})
    
    return jsonify({"error": "uploaded failed"})



@app.route('/pdf/qa',  methods=['POST'])
def openai_pdf_instance():
    request_content_str = request.data.decode('utf-8')
    user_input = request_content_str.strip().lower()
    if user_input == "exit":
        return
    
    response = open_ai.pdf_assistant(user_input)


    return jsonify({"message": response})

# Function for testing the endpoint and OpenAI instance
@app.route('/ask', methods=['POST'])
def ask_openai_question():
    request_content_str = request.data.decode('utf-8')
    response = open_ai.openai_instance(request_content_str)

    return jsonify({"message": response})


@app.route('/openai/azure/creds', methods=['POST'])
def obtain_azure_openai_creds():
    global api_key, endpoint
    try:
        data = request.get_json()
        print(data)
        api_key = data.get('api_key')
        endpoint = data.get('endpoint')

        response = {
            'message': 'Inputs received and processed successfully',
            'api_key': api_key,
            'endpoint': endpoint
        }

        open_ai.openai_auth(api_key, endpoint)
        return jsonify(response)
    
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message})


if __name__ == "__main__":
    app.run("localhost", 5002, debug=True)