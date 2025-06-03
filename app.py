import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="MediGenie AI Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar inputs
with st.sidebar:
    st.header("Patient Information")
    symptoms = st.multiselect(
        'Symptoms',
        ['Fever', 'Cough', 'Headache', 'Fatigue', 'Nausea', 'Sore Throat',
         'Diarrhea', 'Rash', 'Muscle Pain', 'Loss of Smell'],
        help="Select all that apply"
    )
    age_group = st.selectbox('Age Group', ['child', 'young', 'adult', 'elderly'])
    gender = st.radio('Gender', ['male', 'female'], horizontal=True)
    temperature = st.slider('Temperature (°F)', 95.0, 110.0, 98.6, step=0.1)
    bp_level = st.select_slider('Blood Pressure Level', ['low', 'normal', 'high'])
    duration_days = st.number_input('Duration of Symptoms (days)', 1, 30, 5)
    severity = st.slider('Severity (1–5)', 1, 5, 3)
    if st.button('Get Recommendation'):
        st.session_state['request'] = True

# Main area
st.title("MediGenie: AI Health Assistant 🤖")
st.markdown("---")

if st.session_state.get('request'):
    # Build prompt internally
    prompt = f"""
You are an expert medical assistant. A patient has:

• Symptoms: {', '.join(symptoms)}
• Age: {age_group}, Gender: {gender}
• Temperature: {temperature}°F, BP: {bp_level}
• Duration: {duration_days} days, Severity: {severity}/5

Provide:
1. *Diagnosis* (1 sentence)
2. *Treatment* (1-line bullet: medicine, dosage, duration)
3. *Precautions* (2 short bullets)
(Max 120 words)
"""
    
    # Call Gemini API
    with st.spinner('Consulting AI...'):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a concise medical assistant.",
                temperature=0.5,
                max_output_tokens=200,
            ),
            contents=prompt
        )

    # Display user-entered data and AI response
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Entered Patient Details")
        st.markdown(f"- *Symptoms:* {', '.join(symptoms)}")
        st.markdown(f"- *Age Group:* {age_group}")
        st.markdown(f"- *Gender:* {gender}")
        st.markdown(f"- *Temperature:* {temperature}°F")
        st.markdown(f"- *Blood Pressure:* {bp_level}")
        st.markdown(f"- *Duration:* {duration_days} days")
        st.markdown(f"- *Severity:* {severity}/5")
    with col2:
        st.subheader("AI Recommendation")
        st.write(response.text)

    # Footer
    st.markdown("---")
    st.caption("Powered by Google Gemini API")
else:
    st.info("Please fill in the patient details on the sidebar and click 'Get Recommendation'.")
