from flask import Flask
from config import Config
from flask_sqlalcehmy import SQLAlchemy
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

