from flask import Flask, render_template, redirect, jsonify
import flask
from pymongo import MongoClient
import json
import os
import utilis
from bson import json_util
from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#client = MongoClient("mongodb://localhost:27017")
#
#
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', '')
app.config['MONG_DBNAME'] = 'us-housing'
mongo = PyMongo(app)

# create database
#db = client['us-housing-prediction']
#db = mongo.db['us-housing']
# creating collection
#census_2019 = mongo.db['census_2019']
#census_2017 = mongo.db['census_2017']
predictions = mongo.db['predictions']


@app.route('/')
def home():
    # Return the template
    return render_template('index.html')


@app.route('/index.html')
def index():

    # Return the template
    return render_template('index.html')


@app.route('/maps.html')
def maps():
    # Store the entire collection as a list

    # Return the template
    return render_template('maps.html')


@app.route('/contact.html')
def contact():
    # Return the template
    return render_template('contact.html')


@app.route('/send', methods=["GET", "POST"])
def predic():
    if flask.request.method == "POST":
        MonthlyOwnerCost = flask.request.form.get('Monthly Owner Cost')
        PerCapitaIncome = flask.request.form.get("Per Capita Income")
        Lng = flask.request.form.get("Lng")
        Lat = flask.request.form.get('Lat')
        HouseholdIncome = flask.request.form.get('Household Income')
        CollegeRate = flask.request.form.get('College Rate')
        PersonalTransportRate = flask.request.form.get(
            'Personal Transport Rate')
        HighSchoolRate = flask.request.form.get('High School Rate')
        MedianAge = flask.request.form.get('Median Age')
        PublicTransportRate = flask.request.form.get('Public Transport Rate')
        Population = flask.request.form.get('Population')
        variables = [MonthlyOwnerCost, PerCapitaIncome, Lng,  HouseholdIncome,
                     CollegeRate, Lat, PersonalTransportRate, HighSchoolRate, MedianAge, PublicTransportRate, Population]
        predict = utilis.preprocess(variables)
        #predict, *_ = predict
        # Return the template

        #
        return render_template("index.html", pred=variables, prediction=predict)
    else:
        return render_template("index.html")


@ app.route("/data/predict")
def get_predict():
    predict_list = list(predictions.find())
    return json.dumps(predict_list, default=json_util.default)


if __name__ == "__main__":
    app.run(debug=True)
