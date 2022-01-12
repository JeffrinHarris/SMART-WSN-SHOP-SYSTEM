from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"

db = SQLAlchemy(app)

class Sensor_Data(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    ip_addr = db.Column(db.String(20), unique=False, nullable=False)
    sensor1 = db.Column(db.String(20), unique=False, nullable=False)
    sensor2 = db.Column(db.String(20), unique=False, nullable=False)