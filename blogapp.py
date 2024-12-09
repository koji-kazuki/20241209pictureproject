from flask import Flask
from flask import render_template

app = Flask(__name__)

app.config.from_pyfile('settings.py')

@app.route('/')
def index():
    
    return render_template('index.html')

