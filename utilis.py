import joblib
import numpy as np


def preprocess(variables=['City', 'Monthly Owner Cost', 'Per Capita Income',
                          'Lng', 'Household Income', 'College Rate', 'Lat',
                          'Personal Transport Rate', 'High School Rate', 'Median Age',
                          'Public Transport Rate', 'Population']):
    test_data = np.array(variables)
    trained_model = joblib.load('model.pkl')
    prediction = trained_model.predict(test_data)

    return prediction
