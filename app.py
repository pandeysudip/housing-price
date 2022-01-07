from flask import Flask, render_template, redirect, jsonify, request
import utilis
import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import os
# Create an instance of Flask
app = Flask(__name__)

uri = os.environ.get('DATABASE_URL', '')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/housing-price'

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# getting the tables from database-1st approach
#data_2019 = db.Table('data_2019', db.metadata,autoload=True, autoload_with=db.engine)
#data_2017 = db.Table('data_2017', db.metadata,autoload=True, autoload_with=db.engine)
#prediction = db.Table('prediction', db.metadata,autoload=True, autoload_with=db.engine)

# query be like: db.session.query(train).all()


# getting the tables from database-2nd approach
# reflect an existing database into a new model
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# Save references to each table
data_2019 = Base.classes.data_2019
data_2017 = Base.classes.data_2017
prediction = Base.classes.prediction


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


@ app.route("/data/predict")
def get_predict():
    """Return a list of all passenger names"""
    # Query all data
    results = db. session.query(
        prediction.City, prediction.RandomForestPredictedHouseValue, prediction.Lat, prediction.Lng).all()

    # Convert a dictionary
    # Create a dictionary from the row data and append to a list of all_passengers
    predict_list = []
    for City, RandomForestPredictedHouseValue, Lat, Lng in results:
        prediction_dict = {}
        prediction_dict['City'] = City
        prediction_dict["RandomForestPredictedHouseValue"] = RandomForestPredictedHouseValue
        prediction_dict["Lat"] = Lat
        prediction_dict["Lng"] = Lng
        predict_list.append(prediction_dict)

    return jsonify(predict_list)


if __name__ == "__main__":
    app.run(debug=True)
