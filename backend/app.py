from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import joblib
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Project directories
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
FRONTEND_DIR = BASE_DIR / "frontend"

# Load model files
model = joblib.load(MODEL_DIR / "water_model.pkl")
imputer = joblib.load(MODEL_DIR / "imputer.pkl")
scaler = joblib.load(MODEL_DIR / "scaler.pkl")

print("All model files loaded successfully!")


# -----------------------------
# FRONTEND
# -----------------------------

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def frontend_files(path):
    return send_from_directory(FRONTEND_DIR, path)


# -----------------------------
# API
# -----------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        new_data = pd.DataFrame({
            "ph": [float(data["ph"])],
            "Hardness": [float(data["Hardness"])],
            "Solids": [float(data["Solids"])],
            "Chloramines": [float(data["Chloramines"])],
            "Sulfate": [float(data["Sulfate"])],
            "Conductivity": [float(data["Conductivity"])],
            "Organic_carbon": [float(data["Organic_carbon"])],
            "Trihalomethanes": [float(data["Trihalomethanes"])],
            "Turbidity": [float(data["Turbidity"])]
        })

        # Apply same preprocessing used during training
        data_imputed = imputer.transform(new_data)
        data_scaled = scaler.transform(data_imputed)

        # Prediction
        prediction = model.predict(data_scaled)[0]

        # Probability
        probability = model.predict_proba(data_scaled)[0]

        if prediction == 1:
            result = "Potable"
        else:
            result = "Not Potable"

        return jsonify({
            "prediction": result,
            "not_potable_probability": round(float(probability[0] * 100), 2),
            "potable_probability": round(float(probability[1] * 100), 2)
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)