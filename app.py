from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import joblib


# ---------------------------------------
# Create Flask application
# ---------------------------------------

app = Flask(__name__)

# Allow frontend to communicate with backend
CORS(app)


# ---------------------------------------
# Load trained ML components
# ---------------------------------------

model = joblib.load("../model/water_model.pkl")

imputer = joblib.load("../model/imputer.pkl")

scaler = joblib.load("../model/scaler.pkl")


# ---------------------------------------
# Home route
# ---------------------------------------

@app.route("/")
def home():

    return jsonify({
        "message": "Water Quality Prediction API is running"
    })


# ---------------------------------------
# Prediction route
# ---------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get data sent by JavaScript
        data = request.get_json()


        # ---------------------------------------
        # Create DataFrame
        # ---------------------------------------

        new_data = pd.DataFrame({

            "ph": [data["ph"]],

            "Hardness": [data["hardness"]],

            "Solids": [data["solids"]],

            "Chloramines": [data["chloramines"]],

            "Sulfate": [data["sulfate"]],

            "Conductivity": [data["conductivity"]],

            "Organic_carbon": [data["organic_carbon"]],

            "Trihalomethanes": [data["trihalomethanes"]],

            "Turbidity": [data["turbidity"]]

        })


        # ---------------------------------------
        # Apply same preprocessing
        # ---------------------------------------

        data_imputed = imputer.transform(new_data)

        data_scaled = scaler.transform(data_imputed)


        # ---------------------------------------
        # Make prediction
        # ---------------------------------------

        prediction = model.predict(data_scaled)[0]


        # ---------------------------------------
        # Get probabilities
        # ---------------------------------------

        probability = model.predict_proba(data_scaled)[0]


        not_potable_probability = probability[0] * 100

        potable_probability = probability[1] * 100


        # ---------------------------------------
        # Return result
        # ---------------------------------------

        return jsonify({

            "prediction": int(prediction),

            "not_potable_probability":
                float(not_potable_probability),

            "potable_probability":
                float(potable_probability)

        })


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 400


# ---------------------------------------
# Run server
# ---------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )