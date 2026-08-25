import os
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# ==========================================
# 1. Model Training / Loading Logic
# ==========================================
MODEL_FILE = 'pressure_ulcer_model.pkl'

def train_and_save_model():
    # generate dummy clinical dataset if not training dynamically
    np.random.seed(42)
    n_samples = 500
    
    mobility = np.random.choice([1, 2, 3, 4], size=n_samples)
    nutrition = np.random.choice([1, 2, 3, 4], size=n_samples)
    moisture = np.random.choice([1, 2, 3, 4], size=n_samples)
    friction = np.random.choice([1, 2, 3], size=n_samples)
    age = np.random.randint(18, 90, size=n_samples)
    
    # Calculate synthetic risk target based on Braden-like score logic
    braden_score = mobility + nutrition + moisture + friction
    risk = (braden_score <= 8).astype(int)
    
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

# Load the trained model
model = load_model()

# ==========================================
# 2. Streamlit CDSS User Interface
# ==========================================
st.set_page_config(
    page_title="Pressure Ulcer CDSS",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Pressure Ulcer Risk Assessment CDSS")
st.markdown("Clinical Decision Support System for Pressure Ulcer Risk Prediction & Prevention Guidelines.")

st.sidebar.header("Patient Clinical Parameters")

age = st.sidebar.slider("Patient Age", 18, 100, 65)
mobility = st.sidebar.selectbox("Mobility Level", options=[1, 2, 3, 4], 
                                format_func=lambda x: {1: "1 - Completely Immobile", 2: "2 - Very Limited", 3: "3 - Slightly Limited", 4: "4 - No Limitation"}[x])
nutrition = st.sidebar.selectbox("Nutrition Status", options=[1, 2, 3, 4], 
                                 format_func=lambda x: {1: "1 - Very Poor", 2: "2 - Probably Inadequate", 3: "3 - Adequate", 4: "4 - Excellent"}[x])
moisture = st.sidebar.selectbox("Moisture Exposure", options=[1, 2, 3, 4], 
                                format_func=lambda x: {1: "1 - Constantly Moist", 2: "2 - Very Moist", 3: "3 - Occasionally Moist", 4: "4 - Rarely Moist"}[x])
friction = st.sidebar.selectbox("Friction & Shear", options=[1, 2, 3], 
                                format_func=lambda x: {1: "1 - Problem", 2: "2 - Potential Problem", 3: "3 - No Apparent Problem"}[x])

st.subheader("Patient Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Age", f"{age} yrs")
col2.metric("Mobility Rating", f"{mobility}/4")
col3.metric("Nutrition Rating", f"{nutrition}/4")

if st.button("Predict Pressure Ulcer Risk", type="primary"):
    input_data = np.array([[mobility, nutrition, moisture, friction, age]])
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1] * 100

    st.markdown("---")
    st.subheader("Clinical Risk Assessment Result")

    if prediction == 1 or probability >= 50:
        st.error(f"⚠️ **HIGH RISK DETECTED** (Calculated Risk Probability: {probability:.1f}%)")
        st.markdown("### 📋 Recommended Preventive Clinical Care Plan:")
        st.write("- **Repositioning:** Turn patient every 2 hours minimum.")
        st.write("- **Surface Management:** Use pressure-relieving foam/air mattress.")
        st.write("- **Moisture Control:** Apply barrier cream and schedule frequent skin assessments.")
        st.write("- **Nutrition Consultation:** Request high-protein dietary review.")
    else:
        st.content = st.success(f"✅ **LOW / MODERATE RISK** (Calculated Risk Probability: {probability:.1f}%)")
        st.markdown("### 📋 Recommended Clinical Guidelines:")
        st.write("- Continue routine skin evaluation every shift.")
        st.write("- Maintain adequate hydration and skin hygiene.")
        st.write("- Encourage early mobility as tolerated.")
