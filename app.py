from flask import Flask, request, json, render_template
from openai import OpenAI
from flask_cors import CORS
import yaml
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
    request_body = json.loads(request.data)

    config = load_config()
    return os.environ["GITHUB_ACTOR"]
    client = OpenAI(api_key=config['apk'])
    
    response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "¿ descripcion de esta imagen contando un chiste colombiano ?"},
            {
              "type": "image_url",
              "image_url": {                
                "url": f"data:image/jpeg;base64,{request_body['imgBase64']}"
              },
            },
          ],
        }
      ],
      max_tokens=300,
    )        
    imageList = []
    with open('DB.json') as json_file:        
        if json_file.read() != '':
            with open('DB.json', 'r') as json_data:
                data = json.load(json_data)
                imageList.extend(data)
    
    
    dictionary = {
        "imageBase64": f"{request_body['imgBase64']}",
        "description": str(response.choices[0].message.content)
    }        
    
    imageList.append(dictionary)

    # Serializing json
    json_object = json.dumps(imageList, indent=4)
    
    # Writing to sample.json
    with open("DB.json", "w") as outfile:
        outfile.write(json_object)        
    
    return response.choices[0].message.content
    

def load_config():
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    return config



# if __name__ == "__main__":
#     # app.run(debug=True)
#     app.run()
