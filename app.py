from flask import Flask, request, json, render_template
from openai import OpenAI
from flask_cors import CORS
# import yaml
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home ():
    return "home"

@app.route('/get-image-list', methods=["GET"])
def get_image_list ():
    with open('DB.json') as json_file:        
        if json_file.read() == '':
            return []
        
        with open('DB.json', 'r') as json_data:
            image_list = json.load(json_data)
            return render_template("index.html", image_list = image_list)

@app.route('/upload-image', methods=["POST"])
def uppload_image ():
    return str(os.environ.get("HEROKU_API"))
  