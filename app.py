from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import joblib
from pathlib import Path


# ============================================================
# Flask Application
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# Project Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "model"
FRONTEND_DIR = BASE_DIR / "frontend"


# ============================================================
# Load Machine Learning Files
# ============================================================

try:

    model = joblib.load(MODEL_DIR / "water_model.pkl")
    imputer = joblib.load(MODEL_DIR / "imputer.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")

    print("All model files loaded successfully!")

except Exception as e:

    print("Error loading model files:")
    print(e)


# ============================================================
# Home Page
# ============================================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ============================================================
# Prediction API
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        # ----------------------------------------------------
        # Create DataFrame
        # ----------------------------------------------------

        new_data = pd.DataFrame({

            "ph": [
                float(data["ph"])
            ],

            "Hardness": [
                float(data["Hardness"])
            ],

            "Solids": [
                float(data["Solids"])
            ],

            "Chloramines": [
                float(data["Chloramines"])
            ],

            "Sulfate": [
                float(data["Sulfate"])
            ],

            "Conductivity": [
                float(data["Conductivity"])
            ],

            "Organic_carbon": [
                float(data["Organic_carbon"])
            ],

            "Trihalomethanes": [
                float(data["Trihalomethanes"])
            ],

            "Turbidity": [
                float(data["Turbidity"])
            ]

        })


        # ----------------------------------------------------
        # Preprocessing
        # ----------------------------------------------------

        data_imputed = imputer.transform(new_data)

        data_scaled = scaler.transform(data_imputed)


        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = model.predict(data_scaled)[0]

        probability = model.predict_proba(data_scaled)[0]


        # ----------------------------------------------------
        # Convert Prediction
        # ----------------------------------------------------

        if prediction == 1:

            result = "Potable"

        else:

            result = "Not Potable"


        # ----------------------------------------------------
        # Send Response
        # ----------------------------------------------------

        return jsonify({

            "prediction": result,

            "potable_probability": round(
                float(probability[1] * 100),
                2
            ),

            "not_potable_probability": round(
                float(probability[0] * 100),
                2
            )

        })


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# ============================================================
# Health Check
# ============================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "success",

        "message": "Water Quality Prediction API is running"

    })


# ============================================================
# Frontend Static Files
# ============================================================

@app.route("/<path:path>")
def frontend_files(path):

    return send_from_directory(
        FRONTEND_DIR,
        path
    )


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )