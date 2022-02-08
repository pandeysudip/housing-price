import joblib
import numpy as np


def preprocess(variables):
    # using standardscaler for transformation
    scaler = joblib.load('scaler.pkl')
    X_scaler = scaler.transform([variables])

    test_data = scaler.transform(X_scaler)
    trained_model = joblib.load('model.pkl')
    prediction = trained_model.predict(test_data)

    return f'Predicted Housing Value is:{prediction}'
