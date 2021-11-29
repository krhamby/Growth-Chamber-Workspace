# TODO: These will be used later to create a password for the webpage
from flask.helpers import flash
from myforms import NameForm, EmailForm, DataChangeForm

# TODO: Can remove this once SQL implemtation is complete
from datapack import data_db

# Flask imports
from flask import Flask
from flask import render_template, url_for, redirect, jsonify
from flask import request, session

# imports for the database
import os, random
from flask_sqlalchemy import SQLAlchemy

# Used to create dummy data
from datetime import datetime, timedelta

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
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, nullable = False)
    lux = db.Column(db.Unicode, nullable = False)
    temperature = db.Column(db.Float, nullable = False)
    humidity = db.Column(db.Unicode, nullable = False)
    def __str__(self):
        return f"Data(time={self.timestamp}, lux={self.lux}, temperature={self.temperature}, humidity={self.humidity})"
    def __repr__(self):
        return f"Data({self.id})"
    def to_json(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "lux": self.lux,
            "temperature": self.temperature,
            "humidity": self.humidity
        }

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
    data_set = Data.query.all() # TODO: may need to sort the data after this line
    return jsonify({
        'data': [data.to_json() for data in data_set]
    })

@app.route("/", methods = ["GET", "POST"])
def index():
    data = Data.query.order_by(Data.timestamp.asc()).all()
    form = DataChangeForm()
    if request.method == "GET":
        return render_template("webpage.html", data = data, form = form)
    elif request.method == "POST":
        if form.validate():
            # To fully implement the ability to write the data to a JSON
            # file, I will have to build a JS frontend (I think--this is just a guess) 
            session["time"] = form.time.data
            session["data"] = form.data.data
            return redirect(url_for("index"))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}")
                return redirect(url_for("index"))