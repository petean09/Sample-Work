from flask import Flask
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'^\x97\x91S!\xc1\x1b\xce\x0b\x92\xd8\x15Q$\xfe\x9f'

db = SQLAlchemy(app)
