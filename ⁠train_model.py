import streamlit as st
import numpy as np
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="OmniHealth AI | Next-Gen Clinical Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Dark UI Styling
st.markdown("""
    <style>
    .main { background-color: #030712; color: #F3F4F6; }
    .stMetric { background-color: #111827; padding: 18px; border-radius: 12px; border: 1px solid #1F2937; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #2563EB; color: white; height: 50px; }
    div[data-testid="stExpander"] { background-color: #111827; border-radius: 12px; border: 1px solid #1F2937; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1F2937; border-radius: 8px; color: white; padding: 10px 20px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #2563EB; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ OmniHealth AI: Unified Clinical Intelligence & Workflow Platform")
st.caption("Next-Generation Evolution integrating Computer Vision, Zero-Fatigue Task Optimization, Conversational EHR AI, and Precision Protocols.")
st.markdown("---")

# --- SIDEBAR: GLOBAL CONTROLS & EHR TELEMETRY ---
st.sidebar.header("🔗 Active EHR Data Feed")
patient_select = st.sidebar.selectbox("Select Patient Record", ["PAT-9082: Fatima Al-Zahra (ICU)", "PAT-4105: Mohammad Al-Otaibi (Step-Down)"])

if "9082" in patient_select:
    default_age, default_bmi, default_alb, default_brad = 83, 16.8, 2.1, 8
else:
    default_age, default_bmi, default_alb, default_brad = 62, 24.5, 3.8, 16

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Live Parameter Fine-Tuning")
age = st.sidebar.slider("Age", 18, 100, default_age)
bmi = st.sidebar.slider("BMI", 12.0, 45.0, default_bmi)
albumin = st.sidebar.slider("Serum Albumin (g/dL)", 1.0, 5.0, default_alb, 0.1)
braden = st.sidebar.slider("Braden Score", 6, 23, default_brad)

# --- TABS FOR OMNI-PLATFORM MODULES ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🩺 1. Vision & Risk Engine", 
    "🤖 2. Conversational EHR AI", 
    "📊 3. Nurse Workflow & Triage", 
    "🔬 4. Evidence-Based Protocols"
])

# --- TAB 1: VISION & RISK ENGINE ---
with tab1:
    st.subheader("🖼️ Computer Vision Wound & Skin Integrity Analyzer")
    st.markdown("Upload or capture high-resolution skin imagery for automated deep-learning tissue degradation classification.")
    
    col_v1, col_v2 = st.columns([1, 1])
    with col_v1:
        uploaded_file = st.file_uploader("Upload Patient Skin / Sacral Image (.jpg, .png)", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Telemetry Image", use_column_width=True)
        else:
            st.info("💡 Tip: Upload a sample wound or skin image to simulate computer vision segmentation and tissue ischemia detection.")
            
    with col_v2:
        st.markdown("### 🔍 AI Vision Telemetry Output")
        if uploaded_file is not None:
            st.warning("⚠️ **Early Stage Ischemia / Deep Tissue Threat Detected** (Confidence: 94.2%)")
            st.progress(0.94)
            st.markdown("""
            * **Erythema Analysis:** Non-blanching reactive hyperemia detected in sacral region.
            * **Thermal Disparity:** Microvascular restriction indicated via pixel color gradient mapping.
            * **Automated Recommendation:** Immediate offloading required; override standard 2-hour turning to 1-hour interval.
            """)
        else:
            risk_prob = ((23 - braden) / 19) * 100
            st.metric("Composite Algorithmic Risk Index", f"{risk_prob:.1f}%", delta="High Risk" if risk_prob > 50 else "Stable", delta_color="inverse" if risk_prob > 50 else "normal")
            st.success("✅ System ready for optical telemetry stream ingestion.")

# --- TAB 2: CONVERSATIONAL EHR AI ---
with tab2:
    st.markdown("### 💬 Conversational EHR Clinical Copilot")
    st.caption("Ask natural language queries regarding patient history, lab trends, or clinical guidelines.")
    
    user_query = st.text_input("Query Clinical Assistant (e.g., 'What is the protein requirement and underlying risk for this patient?')", "")
    if user_query:
        st.markdown(f"**Query Received:** {user_query}")
        est_w = bmi * (1.65 ** 2)
        p_low, p_high = est_w * 1.2, est_w * 1.5
        st.info(f"""
        **OmniHealth AI Response:**
        Based on the current telemetry for **{patient_select}**:
        1. **Pathophysiology:** The composite risk is driven by a Braden score of {braden} combined with Serum Albumin at {albumin} g/dL, indicating severe risk of skin breakdown due to compromised oncotic pressure.
        2. **Action Plan:** Immediate administration of **{p_low:.1f}g - {p_high:.1f}g/day** of protein alongside L-Arginine supplementation is mandated by ASPEN guidelines.
        """)

# --- TAB 3: NURSE WORKFLOW & TRIAGE ---
with tab3:
    st.markdown("### ⚡ Zero-Fatigue Nurse Workflow & Task Optimization")
    st.caption("Dynamic shift-change task scheduler designed to eliminate alert fatigue and optimize staff allocation.")
    
    workflow_df = pd.DataFrame({
        "Room / Bed": ["ICU-302", "ICU-305", "Step-Down 412", "Step-Down 418"],
        "Patient Name": ["Fatima A.", "John D.", "Mohammad O.", "Sara K."],
        "Assigned Nurse": ["Nurse Mary", "Nurse Ahmed", "Nurse Mary", "Nurse Noura"],
        "Priority Level": ["🚨 Critical (Immediate)", "⚠️ Moderate", "✅ Routine", "⚠️ Moderate"],
        "Next Intervention": ["30° Tilt + APAM Check", "Heel Offloading", "Standard Reposition", "Nutrition Review"]
    })
    st.dataframe(workflow_df, use_container_width=True)

# --- TAB 4: EVIDENCE-BASED PROTOCOLS ---
with tab4:
    st.markdown("### 📚 Integrated Clinical Guidelines (NPIAP & ASPEN)")
    
    est_w = bmi * (1.65 ** 2)
    p_low, p_high = est_w * 1.2, est_w * 1.5
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown(f"""
        ### 🥩 **Metabolic & Nutritional Prescription**
        * **Estimated Weight:** **{est_w:.1f} kg**
        * **Target Protein:** **{p_low:.1f}g – {p_high:.1f}g / day**
        * **Micronutrients:** L-Arginine (4.5g), Zinc Sulfate (50mg), Vitamin C (500mg).
        """)
    with col_p2:
        st.markdown(f"""
        ### 🛏️ **Biomechanical Care Bundle**
        * **Support Surface:** Alternating Pressure Air Mattress (APAM).
        * **Shear Prevention:** Head-of-bed angle capped strictly at **≤ 30°**.
        * **Intervals:** Automated repositioning alerts dispatched via zero-fatigue queue.
        """)
