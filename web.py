import streamlit as st
import asyncio
from state import MailRoomState
from officialRun import mailbot  # Import the async function from officialRun.py
  # Run the async function to get the mailbot instance


# --- Custom CSS for a modern tech vibe ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #232526 0%, #414345 100%);
        color: #F8F8F2;
    }
    .stApp {
        background: linear-gradient(135deg, #232526 0%, #414345 100%);
    }
    .big-title {
        font-size: 3em;
        font-weight: bold;
        letter-spacing: 2px;
        color: #00FFF7;
        text-shadow: 0 0 10px #00FFF7, 0 0 20px #232526;
        margin-bottom: 0.5em;
    }
    .subtitle {
        font-size: 1.3em;
        color: #F8F8F2;
        margin-bottom: 2em;
    }
    .question-box {
        background: #232526;
        border-radius: 10px;
        padding: 2em;
        box-shadow: 0 4px 32px 0 rgba(0,255,247,0.15);
        margin-bottom: 2em;
    }
    .result-box {
        background: #181A1B;
        border-radius: 10px;
        padding: 2em;
        box-shadow: 0 4px 32px 0 rgba(0,255,247,0.10);
        margin-top: 2em;
        font-size: 1.2em;
        color: #00FFF7;
    }
    .footer {
        color: #888;
        font-size: 0.9em;
        margin-top: 3em;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Streamlit App Logic ---
st.set_page_config(page_title="AI Mailroom Chatbot", page_icon=":robot_face:", layout="centered")

# Use session state to store output
if "mailroom_output" not in st.session_state:
    st.session_state["mailroom_output"] = None
    st.session_state.page = "Ask Mailroom AI"
# # Sidebar navigation
# page = st.sidebar.radio("Navigation", ["Ask Mailroom AI", "View Output"], index=0)

if st.session_state.page == "Ask Mailroom AI":
    st.markdown('<div class="big-title">AI Mailroom Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Welcome to your futuristic mailroom assistant invented by BlakeC. Ask anything about your packages, deliveries, or mailroom operations!</div>', unsafe_allow_html=True)

    with st.form("ask_form"):
        # st.markdown('<div class="question-box">', unsafe_allow_html=True)x
        user_input = st.text_input("What would you like to ask?", placeholder="e.g. How many big packages for Blake Chang arrived today?")
        st.markdown('</div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Ask", use_container_width=True)
    
    if submitted and user_input.strip():
        with st.spinner("Mailbot is thinking..."):
            # Run the async workflow in a sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # You may need to adjust this depending on your teset() signature
            finalState: MailRoomState = loop.run_until_complete(
                 mailbot(user_input)
            )
            st.session_state["mailroom_output"] = finalState.get("result", "No result available.")
        # st.success("Your question has been processed! Go to 'View Output' to see the answer.")
        st.session_state.page = "View Output"
        st.rerun()  # Refresh the page to show the output
     
      # Refresh the page to show the output
     

elif st.session_state.page ==  "View Output":
    if st.button("Back to Main"):
            st.session_state.page = "Ask Mailroom AI"
            st.rerun()
    st.markdown('<div class="big-title"> Result: </div>', unsafe_allow_html=True)
    # st.markdown('<div class="subtitle">Here is the latest response from your AI Mailroom assistant:</div>', unsafe_allow_html=True)
    output = st.session_state.get("mailroom_output")
    if output:
        # You may need to adjust this depending on your MailRoomState/result structure
        st.markdown(f'<div class="result-box">{output if hasattr(output, "result") else output}</div>', unsafe_allow_html=True)
    else:
        st.info("No output yet. Please ask a question on the first page.")

st.markdown('<div class="footer">Powered by LangGraph, Streamlit, and your AI Mailroom 🤖</div>', unsafe_allow_html=True)
