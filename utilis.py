import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler


def preprocess(variables=['Monthly Owner Cost', 'Per Capita Income',
                          'Lng', 'Household Income', 'College Rate', 'Lat',
                          'Personal Transport Rate', 'High School Rate', 'Median Age',
                          'Public Transport Rate', 'Population']):
    std_scaler = StandardScaler()
    test_data = std_scaler.fit_transform([variables])
    trained_model = joblib.load('model.pkl')
    prediction = trained_model.predict(test_data)

    return prediction
