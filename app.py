from flask import Flask
from decouple import config

app = Flask(__name__)

@app.route("/")
def index():
  return "Hello World!"

# query for new tweets that follow particular pattern.