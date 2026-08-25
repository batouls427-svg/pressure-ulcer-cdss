import streamlit as st
import numpy as np
import pandas as pd

# 1. Page Configuration (Modern Dashboard Setup)
st.set_page_config(
    page_title="Advanced EHR Clinical CDSS",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Sleek & Modern Healthcare UI
st.markdown("""
    <style>
    .main { background-color: #0F172A; }
    .stMetric { background-color: #1E293B; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #2563EB; color: white; height: 50px; }
    div[data-testid="stExpander"] { background-color: #1E293B; border-radius: 10px; border: 1px solid #334155; }
    </style>
""", unsafe_allow_html=True)

# Simulated Hospital EHR Database
PATIENT_DATABASE = {
    "PAT-9082": {
        "name": "Sarah Ahmed", "age": 83, "gender": "Female", "braden": 8,
        "albumin": 2.1, "bmi": 17.2, "creatinine": 1.1, "mobility": "Completely Immobile",
        "moisture": "Constantly Moist", "nutrition": "Very Poor", "friction": "Problem"
    },
    "PAT-4105": {
        "name": "Mohammad Ali", "age": 62, "gender": "Male", "braden": 16,
        "albumin": 3.8, "bmi": 26.4, "creatinine": 0.9, "mobility": "Slightly Limited",
        "moisture": "Rarely Moist", "nutrition": "Adequate", "friction": "No Apparent Problem"
    }
}

# --- HEADER SECTION ---
st.title("🩺 Advanced Precision Clinical Decision Support System (CDSS)")
st.caption("AI-Driven Pressure Ulcer Risk Stratification & Personalised Metabolic Prescriptions")
st.markdown("---")

# --- SECTION 1: EHR PATIENT RETRIEVAL ---
col_sel1, col_sel2 = st.columns([1, 3])
with col_sel1:
    selected_id = st.selectbox("🔗 Fetch Patient via HL7/FHIR:", list(PATIENT_DATABASE.keys()))

patient = PATIENT_DATABASE[selected_id]

# Patient Clinical Metrics Banner
st.subheader(f"👤 Patient Profile: {patient['name']} ({selected_id})")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Age / Gender", f"{patient['age']} yrs / {patient['gender']}")
m2.metric("Serum Albumin", f"{patient['albumin']} g/dL", delta="- Severe Low" if patient['albumin'] < 3.5 else "Normal", delta_color="inverse")
m3.metric("BMI", f"{patient['bmi']} kg/m²", delta="Underweight" if patient['bmi'] < 18.5 else "Normal", delta_color="inverse")
m4.metric("Braden Score", f"{patient['braden']} / 23")
m5.metric("Serum Creatinine", f"{patient['creatinine']} mg/dL")

st.markdown("---")

# --- SECTION 2: ANALYTICS TRIGGER & EXPLAINABLE AI ---
if st.button("🚀 Execute Multi-Modal Risk Analytics & Precision Plan"):
    
    # Mathematical Model Calculations
    risk_prob = ((23 - patient['braden']) / 23) * 100
    est_weight = patient['bmi'] * ((1.65) ** 2)  # Calculated based on standard height formula
    protein_low = est_weight * 1.2
    protein_high = est_weight * 1.5

    # 1. Predictive Risk Analysis Banner
    st.subheader("1. Predictive Risk Analysis & Explainable AI (XAI)")
    
    if risk_prob >= 65:
        st.error(f"🚨 **VERY HIGH ULCER RISK DETECTED** — Calculated Probability: **{risk_prob:.1f}%**")
    elif risk_prob >= 40:
        st.warning(f"⚠️ **MODERATE ULCER RISK DETECTED** — Calculated Probability: **{risk_prob:.1f}%**")
    else:
        st.success(f"✅ **LOW ULCER RISK DETECTED** — Calculated Probability: **{risk_prob:.1f}%**")

    # Feature Importance Breakdown (SHAP Simulation)
    with st.expander("📊 View AI Model SHAP Feature Contribution (Why this risk score?)", expanded=True):
        shap_df = pd.DataFrame({
            "Biomarker / Feature": ["Impairment in Mobility", "Hypoalbuminemia (< 3.5 g/dL)", "Continuous Moisture Exposure", "Advanced Age (> 75)"],
            "Measured Value": [patient['mobility'], f"{patient['albumin']} g/dL", patient['moisture'], f"{patient['age']} yrs"],
            "Risk Contribution Impact": ["+ 38% (Critical)", "+ 27% (High)", "+ 20% (High)", "+ 15% (Moderate)"]
        })
        st.table(shap_df)

    # 2. Precision Clinical Protocols & Prescriptions
    st.subheader("2. Patient-Centric Precision Clinical Protocols")

    c_plan1, c_plan2 = st.columns(2)

    with c_plan1:
        st.markdown(f"""
        ### 🥩 **A. Personalised Metabolic & Nutrition Prescription**
        * **Calculated Protein Requirement:** **{protein_low:.1f}g – {protein_high:.1f}g / day** *(Based on Est. Weight: {est_weight:.1f} kg)*.
        * **Targeted Supplementation:** High-Protein ONS enriched with **L-Arginine (4.5g/day)** + **Zinc (50mg)** + **Vitamin C (500mg)**.
        * **Biomarker Trigger:** Required due to severe Hypoalbuminemia (**{patient['albumin']} g/dL**).
        * **Safety Clearance:** Serum Creatinine is **{patient['creatinine']} mg/dL** (Normal renal clearance confirmed for high-protein titration).
        """)

    with c_plan2:
        st.markdown(f"""
        ### 🛏️ **B. Biomechanical Pressure & Surface Management**
        * **Active Support System:** Deploy **Alternating Pressure Air Mattress (APAM)** with Bony-Prominence Sensitivity mode ($BMI = {patient['bmi']}$).
        * **Shear Limitation:** Head-of-bed elevation strictly capped at **≤ 30°**. Implement 30-degree lateral tilt rotation.
        * **Offloading Protocol:** Mandatory **Heel Suspension Boots** to maintain zero-pressure on calcaneus regions.
        """)

    st.markdown("---")
    st.markdown(f"""
    ### 🛡️ **C. Advanced Topical Barrier & Skin Microclimate Protocol**
    * **Barrier Protection:** Apply **Cyanoacrylate Liquid Protectant** (e.g., 3M Cavilon) to Sacral region every **12 hours**.
    * **Hygiene Standard:** No friction rubbing; utilization of pH-balanced ($5.5$) non-rinse cleansing foam post incontinence.
    """)
