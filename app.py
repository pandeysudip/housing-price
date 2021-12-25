from flask import Flask, render_template, redirect, jsonify, request
from pymongo import MongoClient
import utilis
import json
from bson import json_util


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
client = MongoClient("mongodb://localhost:27017")
db = client['us-housing-prediction']
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
    # Store the entire collection as a list
    census_2017_list = list(census_2017.find())
    census_2019_list = list(census_2019.find())
    predict_list = list(predictions.find())

    # Return the template
    return render_template('index.html', predict_list=predict_list, census_2019_list=census_2019_list, census_2017_list=census_2017_list)


@app.route('/prediction.html')
def prediction():
    # Store the entire collection as a list
    census_2017_list = list(census_2017.find())
    census_2019_list = list(census_2019.find())
    predict_list = list(predictions.find())

    # Return the template
    return render_template('prediction.html',  predict_list=predict_list, census_2019_list=census_2019_list, census_2017_list=census_2017_list)


@app.route('/contact.html')
def contact():
    # Return the template
    return render_template('contact.html')


@app.route('/predict/', methods=["GET", "POST"])
def predict():
    # Store the entire collection as a list
    census_2017_list = list(census_2017.find())
    census_2019_list = list(census_2019.find())
    predict_list = list(predictions.find())

    if request.method == "POST":
        city = request.form.get("City")
    prediction = utilis.preprocess(city)

    # Return the template
    return render_template('predict.html', prediction=prediction,  predict_list=predict_list, census_2019_list=census_2019_list, census_2017_list=census_2017_list)


@app.route("/data/2019")
def get_census_2019():
    census_2019_list = list(census_2019.find())
    return json.dumps(census_2019_list, default=json_util.default)


@app.route("/data/2017")
def get_census_2017():
    census_2017_list = list(census_2017.find())
    return json.dumps(census_2017_list, default=json_util.default)


@app.route("/data/predict")
def get_predict():
    predict_list = list(predictions.find())
    return json.dumps(predict_list, default=json_util.default)


@app.route("/data/all_data")
def get_all():
    # Store the entire collection as a list
    census_2017_list = list(census_2017.find())
    predict_list = list(predictions.find())
    all_list = census_2017_list+predict_list
    return json.dumps(all_list, default=json_util.default)


if __name__ == "__main__":
    app.run(debug=True)
