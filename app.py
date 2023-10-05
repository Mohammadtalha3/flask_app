from flask import Flask



app = Flask(__name__)




@app.route("/")#decorator
def welcome():
    return 'welcome to page'

@app.route("/home")
def home():
    return 'welcome to home page'

@app.route('/click')
def click():
    return "thank you for click"
@app.route('/page')
def page():
    return "welcome to the page"
@app.route('/talha')
def name():
    return "Hello,talha"

from controller import *






