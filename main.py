import os
from flask import Flask
from flask import render_template, url_for
from flask import redirect
# from flask import request


app = Flask(__name__)  # create an app


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/events')
def events():
    return render_template('events.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
