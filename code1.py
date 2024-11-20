from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(role_model, question):
    """
    Generate a response from the Gemini AI based on the user's role model and question.
    """
    # Create a role model context
    role_model_prompt = f"You are {role_model}. Respond as if you are {role_model} answering this question."
    full_prompt = f"{role_model_prompt}\n\nQuestion: {question}"
    
    # Generate a response
    response = chat.send_message(full_prompt, stream=True)
    return response


# Initialize Streamlit app
st.set_page_config(page_title="Talk to Your Role Model", layout="wide")

# Header section
st.header("MIND HAVEN")

# Collect the role model's name
role_model = st.text_input("Enter the name of your role model:", placeholder="e.g., Elon Musk, Marie Curie, etc.")

# Collect the user's question
input_question = st.text_input("Ask your question:", placeholder="What would you like to ask?")

# Submit button
submit = st.button("Ask the question")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Response and chat history handling
if submit and role_model and input_question:
    # Get AI's response as the role model
    response = get_gemini_response(role_model, input_question)
    # Add user query and AI response to session state chat history
    st.session_state['chat_history'].append((f"You (to {role_model})", input_question))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append((f"{role_model}", chunk.text))

# Chat history display
if st.session_state['chat_history']:
    st.subheader("The Chat History is")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
