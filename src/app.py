import streamlit as st
import requests
import json
BACKEND_URL = "http://127.0.0.1:8000"
st.set_page_config(
    page_title="Financial RAG Agent",
    page_icon="💰",
    layout="wide"
)
st.markdown("""
<style>
    /* Force the main app background to white */
    .stApp {
        background-color: #ffffff;
        color: #000000; /* Force global text to black */
    }
    
    /* Force input fields to have dark text */
    .stTextInput > div > div > input {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        color: #000000; 
        background-color: #ffffff;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #000000;
        color: #ffffff;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #333333;
        color: #ffffff;
    }

    /* CRITICAL FIX: Target the markdown text inside chat messages */
    /* This ensures the AI response is dark grey/black, not light grey */
    .stChatMessage .stMarkdown p {
        color: #1a1a1a !important; 
    }
    
    /* Optional: Add a slight border/background to AI responses for better separation */
    div[data-testid="stChatMessage"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 10px;
    }

</style>
""", unsafe_allow_html=True)


st.title("Financial RAG Agent")
st.markdown("Analyze 10-K financial reports with AI.")
with st.sidebar:
    st.header("Configuration")
    
    ticker = st.text_input("Company Ticker", value="AAPL", max_chars=6, help="e.g., AAPL, MSFT, GOOGL")
    year = st.number_input("Year", min_value=1990, max_value=2025, value=2023, step=1)
    
    ingest_button = st.button("Ingest Data", type="primary")
    
    if ingest_button:
        with st.spinner(f"Ingesting 10-K for {ticker} ({year})..."):
            try:
                payload = {"ticker": ticker, "year": year}
                response = requests.post(f"{BACKEND_URL}/ingest", json=payload)
                
                if response.status_code == 200:
                    st.success(f"Successfully ingested {ticker}!")
                    st.json(response.json())
                else:
                    st.error(f"Ingestion failed: {response.status_code}")
                    st.text(response.text)
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Is uvicorn running?")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Ask a question about the financial reports..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        try:
            payload = {"query": prompt}
            response = requests.post(f"{BACKEND_URL}/chat", json=payload)
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer received.")
                with st.chat_message("assistant"):
                    st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
        except requests.exceptions.ConnectionError:
            msg = "Cannot connect to backend. Ensure the FastAPI server is running."
            st.error(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            msg = f"An error occurred: {e}"
            st.error(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
