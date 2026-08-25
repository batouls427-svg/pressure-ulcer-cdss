import os
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# ==========================================
# 1. Model Training / Loading Logic
# ==========================================
MODEL_FILE = 'pressure_ulcer_model.pkl'

def train_and_save_model():
    np.random.seed(42)
    n_samples = 1000
    
    mobility = np.random.choice([1, 2, 3, 4], size=n_samples)
    nutrition = np.random.choice([1, 2, 3, 4], size=n_samples)
    moisture = np.random.choice([1, 2, 3, 4], size=n_samples)
    friction = np.random.choice([1, 2, 3], size=n_samples)
    age = np.random.randint(18, 95, size=n_samples)
    
    # Advanced risk weighting
    braden_score = mobility + nutrition + moisture + friction
    risk = np.where((braden_score <= 10) | ((age > 75) & (braden_score <= 12)), 1, 0)
    
    df = pd.DataFrame({
        'mobility': mobility,
        'nutrition': nutrition,
        'moisture': moisture,
        'friction': friction,
        'age': age,
        'risk': risk
    })
    
    X = df[['mobility', 'nutrition', 'moisture', 'friction', 'age']]
    y = df['risk']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, MODEL_FILE)
    return model

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_FILE):
        return train_and_save_model()
    return joblib.load(MODEL_FILE)

model = load_model()

# ==========================================
# 2. Streamlit CDSS User Interface
# ==========================================
st.set_page_config(
    page_title="Advanced Clinical CDSS - Pressure Ulcer",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Clinical Decision Support System (CDSS)")
st.caption("Evidence-Based Pressure Ulcer Risk Assessment & Personalised Care Protocol")

st.sidebar.header("Patient Assessment Parameters")

age = st.sidebar.slider("Age (Years)", 18, 100, 83)
mobility = st.sidebar.selectbox("Mobility", options=[1, 2, 3, 4], 
                                format_func=lambda x: {1: "1 - Completely Immobile", 2: "2 - Very Limited", 3: "3 - Slightly Limited", 4: "4 - No Limitation"}[x])
nutrition = st.sidebar.selectbox("Nutritional Intake", options=[1, 2, 3, 4], 
                                 format_func=lambda x: {1: "1 - Very Poor", 2: "2 - Probably Inadequate", 3: "3 - Adequate", 4: "4 - Excellent"}[x])
moisture = st.sidebar.selectbox("Moisture Exposure", options=[1, 2, 3, 4], 
                                format_func=lambda x: {1: "1 - Constantly Moist", 2: "2 - Very Moist", 3: "3 - Occasionally Moist", 4: "4 - Rarely Moist"}[x])
friction = st.sidebar.selectbox("Friction & Shear", options=[1, 2, 3], 
                                format_func=lambda x: {1: "1 - Problem", 2: "2 - Potential Problem", 3: "3 - No Apparent Problem"}[x])

# Braden Sub-score calculation
braden_subscore = mobility + nutrition + moisture + friction

# Layout
col_sum1, col_sum2, col_sum3 = st.columns(3)
col_sum1.metric("Patient Age", f"{age} yrs")
col_sum2.metric("Braden Partial Score", f"{braden_subscore} / 15")
col_sum3.metric("ML Model Status", "Active (Random Forest)")

st.markdown("---")

if st.button("Generate Personalised Clinical Plan", type="primary"):
    input_data = np.array([[mobility, nutrition, moisture, friction, age]])
    probability = model.predict_proba(input_data)[0][1] * 100

    # Risk Stratification
    if braden_subscore <= 6 or probability >= 75:
        risk_level = "VERY HIGH RISK"
        risk_color = "error"
    elif braden_subscore <= 9 or probability >= 50:
        risk_level = "HIGH RISK"
        risk_color = "warning"
    else:
        risk_level = "LOW / MODERATE RISK"
        risk_color = "success"

    st.subheader("1. Predictive Risk Analysis")
    if risk_color == "error":
        st.error(f"🚨 **{risk_level}** — Model Risk Probability: **{probability:.1f}%**")
    elif risk_color == "warning":
        st.warning(f"⚠️ **{risk_level}** — Model Risk Probability: **{probability:.1f}%**")
    else:
        st.success(f"✅ **{risk_level}** — Model Risk Probability: **{probability:.1f}%**")

    st.subheader("2. Targeted Clinical Interventions (NPIAP Aligned)")
    
    interventions = []
    
    # Specific Mobility Protocol
    if mobility in [1, 2]:
        interventions.append("**Support Surface:** Escalate immediately to an **Alternating Pressure Air Mattress (APAM)** or high-specification reactive foam mattress.")
        interventions.append("**Positioning Protocol:** Limit head-of-bed elevation to **≤ 30 degrees** to reduce shear forces on the sacrum. Utilize 30-degree tilted side-lying positions.")
    
    # Specific Moisture Protocol
    if moisture in [1, 2]:
        interventions.append("**Barrier Protection:** Apply a **dimethicone or cyanoacrylate-based skin protectant barrier** after each cleansing episode.")
        interventions.append("**Incontinence Management:** Implement a structured skin cleansing regime; evaluate for fecal/urinary management devices if moisture is uncontrollable.")
        
    # Specific Nutrition Protocol
    if nutrition in [1, 2]:
        interventions.append("**Nutritional Consultation:** Urgent referral to Clinical Dietitian. Initiate high-protein oral nutritional supplements (ONS) enriched with **Arginine, Zinc, and Vitamin C**.")

    # High Age Consideration
    if age >= 75:
        interventions.append("**Fragile Skin Protocol:** Avoid manual sliding during transfers; mandatory use of slide sheets or mechanical patient lifts.")

    if interventions:
        for item in interventions:
            st.write(f"- {item}")
    else:
        st.write("- Maintain standard nursing care, routine shift skin evaluations, and encourage mobilization as tolerated.")
