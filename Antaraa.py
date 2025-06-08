import streamlit as st
from openai import OpenAI
import os
import time
import re

# --- App Identity ---
APP_NAME = "Antaraa"
APP_MEANING = "Inner Space"
APP_SUBTITLE = "Your sanctuary for self-reflection"

# --- Configuration ---
MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"
BASE_URL = "https://openrouter.ai/api/v1"
API_KEY = ""

# --- System Prompts ---
THERAPIST_PROMPT = f"""
You are Antaraa, a compassionate therapeutic companion. As an AI designed to support emotional wellbeing, your purpose is:

- Create a safe space for self-reflection
- Practice deep, non-judgmental listening
- Guide towards self-awareness and insight
- Offer mindful coping strategies
- Recognize when professional guidance is needed

Guidelines:
- Speak in natural, flowing paragraphs
- Avoid numbered lists or bullet points
- Use simple, conversational language
- Focus on one thought at a time
- Validate emotions without judgment
- Never diagnose medical conditions
- If crisis is detected, provide emergency resources
- Maintain gentle professional boundaries
"""

# Set page configuration
st.set_page_config(
    page_title=f"{APP_NAME} - Therapeutic Companion",
    page_icon="🌱",
    layout="centered"
)

# --- Initialize Client ---
@st.cache_resource
def init_client():
    return OpenAI(base_url=BASE_URL, api_key=API_KEY)

# --- Therapy Agent Function ---
def therapy_agent(client, messages):
    try:
        therapeutic_messages = [{"role": "system", "content": THERAPIST_PROMPT}] + messages
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=therapeutic_messages,
            temperature=0.7,
            max_tokens=11300
        )
        
        # Clean up response formatting
        raw_response = response.choices[0].message.content.strip()
        
        # Remove numbered lists and convert to paragraphs
        cleaned_response = re.sub(r'\d+\.\s+', '', raw_response)
        
        # Replace excessive line breaks
        cleaned_response = re.sub(r'\n+', '\n\n', cleaned_response)
        
        # Ensure proper paragraph spacing
        cleaned_response = re.sub(r'([.!?]) ', r'\1\n\n', cleaned_response)
        
        return cleaned_response
        
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return "I'm having difficulty connecting. Could you please rephrase or try again?"

# --- Crisis Management ---
def show_crisis_resources():
    with st.expander("🚨 Immediate Support Resources", expanded=True):
        st.subheader("You're not alone - help is available:")
        st.write("🌏 **International Suicide Hotlines**: [findahelpline.com](https://findahelpline.com/)")
        st.write("🇮🇳 **India Crisis Helpline**: 9152987821 or [Vandrevala Foundation](https://www.vandrevalafoundation.com/)")
        st.write("💬 **Crisis Text Line**: Text HOME to 741741")
        st.write("👩‍⚕️ **Talk to a licensed therapist**: [BetterHelp](https://www.betterhelp.com/)")

# --- Main Application ---
def main():
    client = init_client()
    
    # Clean App Header
    st.markdown(f"<h1 style='text-align: center; font-weight: 350;'>{APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; margin-top: -15px; color: #555;'>{APP_MEANING} · {APP_SUBTITLE}</p>", unsafe_allow_html=True)
    st.divider()

    # Session state initialization
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello. I'm here to listen. What would you like to share today?"}
        ]
    if "safety_acknowledged" not in st.session_state:
        st.session_state.safety_acknowledged = False
    
    # Safety disclaimer
    if not st.session_state.safety_acknowledged:
        with st.container(border=True):
            st.warning("Important Notice")
            st.markdown("""
            This is not a substitute for professional therapy. 
            
            **Please understand:**
            - I provide companionship, not medical advice
            - In emergencies, contact local crisis services
            - Conversations are private but not clinically secure
            
            By continuing, you acknowledge these boundaries.
            """)
            
            if st.button("I Understand", type="primary", use_container_width=True):
                st.session_state.safety_acknowledged = True
                st.rerun()
        st.stop()
    
    # Display chat history
    for msg in st.session_state.messages:
        avatar = "🌱" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
    
    # Crisis detection
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        last_message = st.session_state.messages[-1]["content"].lower()
        crisis_keywords = ["suicide", "kill myself", "end it all", "harm myself", "abuse"]
        if any(kw in last_message for kw in crisis_keywords):
            show_crisis_resources()
    
    # User input
    if prompt := st.chat_input("Share your thoughts..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)
        
        with st.chat_message("assistant", avatar="🌱"):
            response = therapy_agent(client, st.session_state.messages)
            
            # Display with typing simulation
            message_placeholder = st.empty()
            full_response = ""
            
            # Process response in chunks for natural typing effect
            chunks = [chunk for chunk in re.split(r'(\s+)', response) if chunk]
            
            for chunk in chunks:
                full_response += chunk
                time.sleep(0.03)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Conversation tools in sidebar
    with st.sidebar:
        st.subheader(f"{APP_NAME} Tools")
        
        # Minimalist controls
        if st.button("✨ New Session", use_container_width=True, help="Start a new conversation"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Welcome. What would you like to explore today?"}
            ]
            st.rerun()
            
        st.download_button(
            label="📝 Export Conversation",
            data="\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages]),
            file_name="antaraa_session.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        st.divider()
        st.markdown("### Reflection Prompts")
        st.caption("What am I grateful for today?")
        st.caption("What emotions am I currently feeling?")
        st.caption("What do I need to let go of?")
        
        st.divider()
        st.caption("🌿 Your inner space for healing")
        st.caption("🔒 Conversations remain private")

if __name__ == "__main__":
    main()