from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import joblib

# =========================
# Load resources once
# =========================
print("🔄 Loading data and models...")

df = pd.read_csv("dataset/Final_Augmented_dataset_Diseases_and_Symptoms.csv")
symptoms_en = list(df.columns)
symptoms_en.remove("diseases")

translations_df = pd.read_csv("dataset/symptoms_translatedd.csv", on_bad_lines='skip')
translations_df.columns = translations_df.columns.str.strip()
translations_df["symptom_en"] = translations_df["symptom_en"].astype(str).str.strip()
translations_df["symptom_arabic"] = translations_df["symptom_arabic"].astype(str).str.strip()

arabic_to_english = dict(zip(
    translations_df["symptom_arabic"],
    translations_df["symptom_en"]
))

disease_df = pd.read_csv("dataset/diseaseArabic.csv")
disease_en_to_ar = dict(zip(
    disease_df["disease_en"].str.strip(),
    disease_df["disease_ar"].str.strip()
))

rf_model = joblib.load("models\disease_prediction_pipeline.pkl")
label_encoder = joblib.load("models\label_encoder.pkl")

print("✅ Models loaded successfully")

# =========================
# Flask App
# =========================
app = Flask(__name__)

# =========================
# Health Check
# =========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "Disease Diagnosis API is running 🚀"
    })

# =========================
# Prediction Endpoint
# =========================
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data or "symptoms" not in data:
        return jsonify({"error": "Please provide symptoms list"}), 400

    symptoms_ar = data["symptoms"]
    symptoms_en_input = []

    for s in symptoms_ar:
        if s in arabic_to_english:
            symptoms_en_input.append(arabic_to_english[s])

    if len(symptoms_en_input) == 0:
        return jsonify({"error": "No valid symptoms provided"}), 400

    # Build input vector
    input_vector = np.zeros(len(symptoms_en))

    for symptom in symptoms_en_input:
        if symptom in symptoms_en:
            idx = symptoms_en.index(symptom)
            input_vector[idx] = 1

    input_vector = input_vector.reshape(1, -1)

    # Predict probabilities
    probs = rf_model.predict_proba(input_vector)[0]
    top5_idx = np.argsort(probs)[::-1][:5]

    results = []

    for rank, idx in enumerate(top5_idx, start=1):
        prob = float(probs[idx])
        disease_label = idx

        disease_en = label_encoder.inverse_transform([disease_label])[0]
        disease_ar = disease_en_to_ar.get(disease_en, disease_en)

        results.append({
            "rank": rank,
            "disease": disease_ar,
            "confidence": round(prob * 100, 2)
        })

    return jsonify({
        "input_symptoms": symptoms_ar,
        "top_predictions": results
    })


# =========================
# Run Server
# =========================
if __name__ == "__main__":
    app.run(debug=True)
