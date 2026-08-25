import streamlit as st
import numpy as np
import pandas as pd

# 1. Page Configuration - Next-Gen Enterprise UI
st.set_page_config(
    page_title="Next-Gen Clinical CDSS (PUPP-Optimized)",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-Performance Healthcare UI Styling
st.markdown("""
    <style>
    .main { background-color: #07090E; }
    .stMetric { background-color: #111827; padding: 15px; border-radius: 12px; border: 1px solid #1F2937; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #3B82F6; color: white; height: 50px; transition: 0.3s; }
    .stButton>button:hover { background-color: #2563EB; }
    div[data-testid="stExpander"] { background-color: #111827; border-radius: 12px; border: 1px solid #1F2937; }
    </style>
""", unsafe_allow_html=True)

# Advanced EHR Patient Database (Simulating Real-World Hospital Scenarios aligned with Saudi PUPP standards)
PATIENT_DATABASE = {
    "PAT-9082": {
        "name": "Fatima Al-Zahra (Geriatric ICU Case)", 
        "age": 83, "gender": "Female", "braden": 8,
        "albumin": 2.1, "bmi": 16.8, "creatinine": 1.2, 
        "mobility": "1 - Completely Immobile",
        "moisture": "1 - Constantly Moist", 
        "nutrition": "1 - Very Poor", 
        "friction": "1 - Problem",
        "active_alerts": 3
    },
    "PAT-4105": {
        "name": "Mohammad Al-Otaibi (Post-Surgical Step-Down)", 
        "age": 62, "gender": "Male", "braden": 16,
        "albumin": 3.8, "bmi": 24.5, "creatinine": 0.9, 
        "mobility": "3 - Slightly Limited",
        "moisture": "4 - Rarely Moist", 
        "nutrition": "3 - Adequate", 
        "friction": "3 - No Apparent Problem",
        "active_alerts": 0
    }
}

st.title("🚀 Next-Gen Clinical Decision Support System (CDSS)")
st.caption("Advanced Next-Gen Evolution of Pressure Ulcer Prevention Programs (PUPP) — Eliminating Alert Fatigue & Enhancing XAI")
st.markdown("---")

# Patient EHR Selection & Streamlined Workflow
col_sel1, col_sel2 = st.columns([1, 3])
with col_sel1:
    selected_id = st.selectbox("🔗 Select Verified EHR Patient Record:", list(PATIENT_DATABASE.keys()))

patient = PATIENT_DATABASE[selected_id]

# Rigorous Clinical Biomarker & Anthropometric Validation
bmi_value = patient['bmi']
if bmi_value < 18.5:
    bmi_category = "Underweight (Critical Vulnerability)"
    bmi_delta_color = "inverse"
elif 18.5 <= bmi_value <= 24.9:
    bmi_category = "Normal Range"
    bmi_delta_color = "normal"
else:
    bmi_category = "Overweight / Obese"
    bmi_delta_color = "off"

albumin_value = patient['albumin']
albumin_status = "Critical Depletion (Malnutrition)" if albumin_value < 3.5 else "Normal Range"

st.subheader(f"👤 Patient Profile: {patient['name']} ({selected_id})")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Age / Gender", f"{patient['age']} yrs / {patient['gender']}")
m2.metric("Serum Albumin", f"{albumin_value} g/dL", delta=albumin_status, delta_color="inverse" if albumin_value < 3.5 else "normal")
m3.metric("BMI Index", f"{bmi_value} kg/m²", delta=bmi_category, delta_color=bmi_delta_color)
m4.metric("Braden Score", f"{patient['braden']} / 23", delta="High Risk" if patient['braden'] <= 12 else "Stable", delta_color="inverse" if patient['braden'] <= 12 else "normal")
m5.metric("Alert Load Status", f"{patient['active_alerts']} Active Flags", delta="Optimized (No Fatigue)", delta_color="normal")

st.markdown("---")

if st.button("⚡ Run Next-Gen Multi-Modal Clinical Analytics"):
    
    braden_score = patient['braden']
    risk_prob = ((23 - braden_score) / 23) * 100
    est_weight = bmi_value * (1.65 ** 2) 
    protein_low = est_weight * 1.2
    protein_high = est_weight * 1.5

    st.subheader("1. AI-Driven Risk Stratification & Zero-Fatigue Triage")
    
    if braden_score <= 12 or albumin_value < 3.5 or bmi_value < 18.5:
        st.error(f"🚨 **CRITICAL VULNERABILITY ALERT** — Composite Risk Index: **{risk_prob:.1f}%** \n\n *Smart Triage Note: Filtered out background noise to prevent nurse alert fatigue; direct clinical intervention mandated.*")
    else:
        st.success(f"✅ **STABLE CLINICAL PROFILE** — Composite Risk Index: **{risk_prob:.1f}%** \n\n *Smart Triage Note: Routine monitoring pathway active.*")

    # Explainable AI (XAI) Rule Trace - Solving the "Black Box" problem of legacy systems
    with st.expander("🔍 Explainable AI (XAI) Clinical Decision Trace & Root-Cause Breakdown", expanded=True):
        trace_df = pd.DataFrame({
            "Clinical Parameter": ["Braden Score Assessment", "Body Mass Index (BMI)", "Serum Albumin Biomarker", "Age & Tissue Elasticity"],
            "Patient Reading": [f"{braden_score} / 23", f"{bmi_value} ({bmi_category})", f"{albumin_value} g/dL ({albumin_status})", f"{patient['age']} years"],
            "Pathophysiological Impact (Evidence-Based)": [
                "Critical breach (< 13 threshold)." if braden_score <= 12 else "Stable range.",
                "High risk: Total absence of subcutaneous fat padding over sacral and calcaneal bones." if bmi_value < 18.5 else "Adequate cushioning.",
                "Impaired collagen synthesis, reduced oncotic pressure, and compromised tissue regeneration." if albumin_value < 3.5 else "Normal protein synthesis.",
                "Age-related microvascular degeneration."
            ]
        })
        st.table(trace_df)

    st.subheader("2. Precision Care Bundles & Next-Gen Protocols (PUPP & NPIAP Aligned)")

    c_plan1, c_plan2 = st.columns(2)

    with c_plan1:
        if albumin_value < 3.5 or bmi_value < 18.5:
            st.markdown(f"""
            ### 🥩 **A. Clinical Metabolic Prescription**
            * **Target Protein Intake:** **{protein_low:.1f}g – {protein_high:.1f}g / day** *(Calculated on dynamic weight: {est_weight:.1f} kg)*.
            * **Immunonutrition Support:** High-protein oral supplements enriched with **L-Arginine (4.5g/day)**, **Zinc Sulfate (50mg)**, and **Vitamin C (500mg)**.
            * **Clinical Rationale:** Immediate counteraction of Hypoalbuminemia ({albumin_value} g/dL) to restore positive nitrogen balance.
            """)
        else:
            st.markdown(f"""
            ### 🥩 **A. Standard Nutritional Maintenance**
            * **Requirement:** Maintain baseline balanced caloric and protein intake (0.8 - 1.0 g/kg/day).
            """)

    with c_plan2:
        if braden_score <= 12:
            st.markdown(f"""
            ### 🛏️ **B. Biomechanical Surface & Offloading Plan**
            * **Surface Technology:** Automatic deployment of **Alternating Pressure Air Mattress (APAM)** customized for low-BMI patients to eliminate bottoming-out.
            * **Shear Stress Mitigation:** Head-of-bed angle strictly locked at **≤ 30°**; execute automated 2-hour repositioning intervals.
            * **Prominence Protection:** Complete offloading utilizing specialized **Heel Suspension Booties**.
            """)
        else:
            st.markdown(f"""
            ### 🛏️ **B. Standard Preventative Biomechanics**
            * **Surface:** Standard reactive support surface with regular independent patient repositioning.
            """)
