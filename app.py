from flask import Flask, render_template, redirect, jsonify
import flask
from pymongo import MongoClient
import utilis
import json
import os
from bson import json_util
from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#client = MongoClient("mongodb://localhost:27017")

app.config["MONGO_URI"] = os.environ.get('MONGODB_URI', '')
mongo = PyMongo(app, tls=True)

# create database
#db = mongo['us-agriculture']
db = mongo.db['us-housing-prediction']
# creating collection
census_2019 = db['census_2019']
census_2017 = db['census_2017']
predictions = db['predictions']


@app.route('/')
def home():
    # Return the template
    return render_template('home.html')


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


@app.route('/prediction.html', methods=["GET", "POST"])
def predic():
    if flask.request.method == "POST":

        MonthlyOwnerCost = flask.request.form.get('Monthly Owner Cost')
        PerCapitaIncome = flask.request.form.get("Per Capita Income")
        Lng = flask.request.form.get("Lng")
        Lat = flask.request.form.get('Lat')
        Lat, *_ = Lat
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

        return render_template("prediction.html", pred=variables, prediction=predict)
    else:
        return render_template("prediction.html")


@ app.route("/data/2019")
def get_census_2019():
    census_2019_list = list(census_2019.find())
    return json.dumps(census_2019_list, default=json_util.default)


@ app.route("/data/2017")
def get_census_2017():
    census_2017_list = list(census_2017.find())
    return json.dumps(census_2017_list, default=json_util.default)


@ app.route("/data/predict")
def get_predict():
    predict_list = list(predictions.find())
    return json.dumps(predict_list, default=json_util.default)


@ app.route("/data/all_data")
def get_all():
    # Store the entire collection as a list
    census_2017_list = list(census_2017.find())
    predict_list = list(predictions.find())
    all_list = census_2017_list+predict_list
    return json.dumps(all_list, default=json_util.default)


if __name__ == "__main__":
    app.run(debug=True)
