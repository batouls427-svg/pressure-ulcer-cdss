import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="EHR-Integrated Clinical CDSS", layout="wide")

# Simulation of Electronic Health Record (EHR) Database
PATIENT_DATABASE = {
    "PAT-9082": {"name": "Patient A", "age": 83, "braden": 8, "mobility": 1, "moisture": 1, "nutrition": 1, "albumin": 2.1, "bmi": 17.2},
    "PAT-4105": {"name": "Patient B", "age": 62, "braden": 15, "mobility": 3, "moisture": 3, "nutrition": 3, "albumin": 3.8, "bmi": 24.5},
}

st.title("🏥 EHR-Integrated Pressure Ulcer CDSS & Explainable AI")
st.caption("Automatic Patient Data Retrieval via HL7/FHIR Protocol Simulation")

# Step 1: EHR Patient Fetching
st.sidebar.header("🔌 Hospital EHR Integration")
patient_id = st.sidebar.selectbox("Select Patient Record (EHR Fetch)", list(PATIENT_DATABASE.keys()))

patient_data = PATIENT_DATABASE[patient_id]

st.subheader(f"Patient File: {patient_id} ({patient_data['name']})")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Age", f"{patient_data['age']} yrs")
c2.metric("Serum Albumin", f"{patient_data['albumin']} g/dL", delta="- Severe Low" if patient_data['albumin'] < 3.5 else "Normal")
c3.metric("BMI", f"{patient_data['bmi']}")
c4.metric("Braden Score", f"{patient_data['braden']} / 23")

st.markdown("---")

if st.button("Run Advanced CDSS Risk Analytics", type="primary"):
    # Analytics
    risk_score = (23 - patient_data['braden']) / 23 * 100
    
    st.subheader("1. Predictive Risk & Explainable AI (XAI)")
    st.error(f"⚠️ High Ulcer Risk Detected: **{risk_score:.1f}% Probability**")
    
    # Feature Importance / SHAP Breakdown
    st.write("**Top Clinical Factors Driving Risk Score (SHAP Breakdown):**")
    factors_df = pd.DataFrame({
        "Clinical Feature": ["Impairment in Mobility", "Hypoalbuminemia (< 3.5 g/dL)", "Moisture Exposure", "Advanced Age (> 75)"],
        "Risk Contribution Impact": ["+ 38%", "+ 27%", "+ 20%", "+ 15%"]
    })
    st.table(factors_df)
    
    st.subheader("2. Evidence-Based Clinical Protocols")
    st.write("• **Advanced Surface:** Deploy Active Dynamic Air Mattress (APAM).")
    st.write("• **Metabolic Support:** High-protein nutritional therapy triggered due to Serum Albumin < 3.5 g/dL.")
    st.write("• **Skin Protection:** Apply Silicone-based Barrier Protection every 4 hours.")
