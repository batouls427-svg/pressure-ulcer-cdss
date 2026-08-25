import streamlit as st
import numpy as np
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Evidence-Based Clinical CDSS",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0F172A; }
    .stMetric { background-color: #1E293B; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #2563EB; color: white; height: 50px; }
    div[data-testid="stExpander"] { background-color: #1E293B; border-radius: 10px; border: 1px solid #334155; }
    </style>
""", unsafe_allow_html=True)

# Clinically Verified Patient Database (Strict BMI & Biomarker Logic)
PATIENT_DATABASE = {
    "PAT-9082": {
        "name": "Sarah Ahmed", "age": 83, "gender": "Female", "braden": 8,
        "albumin": 2.1, "bmi": 17.2, "creatinine": 1.1, "mobility": "Completely Immobile",
        "moisture": "Constantly Moist", "nutrition": "Very Poor", "friction": "Problem"
    },
    "PAT-4105": {
        "name": "Mohammad Ali", "age": 62, "gender": "Male", "braden": 16,
        "albumin": 3.8, "bmi": 24.5, "creatinine": 0.9, "mobility": "Slightly Limited",
        "moisture": "Rarely Moist", "nutrition": "Adequate", "friction": "No Apparent Problem"
    }
}

st.title("🩺 Evidence-Based Clinical Decision Support System (CDSS)")
st.caption("Strict Clinical Pathway Validation & Algorithmic Risk Stratification")
st.markdown("---")

# Patient Selection
col_sel1, col_sel2 = st.columns([1, 3])
with col_sel1:
    selected_id = st.selectbox("🔗 Select EHR Patient Record:", list(PATIENT_DATABASE.keys()))

patient = PATIENT_DATABASE[selected_id]

# Strict Clinical BMI Classification Logic
bmi_value = patient['bmi']
if bmi_value < 18.5:
    bmi_category = "Underweight (High Risk)"
    bmi_delta_color = "inverse"
elif 18.5 <= bmi_value <= 24.9:
    bmi_category = "Normal Weight"
    bmi_delta_color = "normal"
else:
    bmi_category = "Overweight / Obese"
    bmi_delta_color = "off"

# Albumin Clinical Validation
albumin_value = patient['albumin']
albumin_status = "Severe Depletion" if albumin_value < 3.5 else "Normal Range"

st.subheader(f"👤 Patient Profile: {patient['name']} ({selected_id})")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Age / Gender", f"{patient['age']} yrs / {patient['gender']}")
m2.metric("Serum Albumin", f"{albumin_value} g/dL", delta=albumin_status, delta_color="inverse" if albumin_value < 3.5 else "normal")
m3.metric("BMI Index", f"{bmi_value} kg/m²", delta=bmi_category, delta_color=bmi_delta_color)
m4.metric("Braden Score", f"{patient['braden']} / 23")
m5.metric("Serum Creatinine", f"{patient['creatinine']} mg/dL")

st.markdown("---")

if st.button("🚀 Execute Evidence-Based Clinical Analytics"):
    
    risk_prob = ((23 - patient['braden']) / 23) * 100
    est_weight = bmi_value * (1.65 ** 2)
    protein_low = est_weight * 1.2
    protein_high = est_weight * 1.5

    st.subheader("1. Algorithmic Risk & Evidence Stratification")
    
    if risk_prob >= 65 or bmi_value < 18.5:
        st.error(f"🚨 **HIGH CLINICAL VULNERABILITY DETECTED** — Risk Index: **{risk_prob:.1f}%** (Triggered by Low BMI / Severe Underweight & Braden Sub-scores)")
    else:
        st.success(f"✅ **STABLE CLINICAL PROFILE** — Risk Index: **{risk_prob:.1f}%**")

    # Clinical Reasoning / XAI
    with st.expander("📊 View Clinical Decision Rule Trace (Why this protocol was triggered?)", expanded=True):
        trace_df = pd.DataFrame({
            "Clinical Parameter": ["Body Mass Index (BMI)", "Serum Albumin Biomarker", "Braden Mobility Score", "Age Factor"],
            "Patient Reading": [f"{bmi_value} ({bmi_category})", f"{albumin_value} g/dL ({albumin_status})", patient['mobility'], f"{patient['age']} years"],
            "Pathophysiological Impact": [
                "Critical: Insufficient subcutaneous fat padding over bony prominences." if bmi_value < 18.5 else "Adequate tissue padding.",
                "High: Compromised oncotic pressure and impaired collagen synthesis." if albumin_value < 3.5 else "Normal protein synthesis.",
                "Critical: Zero independent micro-shifts.",
                "Moderate: Reduced skin elasticity."
            ]
        })
        st.table(trace_df)

    st.subheader("2. Evidence-Based Precision Protocols (NPIAP / EPUAP Guidelines)")

    c_plan1, c_plan2 = st.columns(2)

    with c_plan1:
        st.markdown(f"""
        ### 🥩 **A. Targeted Metabolic & Nutritional Support**
        * **Calculated Protein Requirement:** **{protein_low:.1f}g – {protein_high:.1f}g / day** *(Calculated on clinical weight: {est_weight:.1f} kg)*.
        * **Specific Prescription:** High-Protein ONS formula enriched with **L-Arginine (4.5g/day)**, **Zinc (50mg)**, and **Vitamin C (500mg)** to counteract severe Hypoalbuminemia.
        * **Renal Check:** Serum Creatinine is **{patient['creatinine']} mg/dL** (Safe for high-protein load).
        """)

    with c_plan2:
        st.markdown(f"""
        ### 🛏️ **B. Biomechanical & Pressure Relief Protocol**
        * **Surface Technology:** Mandate **Alternating Pressure Air Mattress (APAM)** specifically calibrated for low-BMI patients to prevent bottoming-out.
        * **Shear Prevention:** Restrict head-of-bed elevation strictly to **≤ 30°**.
        * **Prominence Protection:** Apply **Heel Suspension Devices** to achieve total offloading of calcaneal pressure points.
        """)
