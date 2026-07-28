import os
import json
import pandas as pd
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS to allow your Vue frontend (e.g., localhost:5173) to hit this API
CORS(app)

# ---------------------------------------------------------
# 1. Load the Machine Learning Artifacts
# ---------------------------------------------------------
# Determine the absolute path to the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    print("Loading the Oracle's logic...")
    rf_model = joblib.load(os.path.join(BASE_DIR, 'best_rf_headache_model.pkl'))
    label_encoder = joblib.load(os.path.join(BASE_DIR, 'label_encoder.pkl'))
    
    with open(os.path.join(BASE_DIR, 'model_columns.json'), 'r') as f:
        model_columns = json.load(f)
        
    print("All ML components loaded successfully.")
except Exception as e:
    print(f"Error loading models. Ensure the .pkl and .json files are in {BASE_DIR}")
    print(e)

# ---------------------------------------------------------
# 2. Define the Prediction Endpoint
# ---------------------------------------------------------
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # 1. Parse the incoming JSON payload from Vue
        # Format expected: { "Pain_Type": ["Dull/Aching"], "Onset_Speed": ["Gradual"], ... }
        symptoms_json = request.get_json()
        
        if not symptoms_json:
            return jsonify({'error': 'No data provided'}), 400

        # 2. Convert to a Pandas DataFrame
        user_df = pd.DataFrame(symptoms_json)

        # 3. One-Hot Encode the user's input
        user_encoded = pd.get_dummies(user_df)

        # 4. Align columns perfectly with the training data
        # Any symptom combination the user didn't select gets filled with a 0
        user_aligned = user_encoded.reindex(columns=model_columns, fill_value=0)
        
        # Ensure datatypes are strictly integers (0 and 1) for the Random Forest
        user_aligned = user_aligned.astype(int)

        # 5. Make the Prediction
        predicted_class_int = rf_model.predict(user_aligned)

        # 6. Translate the integer back to the human-readable headache type
        predicted_headache = label_encoder.inverse_transform(predicted_class_int)

        # 7. Return the result to the frontend
        return jsonify({
            'prediction': predicted_headache[0]
        }), 200

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500

# ---------------------------------------------------------
# 3. Server Execution
# ---------------------------------------------------------
if __name__ == '__main__':
    # Run the server on port 5000 
    app.run(host='0.0.0.0', port=5000, debug=True)