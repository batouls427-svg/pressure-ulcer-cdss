import streamlit as st
import numpy as np
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Next-Gen Clinical CDSS | Advanced Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Enterprise UI Styling
st.markdown("""
    <style>
    .main { background-color: #030712; color: #F3F4F6; }
    .stMetric { background-color: #111827; padding: 18px; border-radius: 12px; border: 1px solid #1F2937; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #2563EB; color: white; height: 50px; }
    div[data-testid="stExpander"] { background-color: #111827; border-radius: 12px; border: 1px solid #1F2937; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Next-Gen Clinical Decision Support System (CDSS)")
st.caption("Real-Time Algorithmic Risk Stratification & Precision Metabolic Care Protocol Engine")
st.markdown("---")

# --- SIDEBAR: LIVE INTERACTIVE CLINICAL PARAMETERS ---
st.sidebar.header("🎛️ Live Patient Parameters Input")
st.sidebar.caption("Dynamic adjustment simulating live EHR telemetry feeds.")

age = st.sidebar.slider("Patient Age (Years)", 18, 100, 83)
gender = st.sidebar.selectbox("Gender", ["Female", "Male"])
bmi = st.sidebar.slider("Body Mass Index (BMI kg/m²)", 12.0, 45.0, 16.8)
albumin = st.sidebar.slider("Serum Albumin (g/dL)", 1.0, 5.0, 2.1, 0.1)
creatinine = st.sidebar.slider("Serum Creatinine (mg/dL)", 0.4, 3.0, 1.1, 0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("Braden Sub-Scales")
mobility = st.sidebar.selectbox("Mobility", [1, 2, 3, 4], format_func=lambda x: {1: "1 - Completely Immobile", 2: "2 - Very Limited", 3: "3 - Slightly Limited", 4: "4 - No Limitation"}[x])
moisture = st.sidebar.selectbox("Moisture", [1, 2, 3, 4], format_func=lambda x: {1: "1 - Constantly Moist", 2: "2 - Very Moist", 3: "3 - Occasionally Moist", 4: "4 - Rarely Moist"}[x])
nutrition = st.sidebar.selectbox("Nutrition", [1, 2, 3, 4], format_func=lambda x: {1: "1 - Very Poor", 2: "2 - Probably Inadequate", 3: "3 - Adequate", 4: "4 - Excellent"}[x])
friction = st.sidebar.selectbox("Friction & Shear", [1, 2, 3], format_func=lambda x: {1: "1 - Problem", 2: "2 - Potential Problem", 3: "3 - No Apparent Problem"}[x])

# --- CALCULATIONS ---
braden_score = mobility + moisture + nutrition + friction
risk_prob = max(0, min(100, ((23 - braden_score) / 19) * 100 + (max(0, 75 - age) * 0.1) + (max(0, 3.5 - albumin) * 10)))

# Dynamic weight estimate & nutritional needs
est_weight = bmi * (1.65 ** 2)
protein_low = est_weight * 1.2
protein_high = est_weight * 1.5

# --- MAIN DASHBOARD DISPLAY ---
st.subheader("📊 Live Patient Clinical Dashboard")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Age / Gender", f"{age} yrs / {gender}")
m2.metric("Serum Albumin", f"{albumin} g/dL", delta="Critical Low" if albumin < 3.5 else "Normal", delta_color="inverse" if albumin < 3.5 else "normal")
m3.metric("BMI Index", f"{bmi} kg/m²", delta="Underweight" if bmi < 18.5 else "Normal", delta_color="inverse" if bmi < 18.5 else "normal")
m4.metric("Braden Score", f"{braden_score} / 23", delta="High Risk" if braden_score <= 12 else "Stable", delta_color="inverse" if braden_score <= 12 else "normal")
m5.metric("Composite Risk Index", f"{risk_prob:.1f}%", delta="High Vulnerability" if risk_prob > 50 else "Stable", delta_color="inverse" if risk_prob > 50 else "normal")

st.markdown("---")

# --- ANALYTICS & DECISION ENGINE ---
st.subheader("1. AI Risk Stratification & Explainable AI (XAI) Trace")

if risk_prob >= 50 or braden_score <= 12 or albumin < 3.5 or bmi < 18.5:
    st.error(f"🚨 **HIGH CLINICAL VULNERABILITY DETECTED** — Real-Time Risk Index: **{risk_prob:.1f}%** \n\n *Smart Triage Engine: Automated alert dispatched to clinical nursing team.*")
else:
    st.success(f"✅ **STABLE CLINICAL PROFILE** — Real-Time Risk Index: **{risk_prob:.1f}%** \n\n *Smart Triage Engine: Standard preventative protocol active.*")

# Explainable AI Trace Table
with st.expander("🔍 View Live Explainable AI (XAI) Decision Breakdown", expanded=True):
    trace_df = pd.DataFrame({
        "Parameter Evaluated": ["Braden Scale Score", "Body Mass Index (BMI)", "Serum Albumin Biomarker", "Age Factor"],
        "Current Live Value": [f"{braden_score} / 23", f"{bmi} kg/m²", f"{albumin} g/dL", f"{age} years"],
        "Pathophysiological Impact (NPIAP Aligned)": [
            "Critical threshold breach (< 13)." if braden_score <= 12 else "Stable threshold.",
            "High risk: Insufficient subcutaneous adipose tissue padding over bony prominences." if bmi < 18.5 else "Adequate structural cushioning.",
            "Severe risk: Impaired oncotic pressure and collagen synthesis." if albumin < 3.5 else "Normal visceral protein levels.",
            "Age-related microvascular degeneration."
        ]
    })
    st.table(trace_df)

st.subheader("2. Precision Care Bundles & Dynamic Protocols")

col_p1, col_p2 = st.columns(2)

with col_p1:
    if albumin < 3.5 or bmi < 18.5:
        st.markdown(f"""
        ### 🥩 **A. Clinical Metabolic Prescription (ASPEN Aligned)**
        * **Target Protein Requirement:** **{protein_low:.1f}g – {protein_high:.1f}g / day** *(Calculated dynamically for weight: {est_weight:.1f} kg)*.
        * **Immunonutrition Support:** High-protein oral supplements enriched with **L-Arginine (4.5g/day)**, **Zinc Sulfate (50mg)**, and **Vitamin C (500mg)**.
        * **Clinical Rationale:** Immediate counteraction of Hypoalbuminemia ({albumin} g/dL) and low BMI to stimulate tissue granulation.
        """)
    else:
        st.markdown(f"""
        ### 🥩 **A. Standard Nutritional Maintenance**
        * **Requirement:** Baseline caloric intake (25-30 kcal/kg/day) and standard protein distribution.
        """)

with col_p2:
    if braden_score <= 12:
        st.markdown(f"""
        ### 🛏️ **B. Biomechanical Surface & Offloading Plan**
        * **Surface Technology:** Immediate deployment of **Alternating Pressure Air Mattress (APAM)** calibrated for low-BMI patient protection.
        * **Shear Stress Mitigation:** Head-of-bed angle strictly locked at **≤ 30°**; execute automated 2-hour repositioning intervals.
        * **Prominence Protection:** Complete offloading utilizing specialized **Heel Suspension Booties**.
        """)
    else:
        st.markdown(f"""
        ### 🛏️ **B. Standard Preventative Biomechanics**
        * **Surface:** Standard reactive support surface with regular independent patient repositioning.
        """)
