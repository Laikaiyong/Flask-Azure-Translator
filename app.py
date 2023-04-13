from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

# Load the values from .env
TRANSLATOR_KEY = os.environ['TRANSLATOR_KEY']
TRANSLATOR_ENDPOINT = os.environ['TRANSLATOR_ENDPOINT']
TRANSLATOR_LOCATION = os.environ['TRANSLATOR_LOCATION']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def translate():
    original_text = request.form['text']
    target_language = request.form['language']

    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + target_language
    target_url = TRANSLATOR_ENDPOINT + path + target_language_parameter

    # Setup request
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_LOCATION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{ 'text': original_text }]

    # Translation service
    translator_request = requests.post(target_url, headers=headers, json=body)
    translator_response = translator_request.json()
    translated_text = translator_response[0]['translations'][0]['text']

    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )