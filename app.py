from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load model, threshold, and training columns
model = joblib.load("models/Random_Forest_best_model.pkl")
with open("models/best_threshold.txt", "r") as f:
    threshold = float(f.read())
train_columns = joblib.load("models/train_columns.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect form data
        user_data = {
            'CODE_GENDER': request.form["CODE_GENDER"].strip().upper(),
            'FLAG_OWN_CAR': request.form["FLAG_OWN_CAR"].strip().upper(),
            'FLAG_OWN_REALTY': request.form["FLAG_OWN_REALTY"].strip().upper(),
            'CNT_CHILDREN': int(request.form["CNT_CHILDREN"]),
            'AMT_INCOME_TOTAL': float(request.form["AMT_INCOME_TOTAL"]),
            'NAME_INCOME_TYPE': request.form["NAME_INCOME_TYPE"].strip(),
            'NAME_EDUCATION_TYPE': request.form["NAME_EDUCATION_TYPE"].strip(),
            'NAME_FAMILY_STATUS': request.form["NAME_FAMILY_STATUS"].strip(),
            'NAME_HOUSING_TYPE': request.form["NAME_HOUSING_TYPE"].strip(),
            'DAYS_BIRTH': int(request.form["DAYS_BIRTH"]),
            'DAYS_EMPLOYED': int(request.form["DAYS_EMPLOYED"]),
            'FLAG_WORK_PHONE': int(request.form["FLAG_WORK_PHONE"]),
            'FLAG_PHONE': int(request.form["FLAG_PHONE"]),
            'FLAG_EMAIL': int(request.form["FLAG_EMAIL"]),
            'CNT_FAM_MEMBERS': float(request.form["CNT_FAM_MEMBERS"]),
        }

        # Convert to DataFrame and preprocess
        user_df = pd.DataFrame([user_data])
        user_encoded = pd.get_dummies(user_df)

        for col in train_columns:
            if col not in user_encoded.columns:
                user_encoded[col] = 0

        user_encoded = user_encoded[train_columns]

        # Predict
        proba = model.predict_proba(user_encoded)[:, 1][0]
        prediction = int(proba >= threshold)

        result_text = "GOOD CREDIT RISK — Eligible for Credit Card" if prediction == 0 else "BAD CREDIT RISK — Not Eligible for Credit Card"

        return render_template("index.html", probability=round(proba, 4), result=result_text)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
