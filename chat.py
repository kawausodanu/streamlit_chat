import streamlit as st
from openai import OpenAI

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key = "openai_api_key")

# 会話履歴
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "どのようにお手伝いしましょうか。"
        }
    ]
if "response" not in st.session_state:
    st.session_state["response"] = None

# 会話履歴を表示
messages = st.session_state.messages
for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])


#ユーザ入力を表示
prompt = st.chat_input(placeholder="メッセージを入力してください。")

if prompt:
    messages.append({
        "role": "user",
        "content": prompt
    })
    st.chat_message(name="user").write(prompt)

    if not openai_api_key:
        st.info("APIキーを設定してください。")
        st.stop()
    
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            ]
        )

    st.session_state["response"] = completion.choices[0].message.content
    
    # 回答を表示
    with st.chat_message("assistant"):
        messages.append({
            "role": "assistant",
            "content": st.session_state["response"]
        })
        st.write(st.session_state["response"])
    
    