from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


PRJT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = PRJT_PATH + '\databases'
app = Flask(__name__)
print(f'sqlite://///{DB_PATH}/database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://///{DB_PATH}\database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://///c/Users/denis/x5/Performance_appraisal/prototype/databases/database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

db.create_all()