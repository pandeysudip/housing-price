import joblib
import numpy as np


def preprocess(variables):
    if variables[0] == '' or variables[1] == '' or variables[2] == '' or variables[3] == '' or variables[4] == '' or variables[5] == '' or variables[6] == '' or variables[7] == '' or variables[8] == '' or variables[9] == '' or variables[10] == '':
        return "Please enter all the above information first and click submit. "
    else:
        # using standardscaler for transformation
        scaler = joblib.load('scaler.pkl')
        X_scaler = scaler.transform([variables])

        test_data = scaler.transform(X_scaler)
        trained_model = joblib.load('model.pkl')
        prediction = trained_model.predict(test_data)

        return f'Predicted Housing Price is: ${prediction[0]}0'
