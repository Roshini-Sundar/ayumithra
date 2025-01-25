from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
from langdetect import detect
import requests
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with an environment variable for security
CORS(app)  # Enable CORS for all routes

# Rasa API URL
RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'  # Update the URL if necessary

# Routes

# Welcome page
@app.route('/')
def index():
    return render_template('index.html', title="Welcome")

# Sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add backend validation and integration (e.g., Firebase) here
        flash("Sign Up Successful!", "success")
        return redirect(url_for('profile'))
    return render_template('signup.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add authentication logic here
        flash("Login Successful!", "success")
        return redirect(url_for('homepage'))
    return render_template('login.html')

# Home page
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('home.html')

# Profile page
@app.route('/profilepage', methods=['GET', 'POST'])
def profilepage():
    return render_template('profilepage.html')

# Forum page
@app.route('/forum', methods=['GET', 'POST'])
def forum():
    return render_template('forum.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')

# Profile creation page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        userid = request.form['userid']
        username = request.form['username']
        dob = request.form['dob']
        # Add backend validation and integration here if needed
        flash("Profile Created Successfully!", "success")
        return redirect(url_for('homepage'))
    return render_template('profile.html')

# Translation API
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    target_lang = data.get('target_lang', '')

    try:
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return jsonify({
            'translatedContent': translated_text,
        })
    except Exception as e:
        print(f"Translation Error: {e}")
        return jsonify({'error': 'Translation failed'}), 500

# Chatbot Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json.get('message')
    translate_to = request.json.get('translateTo')

    # Step 1: Detect the input language using langdetect
    try:
        detected_lang = detect(user_message)
        print(f"Detected language: {detected_lang}")
    except Exception as e:
        print(f"Language detection error: {e}")
        detected_lang = 'en'  # Default to English if detection fails

    # Step 2: If the language is supported, translate to English
    supported_languages = ['ta', 'hi', 'ml', 'te', 'kn', 'gu', 'as']
    if detected_lang in supported_languages:
        user_message = GoogleTranslator(source=detected_lang, target='en').translate(user_message)

    # Step 3: Send the translated (or original English) message to Rasa
    response = get_rasa_response(user_message)

    # Step 4: Translate the response back to the preferred language if requested
    if translate_to == 'ta':
        translated_response = GoogleTranslator(source='auto', target='ta').translate(response)
        return jsonify({'response': translated_response})

    elif translate_to == 'hi':
        translated_response = GoogleTranslator(source='auto', target='hi').translate(response)
        return jsonify({'response': translated_response})
    
    elif translate_to == 'ml':  # Malayalam support
        translated_response = GoogleTranslator(source='auto', target='ml').translate(response)
        return jsonify({'response': translated_response})
    
    elif translate_to == 'te':  # Telugu support
        translated_response = GoogleTranslator(source='auto', target='te').translate(response)
        return jsonify({'response': translated_response})
    
    elif translate_to == 'kn':  # Kannada support
        translated_response = GoogleTranslator(source='auto', target='kn').translate(response)
        return jsonify({'response': translated_response})
    elif translate_to == 'gu':  # Gujarati support
        translated_response = GoogleTranslator(source='auto', target='gu').translate(response)
        return jsonify({'response': translated_response})   
        
    elif translate_to == 'as':  # Gujarati support
        translated_response = GoogleTranslator(source='auto', target='as').translate(response)
        return jsonify({'response': translated_response})       

    else:
        return jsonify({'response': response})


# Helper function to communicate with Rasa
def get_rasa_response(user_message):
    try:
        response = requests.post(
            RASA_API_URL,
            json={'sender': 'user', 'message': user_message}
        )
        response.raise_for_status()  # Raise an error for bad responses
        messages = response.json()
        return messages[0]['text'] if messages else "I didn't get that."
    except requests.exceptions.RequestException as e:
        print("Error communicating with Rasa:", e)
        return "Sorry, I couldn't reach the chatbot."

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
