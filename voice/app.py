import random
import pyttsx3
import spacy
from textblob import TextBlob
import speech_recognition as sr
from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, db
import json
import os
from dotenv import load_dotenv


load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
}


# cred = credentials.Certificate("D:/GitHub/BIT-Voice-Assistant-main/voice/voice-e358a-firebase-adminsdk-o9t2y-1ef8f373a8.json")

try:
    firebase_admin.initialize_app(cred, firebase_config)
except Exception as e:
    print(f"Firebase initialization error: {e}")




app = Flask(__name__)

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def analyze_sentiment(text):
    # Use TextBlob for sentiment analysis
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        return "positive"
    elif sentiment_score < 0:
        return "negative"
    else:
        return "neutral"

def text_to_speech(text, language='en', voice_gender='f'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Select voice based on language and gender
    if language == 'ta':
        voice_id = 'ta+m1' if voice_gender == 'm' else 'ta+f1'
    elif language == 'hi':
        voice_id = 'hi+m1' if voice_gender == 'm' else 'hi+f1'
    else:
        voice_id = 'en+m3' if voice_gender == 'm' else 'en+f3'

    # Set the selected voice
    selected_voice = None
    for voice in voices:
        if voice_id in voice.id:
            selected_voice = voice
            break

    if selected_voice:
        engine.setProperty('voice', selected_voice.id)
    else:
        print(f"Voice not found for voice ID: {voice_id}. Using the default voice.")

    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def get_responses():
    ref = db.reference('/responses')
    return ref.get() or {}

def add_response(patterns, response):
    ref = db.reference('/responses')
    ref.push({
        'patterns': patterns,
        'response': response
    })

def update_response(key, patterns, response):
    ref = db.reference(f'/responses/{key}')
    ref.update({
        'patterns': patterns,
        'response': response
    })

def delete_response(key):
    ref = db.reference(f'/responses/{key}')
    ref.delete()


def process_query():
    continue_playing = True
    language_choice = ''
    voice_gender = ''

    while continue_playing:
        r = sr.Recognizer()

        if not language_choice:
            text_to_speech("Select a language (English, Tamil, Hindi):")
            with sr.Microphone() as source:
                audio = r.listen(source)

            try:
                language_choice = r.recognize_google(audio)
                if language_choice.lower() not in ["en", "ta", "hi"]:
                    language_choice = 'en'
            except sr.UnknownValueError:
                continue

        if not voice_gender:
            text_to_speech("Select a voice gender (male or female):")
            with sr.Microphone() as source:
                audio = r.listen(source)

            try:
                voice_gender = r.recognize_google(audio)
                if voice_gender.lower() not in ["male", "female"]:
                    voice_gender = 'male'
            except sr.UnknownValueError:
                continue

        text_to_speech("Now you can ask queries.")

        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            question = r.recognize_google(audio)
            sentiment = analyze_sentiment(question)
            print(f"Sentiment: {sentiment}")

            if sentiment == "positive":
              text_to_speech("I sense a positive sentiment in your query thats great")
            elif sentiment == "negative":
              text_to_speech("I sense a negative sentiment in your query I am here to help  lets see if I can address any concerns.")
            else:
              text_to_speech("Your query seems neutral If you have any questions feel free to ask.")
        except sr.UnknownValueError:
            continue

        if question.lower() == "exit":
            break
        else:
            response = generate_response(question, language_choice, voice_gender)
            text_to_speech(response, language_choice, voice_gender)

            # Store the user's voice command in Firebase
            store_command(question, language_choice, voice_gender)

        while True:
            text_to_speech("Do you have any other queries? Say 'yes' or 'no'.")
            with sr.Microphone() as source:
                audio = r.listen(source)

            try:
                next_question = r.recognize_google(audio).lower()

                if any(keyword in next_question for keyword in ['yes', 'yeah', 'yup', 'sure']):
                    break
                elif 'no' in next_question:
                    continue_playing = False
                    break
            except sr.UnknownValueError:
                continue

    text_to_speech("Thank you for using the query system. Goodbye!")
    return redirect('/')

def generate_response(question, language_choice, voice_gender):
    responses = get_responses()
    
    # Process the question using spaCy for entity recognition
    doc = nlp(question)
    entities = [ent.text.lower() for ent in doc.ents]

    # Check each response pattern in the database
    for key, response_entry in responses.items():
        if all(keyword.lower() in question.lower() for keyword in response_entry['patterns']):
            return response_entry['response']

    # If no matching pattern is found, return a default response
    return "Sorry, I don't have an answer for that."

def store_command(question, language_choice, voice_gender):
    # Get a reference to the database
    ref = db.reference('/voice_commands')

    # Push the voice command data to the database
    ref.push({
        'question': question,
        'language_choice': language_choice,
        'voice_gender': voice_gender
    })

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip()
    if not user_input:
        return {"response": "Please provide a message to process."}, 400

    # Process the input and generate a response
    response = generate_response(user_input, "en", "f")  # Assuming English and female voice for chatbot
    return {"response": response}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    return process_query()

@app.route('/admin')
def admin_index():
    responses = get_responses()
    return render_template('admin.html', responses=responses)

@app.route('/admin/add', methods=['POST'])
def admin_add():
    patterns = request.form.getlist('patterns')
    response = request.form.get('response')
    add_response(patterns, response)
    return redirect('/admin')

@app.route('/admin/update/<key>', methods=['POST'])
def admin_update(key):
    patterns = request.form.getlist('patterns')
    response = request.form.get('response')
    update_response(key, patterns, response)
    return redirect('/admin')

@app.route('/admin/delete/<key>', methods=['POST'])
def admin_delete(key):
    delete_response(key)
    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)
