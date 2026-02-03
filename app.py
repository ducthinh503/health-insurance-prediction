import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load models
scaler = joblib.load("models/scaler.pkl")
model = joblib.load("models/best_model.pkl")

st.set_page_config(page_title="Insurance Claim Predictor", layout="centered")
st.title("Health Insurance Payment Prediction App")
st.write("Enter the details below to estimate your insurance payment amount")

# UI Form
with st.form("input_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=0, max_value=100, value=30)
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)
        children = st.number_input("Number of Children", min_value=0, max_value=8, value=0)

    with col2:
        bloodpressure = st.number_input("Blood Pressure", min_value=60, max_value=200, value=120)

        gender_label = st.selectbox("Gender", ["Female", "Male"])
        diabetic_label = st.selectbox("Diabetic", ["No", "Yes"])
        smoker_label = st.selectbox("Smoker", ["No", "Yes"])

    submitted = st.form_submit_button("Predict Payment")

# Prediction
if submitted:
    
    # Manual Mapping
    gender = 0 if gender_label == "Female" else 1
    diabetic = 0 if diabetic_label == "No" else 1
    smoker = 0 if smoker_label == "No" else 1

    input_data = pd.DataFrame({
        "age": [age],
        "gender": [gender],
        "bmi": [bmi],
        "bloodpressure": [bloodpressure],
        "diabetic": [diabetic],
        "children": [children],
        "smoker": [smoker]
    })

    # Scale numeric features
    num_cols = ["age", "bmi", "bloodpressure", "children"]
    input_data[num_cols] = scaler.transform(input_data[num_cols])

    prediction = model.predict(input_data)[0]

    st.success(f"**Estimated Insurance Payment Amount:** ${prediction:,.2f}")
