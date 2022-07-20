from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('PY_DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
  return redirect('https://app.sigle.io/stories/y384X5alCJWPsfVQpHrbk', code=302)

class RetweetedTweet(db.Model):
  id=db.Column(db.Integer, primary_key=True)
  post_url=db.Column(db.String(200), unique=True, nullable=False)
  date_retweeted=db.Column(db.DateTime, unique=False, nullable=False)
