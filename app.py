from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
import requests
from db import Database


app = Flask(__name__)
app.secret_key = 'your_secret_key'
db = Database(host = 'localhost', user = 'root', password = 'Ajay@123', database = 'nlp_app')
#you can also create the database
db.create_user_table()  # Ensure the user table is created when the app starts

HF_API_TOKEN = "your token here"

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = db.validate_user(email, password)
    if user:
        session['user_id'] = user['id']
        session['user'] = user['first_name']
        flash('Login successful!', 'success')
        return redirect(url_for('profile'))

    flash('Login failed. Please check your credentials.', 'danger')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        email = request.form['email']
        password = request.form['password']
        if db.get_user_by_email(email):
            flash('Email already registered. Please log in or register', 'warning')
            return redirect(url_for('register'))
        db.add_user(first_name, email, password)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        flash('Please log in to access your profile.', 'warning')
        return redirect(url_for('home'))
    tab = request.args.get('tab', 'ner')
    return render_template('profile.html', active_tab=tab, session=session)

@app.route('/ner', methods=['POST'])
def ner():
    if 'user' not in session:
        return redirect(url_for('home'))
    text = request.form['ner_text']

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    response = requests.post(
        "https://api-inference.huggingface.co/models/dbmdz/bert-large-cased-finetuned-conll03-english",
        headers=headers,
        json={"inputs": text}
    )
    try:
        result = response.json()
    except Exception:
        result = {"error": f"API Error: {response.status_code} - {response.text}"}
    return render_template('profile.html', ner_result=result, active_tab='ner', session=session)



@app.route('/sentiment', methods=['POST'])
def sentiment():
    if 'user' not in session:
        return redirect(url_for('home'))
    text = request.form['sentiment_text']

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    response = requests.post(
        "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment",
        headers=headers,
        json={"inputs": text}
    )
    try:
        result = response.json()
    except Exception:
        result = {"error": f"API Error: {response.status_code} - {response.text}"}
    return render_template('profile.html', sentiment_result=result, active_tab='sentiment', session=session)

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'user' not in session:
        return redirect(url_for('home'))
    text = request.form['summarize_text']

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

    # Set max_length to a lower value for a shorter summary
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": 10,
            "max_length": 40
        }
    }
    response = requests.post(
        "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6",
        headers=headers,
        json=payload
    )
    try:
        result = response.json()
    except Exception:
        result = {"error": f"API Error: {response.status_code} - {response.text}"}
    return render_template('profile.html', summarize_result=result, active_tab='summarize', session=session)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)

login_id = "123"
    