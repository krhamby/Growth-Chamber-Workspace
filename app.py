# TODO: These will be used later to create a password for the webpage
from flask.helpers import flash
from myforms import NameForm, EmailForm, DataChangeForm, WaterForm

# TODO: Can remove this once SQL implemtation is complete
# from datapack import data_db

# Flask imports
from flask import Flask
from flask import render_template, url_for, redirect, jsonify
from flask import request, session

# imports for the database
import os
import random
from flask_sqlalchemy import SQLAlchemy

# Used to create dummy data
from datetime import datetime, timedelta

# imports for filtering
from sqlalchemy import func
import json
import sys

# Determine the absolute path of our database file
scriptdir = os.path.abspath(os.path.dirname(__file__))
dbpath = os.path.join(scriptdir, 'sensor_data.sqlite3')

# Configure the Flask App
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE'] = 0
app.config['SECRET_KEY'] = 'anystring'

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbpath}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Getting the database object handle from the app
db = SQLAlchemy(app)

# Define model for Data table
class Data(db.Model):
    __tablename__ = "Data"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Text, nullable=False)
    lux = db.Column(db.Unicode, nullable=False)
    temperature = db.Column(db.Unicode, nullable=False)
    humidity = db.Column(db.Unicode, nullable=False)

    def __str__(self):
        return f"Data(time={self.timestamp}, lux={self.lux}, temperature={self.temperature}, humidity={self.humidity})"

    def __repr__(self):
        return f"Data({self.id})"

    def to_json(self):
        return {"timestamp": self.timestamp, "lux": self.lux, "temperature": self.temperature, "humidity": self.humidity}

# Define model for Schedule table
class Schedule(db.Model):
    __tablename__ = "Schedule"
    id = db.Column(db.Text, primary_key=True)
    startTime = db.Column(db.Text, nullable=False)
    endTime = db.Column(db.Text, nullable=False)

# Define model for Interval table
class Interval(db.Model):
    __tablename__ = "Interval"
    id = db.Column(db.Text, primary_key=True)
    duration = db.Column(db.Text, nullable=False)
    interval = db.Column(db.Integer, nullable=False)

# ONLY USE THIS IN DEVELOPMENT
# db.drop_all()

# Only needed if the tables are not created
db.create_all()

# for i in range(100):
#     # Dummy data for testing
#     multiple_instances = [
#         Data(timestamp = datetime.now(), lux = random.randint(80000, 85000), temperature = random.randint(65, 75), humidity = random.randint(80, 85)),
#     ]

#     # Insert instances into database
#     db.session.add_all(multiple_instances)

#     # Commit changes
#     db.session.commit()
# #     # time.sleep(15)



# Route for database API containing all tuples
@app.get("/api/v1/data/")
def get_all_data():
    data_set = Data.query.all() 
    return jsonify({"data": [data.to_json() for data in data_set]})

@app.get("/api/v1/data/<float:hour>/")
def get_filtered_data(hour):
    time_filter = (datetime.now() - timedelta(hours = hour)).isoformat()
    print(time_filter)
    filtered_data = Data.query.filter(Data.timestamp >= time_filter).all()
    print(filtered_data)
    return jsonify({"data": [data.to_json() for data in filtered_data]})

# Temporary imports for testing (move to top later)
from gpiozero import LED
light = LED(22)

from gpiozero import OutputDevice
pump = OutputDevice(27)

# Post request for changing the lights
@app.post("/api/v1/functions/<string:func>/")
def post_functions(func):
    if func == "light":
        if light.is_lit:
            light.off()
            print("Light off")
        else:
            light.on()
            print("Light on")
    elif func == "water":
        if pump.is_active:
            pump.off()
            print("Water off")
        else:
            pump.on()
            print("Water on")
    return jsonify({"status": "success"})

@app.route("/", methods=["GET", "POST"])
def index(): 
    data = Data.query.order_by(Data.timestamp.asc()).all()
    # data = get_all_data()
    form = DataChangeForm()
    waterForm = WaterForm()
    if request.method == "GET":
        return render_template("webpage.html", data=data, form=form, waterForm=waterForm)
    elif request.method == "POST":
        if waterForm.validate():
            # Check if interval exists
            interval = Interval.query.filter_by(id="water").first()
            if interval:
                # Update interval
                interval.interval = waterForm.interval.data
                interval.duration = waterForm.minutes.data
            else:
                # Create new interval
                interval = Interval(id="water", interval=waterForm.interval.data, duration=waterForm.minutes.data)
                db.session.add(interval)
            db.session.commit()
            print(f"Watering for {waterForm.minutes.data} minutes every {waterForm.interval.data} hours")
            return redirect(url_for("index"))
        elif form.validate():
            startTime = form.startTime.data.strftime("%H:%M")
            endTime = form.endTime.data.strftime("%H:%M")

            # Check if the schedule already exists
            schedule = Schedule.query.filter_by(id="lux").first()
            if schedule:
                # Update the schedule
                schedule.startTime = startTime
                schedule.endTime = endTime
            else:
                # Create a new schedule
                schedule = Schedule(id="lux", startTime=startTime, endTime=endTime)
                db.session.add(schedule)
            # schedule = Schedule(id = "lux", startTime = startTime, endTime = endTime)
            # db.session.add(schedule)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}")
                return redirect(url_for("index"))
                
# Imports for measuring and writing data
import data
from threading import Thread

# Runs data.py concurrently; will use a separate terminal later
Thread(target = data.main).start()