import streamlit as st
import requests

st.set_page_config(page_title="CareerPath AI", page_icon="💼", layout="centered")
st.title("💼 CareerPath AI: Smart Career Roadmap Engine")
st.write("An intelligent platform driven by advanced Prompt Engineering.")

# Fetch API key safely
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("API Key missing in Streamlit Secrets.")
    st.stop()

st.subheader("🤖 Define Your Career Goals")
target_role = st.text_input("What is your target job role?", placeholder="e.g., Junior Data Scientist, Frontend Developer")
current_skills = st.text_area("What are your current skills?", placeholder="e.g., Python, basic HTML, Excel")
time_commitment = st.slider("Weekly time commitment (Hours)", min_value=5, max_value=40, value=10)

if st.button("Generate Optimized Roadmap", type="primary"):
    if target_role:
        with st.spinner("Engaging Instruction Prompting logic..."):
            base_prompt = f"""
            Act as a Senior Career Coach and Technical Recruiter. 
            Create a structured 4-week career transition roadmap for a student aiming to become a {target_role}. 
            The student currently knows: {current_skills}. Include technical skills and interview milestones.
            """
            
            # Using raw HTTP request to bypass strict SDK handshake errors
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": base_prompt}]}]}
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(url, json=payload, headers=headers)
            res_data = response.json()
            
            if response.status_code == 200:
                try:
                    output_text = res_data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("---")
                    st.subheader("📋 Your Personalized Career Plan")
                    st.markdown(output_text)
                except Exception:
                    st.error("Failed to parse AI response.")
            else:
                st.error(f"Google Server Error: {res_data.get('error', {}).get('message', 'Unknown Error')}")
    else:
        st.warning("Please enter a target job role.")
