import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Retrieve the API key from variable 'x'
api_key = os.getenv("x")

# Streamlit Page Configuration
st.set_page_config(
    page_title="🌈 Ultra-Colorful Groq Chatbot",
    page_icon="🦄",
    layout="centered",
)

# --- EXTREMELY COLORFUL CUSTOM CSS ---
st.markdown(
    """
    <style>
    /* Animated Rainbow Background Gradient for Main App */
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 20%, #ffecd2 40%, #fcb69f 60%, #a1c4fd 80%, #c2e9fb 100%);
        background-size: 400% 400%;
        animation: rainbowBackground 15s ease infinite;
    }

    @keyframes rainbowBackground {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Vibrant Header Banner */
    .rainbow-header {
        background: linear-gradient(90deg, #ff0844, #ffb199, #f7ff00, #00dbde, #fc00ff);
        background-size: 300% 300%;
        animation: shimmer 6s infinite alternate;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-weight: 900;
        font-size: 28px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin-bottom: 20px;
    }

    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }

    /* Customizing Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1d2b64 0%, #f8cdda 100%);
        color: white;
    }

    /* Styling User Message Bubbles */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%);
        border-radius: 20px;
        padding: 10px;
        border: 2px solid #fff;
        box-shadow: 0 4px 15px rgba(255, 117, 140, 0.4);
    }

    /* Styling Assistant Message Bubbles */
    [data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        border-radius: 20px;
        padding: 10px;
        border: 2px solid #fff;
        box-shadow: 0 4px 15px rgba(67, 233, 123, 0.4);
    }

    /* Text styling inside chat */
    [data-testid="stChatMessage"] p {
        color: #111111 !important;
        font-weight: 600;
    }

    /* Input Box Styling */
    .stChatInput input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 3px solid #ff0844 !important;
        border-radius: 30px !important;
        color: #333 !important;
        font-weight: bold;
    }

    /* Glowing Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #ff0844, #ffb199);
        color: white;
        border-radius: 25px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 8, 68, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(45deg, #00dbde, #fc00ff);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar Customization ---
with st.sidebar:
  st.markdown("### 🦄 Rainbow Control Panel")
  st.info("✨ Theme: Maximalist Technicolor Dream")
  st.write("---")
  if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = [{
        "role": "system",
        "content": "You are a helpful, witty, and concise AI assistant.",
    }]
    st.rerun()
  st.write("---")
  st.caption("Powered by Groq & OpenAI GPT-OSS 120B")

# --- Main App Header ---
st.markdown(
    '<div class="rainbow-header">🌈 ✨ ULTIMATE GROQ CHROMATIC CHAT ✨ 🌈</div>',
    unsafe_allow_html=True,
)

# 3. Validate API key
if not api_key:
  st.error(
      "❌ **Error:** API key not found. Make sure variable `x` is defined in"
      " your `.env` file."
  )
  st.stop()

# 4. Initialize the Groq client
client = Groq(api_key=api_key)
MODEL_NAME = "openai/gpt-oss-120b"

# 5. Initialize conversation history in Streamlit session state
if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "system",
      "content": "You are a helpful, witty, and concise AI assistant.",
  }]

# Display prior chat messages
for message in st.session_state.messages:
  if message["role"] != "system":
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

# 6. Handle user input from the chat box at the bottom
if user_input := st.chat_input("Type a message to the rainbow realm..."):
  # Display user message
  with st.chat_message("user"):
    st.markdown(user_input)

  # Append user message to history
  st.session_state.messages.append({"role": "user", "content": user_input})

  # Generate and display assistant response
  with st.chat_message("assistant"):
    with st.spinner("🎨 Mixing colors & generating response..."):
      try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=1024,
        )
        assistant_reply = response.choices[0].message.content
        st.markdown(assistant_reply)

        # Append assistant reply to history
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

      except Exception as e:
        st.error(f"An error occurred: {e}")