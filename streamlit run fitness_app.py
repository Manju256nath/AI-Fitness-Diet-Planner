import streamlit as st
import google.generativeai as genai

# ---- App Title ----
st.title("🏋️ AI Fitness & Diet Planner")
st.write("Get your personalized workout and diet plan using AI (Powered by Gemini!)")

# ---- Setup Gemini API ----
# This line pulls the key directly from your .streamlit/secrets.toml file
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except KeyError:
    st.error("🚨 Secret Key Missing! Please make sure you have a `.streamlit/secrets.toml` file with `GEMINI_API_KEY = 'your_key'` inside.")
    st.stop()

# ---- User Input ----
st.header("Enter Your Details")

age = st.number_input("Age", 10, 100, value=25)
weight = st.number_input("Weight (kg)", 30, 200, value=70)
height = st.number_input("Height (cm)", 100, 250, value=170)

goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "General Fitness"])
level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
diet = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])

# ---- Generate Button ----
if st.button("Generate Plan"):
    st.info("⏳ Generating your customized plan...")

    prompt = f"""
    Create a 7-day fitness and diet plan.
    User details:
    Age: {age}
    Weight: {weight}kg
    Height: {height}cm
    Goal: {goal}
    Fitness Level: {level}
    Diet Preference: {diet}

    Include:
    - Weekly workout plan
    - Daily meal plan
    - 1 Motivation tip
    """

    try:
        # Generate the response from Gemini
        response = model.generate_content(prompt)
        result = response.text

        # ---- Show Output ----
        st.subheader("📋 Your AI Plan")
        st.markdown(result)

        # ---- Download Option ----
        st.download_button(
            label="📥 Download Plan",
            data=result,
            file_name="fitness_plan.txt"
        )
        
    except Exception as e:
        st.error(f"An error occurred with the AI: {e}")