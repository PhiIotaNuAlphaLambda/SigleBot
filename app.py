from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('PY_DB_URL')
db = SQLAlchemy(app)

@app.route("/")
def index():
  return "Hello World!"

class RetweetedTweet(db.Model):
  id=db.Column(db.Integer, primary_key=True)
  post_url=db.Column(db.String(200), unique=True, nullable=False)
  date_retweeted=db.Column(db.DateTime, unique=False, nullable=False)
