
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect
from flask_migrate import Migrate
import socket  

s = socket.socket()  

port = 12345   

IPF = "1.2.3.4"
num = 1
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

migrate = Migrate(app, db)
 
# Models
class Sensor_Data(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    ip_addr = db.Column(db.String(20), unique=False, nullable=False)
    sensor1 = db.Column(db.String(20), unique=False, nullable=False)
    sensor2 = db.Column(db.String(20), unique=False, nullable=False)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    profiles = Sensor_Data.query.all()
    return render_template('index.html', profiles=profiles, value=num)

@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')

# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
    # In this function we will input data from the
    # form page and store it in our database. Remember
    # that inside the get the name shoukd exactly be the same
    # as that in the html input fields
    ip_addr = request.form.get("ip_addr")
    # sensor1 = request.form.get("sensor1")
    # sensor2 = request.form.get("sensor2")
 
    # create an object of the Profile class of models and
    # store data as a row in our datatable
    if ip_addr != '':
        p = Sensor_Data(ip_addr=ip_addr, sensor1="", sensor2="")
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/update/<int:id>')
def edit(id):
    data = Sensor_Data.query.get(id)
    #data = Sensor_Data.query.filter_by(ip_addr=IPF).first()

    s = socket.socket()  
    s.connect(('192.168.1.19', port))
    sens_data = s.recv(1024).decode()
    sens_data = eval(sens_data)
    s.close()

    data.sensor1 = sens_data[0]
    data.sensor2 = sens_data[1]
    db.session.commit()
    return redirect('/')
 
@app.route('/delete/<int:id>')
def erase(id):
    
    # letes the data on the basis of unique id and
    # directs to home page
    data = Sensor_Data.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="0.0.0.0")