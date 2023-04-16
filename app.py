from flask import Flask, render_template, url_for, redirect, request, session
import requests, os, uuid, json
from dotenv import load_dotenv

load_dotenv()

# Load ENV Values
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
TRANSLATOR_LOCATION = os.getenv("TRANSLATOR_LOCATION")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def translate():
    original_text = request.form['text']
    target_language = request.form['language']
    
    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + target_language
    target_url = TRANSLATOR_ENDPOINT + path + target_language_parameter
    
    # Setup Request
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_LOCATION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [
        {
            'text': original_text
        }
    ]
    
    # Translation service
    translated_request = requests.post(target_url, headers=headers, json=body)
    translate_response = translated_request.json()
    translated_key_items = translate_response[0]["translations"][0]
    
    return render_template(
        "result.html",
        original_text = original_text,
        translated_text = translated_key_items["text"],
        translated_language = translated_key_items['to'],
    )
    
    
