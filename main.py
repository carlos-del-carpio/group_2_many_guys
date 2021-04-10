import os
from flask import Flask
from flask import render_template
# from flask import request
# from flask import redirect, url_for


app = Flask(__name__)  # create an app


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
