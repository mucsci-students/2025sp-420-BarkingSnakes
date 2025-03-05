from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('./flask.html')

@app.route("/classlist")
def classlist():
    return ["Car", "Racecar", "Spaceship", "School"]