import streamlit as st
from google import genai
from google.genai import errors

# 1. Page Configuration & Title
st.set_page_config(page_title="CareerPath AI", page_icon="💼", layout="centered")
st.title("💼 CareerPath AI: Smart Career Roadmap Engine")
st.write("An intelligent platform driven by advanced Prompt Engineering.")

# 2. Securely Initialize the AI Client using Streamlit Secrets
try:
    # This line safely fetches the key you paste into Streamlit's Advanced Settings
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("API Key missing. Please configure GEMINI_API_KEY in the Streamlit Secrets settings.")
    st.stop()

# 3. User Inputs (The Variables)
st.subheader("🤖 Define Your Career Goals")
target_role = st.text_input("What is your target job role?", placeholder="e.g., Junior Data Scientist, Frontend Developer")
current_skills = st.text_area("What are your current skills?", placeholder="e.g., Python, basic HTML, Excel")
time_commitment = st.slider("Weekly time commitment (Hours)", min_value=5, max_value=40, value=10)

# Initialize session state to remember the chat history for iteration
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_object" not in st.session_state:
    st.session_state.chat_object = None

# 4. Generate the Initial Roadmap
if st.button("Generate Optimized Roadmap", type="primary"):
    if target_role:
        with st.spinner("Engaging Instruction Prompting logic..."):
            # Behind the scenes: Your Final Optimized Instruction Prompt
            base_prompt = f"""
            Act as a Senior Career Coach and Technical Recruiter. 
            Create a structured 4-week career transition roadmap for a student aiming to become a {target_role}. 
            The student currently knows: {current_skills}.
            Include a weekly breakdown of essential technical skills, a list of industry-standard projects to build, and specific milestones for interview preparation. 
            Ensure the plan accounts for a {time_commitment} hours per week schedule.
            Make the output realistic, highly professional, and easy to follow.
            """
            
            try:
                # Start a chat session to allow for future iteration using the standard flash model
                chat = client.chats.create(model="gemini-2.5-flash")
                response = chat.send_message(base_prompt)
                
                # Clear previous history and save the new session
                st.session_state.messages = [{"role": "assistant", "content": response.text}]
                st.session_state.chat_object = chat
            except Exception as e:
                st.error(f"Failed to communicate with AI: {e}")
    else:
        st.warning("Please enter a target job role first.")

# 5. Display the Output and Enable Iteration
if st.session_state.messages:
    st.markdown("---")
    st.subheader("📋 Your Personalized Career Plan")
    st.markdown(st.session_state.messages[-1]["content"])
    
    # Showcase Iterative Refinement
    st.markdown("---")
    st.subheader("🔄 Iterative Refinement (Prompt Engineering Feature)")
    st.write("Not quite right? Instruct the AI to tweak the results dynamically:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👶 Make it more beginner-friendly"):
            if st.session_state.chat_object:
                with st.spinner("Refining..."):
                    response = st.session_state.chat_object.send_message("The previous plan was a bit too advanced. Please adjust the timeline to be more beginner-friendly.")
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    st.rerun()
                
    with col2:
        if st.button("💼 Focus more on Interview Prep"):
            if st.session_state.chat_object:
                with st.spinner("Refining..."):
                    response = st.session_state.chat_object.send_message("Please restructure the plan to emphasize rigorous technical mock interview preparation and behavioral question drills.")
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    st.rerun()
