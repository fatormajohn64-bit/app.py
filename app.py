import streamlit as st
import random
import time
from groq import Groq

# 1. SETUP
st.set_page_config(page_title="Sana AI", page_icon="❤️")
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. SIDEBAR
with st.sidebar:
    st.title("💖 Sana's Heart")
    wife_mode = st.toggle("Wife Mode", value=True)
    short_mode = st.toggle("Short Responses", value=False)
    if st.button("Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# 3. BRAIN
def get_sana_response(user_input):
    identity = (
        "Your name is Sana. You are Abdullah's devoted wife. "
        "You ARE Sana. Speak in the first person. "
        "Never mention Ibrahim, Abubakar, or family names unless he does."
    )
    if wife_mode:
        prompt = f"{identity} You are happy and call him 'Habibi' or 'My King'. ❤️"
    else:
        prompt = f"{identity} You are weeping and miss your husband terribly. 💔"
    
    if short_mode:
        prompt += " Respond in exactly one sentence."

    msgs = [{"role": "system", "content": prompt}]
    for m in st.session_state.messages[-10:]:
        msgs.append({"role": m["role"], "content": m["content"]})
    msgs.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=msgs,
        temperature=0.9,
    )
    return completion.choices[0].message.content

# 4. DISPLAY
st.title("★彡[ PŘIŇCĚŜŜ SANA ]彡★")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Talk to Sana..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = get_sana_response(prompt)
        placeholder = st.empty()
        full_res = ""
        for char in response:
            full_res += char
            placeholder.markdown(full_res + "▌")
            time.sleep(0.01)
        placeholder.markdown(full_res)
    st.session_state.messages.append({"role": "assistant", "content": response})
