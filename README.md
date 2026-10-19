Water Quality Prediction
An end-to-end Machine Learning web application that predicts whether a water sample is Potable or Not Potable based on nine water-quality parameters.
Live Demo
Live Website: https://water-quality-prediction-ruddy.vercel.app/
Project Overview
Water quality assessment is important for determining whether water is suitable for consumption. This project uses a Machine Learning classification model to evaluate water potability from measured physicochemical parameters.

The project covers the complete workflow:
- Data collection and understanding
- Exploratory Data Analysis (EDA)
- Data preprocessing
- Missing-value handling
- Feature scaling
- Machine Learning model training
- Model evaluation
- Model serialization
- Flask backend development
- HTML/CSS/JavaScript frontend development
- Web deployment using Vercel
Machine Learning Model
The project uses Logistic Regression as the classification algorithm.
Why Logistic Regression?
Logistic Regression is suitable because the target variable is binary:
- 0 → Not Potable
- 1 → Potable
It is also relatively simple, interpretable, and appropriate for a beginner-friendly binary classification problem.

To improve the model's ability to identify both classes, class_weight="balanced" was used during training.
Dataset
The project uses the Water Potability Dataset.

The dataset contains the following input features:
Feature	Description
pH	Acidity/alkalinity level of water
Hardness	Amount of dissolved calcium and magnesium
Solids	Total dissolved solids
Chloramines	Chloramine concentration
Sulfate	Sulfate concentration
Conductivity	Electrical conductivity
Organic Carbon	Organic carbon concentration
Trihalomethanes	Trihalomethanes concentration
Turbidity	Cloudiness of water


Target Variable
Potability
- 0 = Not Potable
- 1 = Potable
Data Preprocessing
The following preprocessing steps were used:
1. Missing values were handled using median imputation.
2. Numerical features were standardized using StandardScaler.
3. The dataset was divided into training and testing sets using an 80/20 stratified split.
4. random_state=42 was used to make the experiment reproducible.
The trained preprocessing components are stored separately:
model/
├── imputer.pkl
├── scaler.pkl
└── water_model.pkl
Model Performance
The final balanced Logistic Regression model achieved approximately:
Metric	Score
Accuracy	52.44%
Precision	41.46%
Recall	53.13%
F1 Score	46.58%


The model is intended as an educational and demonstration project. The results indicate that water potability is not perfectly separated by the available features, so the model should not be treated as a replacement for laboratory water-quality testing.
Web Application
The application has two main components.
Frontend
The frontend is developed using:
- HTML
- CSS
- JavaScript
It provides input fields for all nine water-quality parameters and displays the predicted water quality along with the predicted probabilities.
Backend
The backend is developed using:
- Python
- Flask
- Pandas
- Joblib
- Scikit-learn
The Flask API receives the user's water-quality parameters, applies the saved preprocessing pipeline, performs the prediction, and returns the result to the frontend.
Application Workflow
User enters water-quality values
              ↓
        HTML/CSS/JavaScript
              ↓
        POST /predict
              ↓
          Flask API
              ↓
        Median Imputation
              ↓
         Standard Scaling
              ↓
       Logistic Regression
              ↓
      Potable / Not Potable
              ↓
     Probability displayed
Project Structure
Water Quality Prediction/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── model/
│   ├── water_model.pkl
│   ├── imputer.pkl
│   └── scaler.pkl
│
├── main.ipynb
├── water_potability.csv
└── WQP report.pdf
Installation and Local Setup
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
2. Open the project folder
cd "Water Quality Prediction"
3. Create and activate the environment
conda create -n water-quality python=3.11
conda activate water-quality
4. Install dependencies
pip install -r requirements.txt
5. Run the Flask application
python app.py
6. Open the application
Open:
http://127.0.0.1:5000/
Example Input
You can test the application using example values such as:
Parameter	Example Value
pH	7.0
Hardness	200
Solids	20000
Chloramines	7.0
Sulfate	300
Conductivity	400
Organic Carbon	14
Trihalomethanes	70
Turbidity	4.0


These are example inputs for demonstrating the application and are not a guarantee of water safety.
API
Health Check
GET /health
Returns the API status.
Prediction
POST /predict
Example JSON request:
{
    "ph": 7.0,
    "Hardness": 200,
    "Solids": 20000,
    "Chloramines": 7.0,
    "Sulfate": 300,
    "Conductivity": 400,
    "Organic_carbon": 14,
    "Trihalomethanes": 70,
    "Turbidity": 4.0
}
Example response:
{
    "prediction": "Potable",
    "potable_probability": 54.23,
    "not_potable_probability": 45.77
}
The probability values depend on the trained model and input values.
Deployment
The web application is deployed using Vercel.

The deployed application combines the Flask backend and static frontend into a single web application.
Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Flask
- Flask-CORS
- HTML5
- CSS3
- JavaScript
- Git/GitHub
- Vercel
- Google Colab / Jupyter Notebook
Limitations
- The model is trained on a specific historical dataset.
- Model performance depends on the quality and representativeness of the dataset.
- The model does not replace professional laboratory testing.
- Real-world deployment would require validation using current, local water-quality data.
- The prediction should be considered an ML-based estimation rather than a certified water-safety decision.
Future Improvements
Possible improvements include:
- Testing additional classification algorithms
- Hyperparameter tuning
- Cross-validation
- Feature importance analysis
- Larger and more representative datasets
- Real-time sensor integration
- Database integration
- User authentication
- Prediction history
- Improved visualization and analytics
- Continuous model retraining using new data
Author
Omkar Satpute

Machine Learning / Data Science Mini Project
Disclaimer
This project is developed for educational and demonstration purposes. The prediction generated by the application should not be used as the sole basis for determining whether water is safe for human consumption. Proper laboratory testing and applicable water-quality standards should be used for real-world decisions.