from flask import Flask, jsonify, request
import urllib.request
import json
import os
import ssl



def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context
allowSelfSignedHttps(True) 

app= Flask(__name__)

@app.route("/")
def root():
    return "root"

@app.route('/predict', methods=['POST'])
def predic_anemia_level():
    data =request.get_json()

    body = str.encode(json.dumps(data))
    url = 'https://proy-children-anemic-ugnzw.eastus2.inference.ml.azure.com/score'
    api_key = 'Fi7RPPXhlgofRGZxxRx4M9ShOfzeAe9H'
    if not api_key:
        return jsonify({"error":"A key should be provided to invoke the endpoint"}), 404
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'anemic-prediction-model-1' }
    req = urllib.request.Request(url, body, headers)
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return result
    except urllib.error.HTTPError as error:
        return jsonify({"error":"erorrrrrrrr"}), 404
    

if __name__ == "__main__":
    app.run(debug=True)