import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.messages import SystemMessage, HumanMessage, AIMessage
import os
# title and header

st.title("Simple Langchain chat with groq")




## page config
st.set_page_config( page_title="Chatbot",
    page_icon="🤖", layout="centered")

with st.sidebar:
    st.header("Setting")
     ## api key
    api_key=st.text_input("GROQ API Key",type="password",help="get free api_key at console.groq.com")
    ## model selection
    model_name=st.selectbox("Model",["llama-3.1-8b-instant","llama-3.3-70b-versatile","openai/gpt-oss-120b"],index=0)
    ## clear button
    if st.button("clear chat"):
        st.session_state.messages=[]
        st.rerun()

## initialize chat history
#    if "messages" not in st.session_state:
#        st.session_state.messages=[]
if "messages" not in st.session_state:
    st.session_state.messages=[
        SystemMessage(content="You are a helpful assistant.")
    ]

## initialize model
@st.cache_resource
def get_chain(api_key,model_name):
    if not api_key:
        return None
    ## insitantiate the model
    llm=ChatGroq(groq_api_key=api_key,model=model_name,temperature=0.7,streaming=True)
    
    ##  instialation prompt template
    prompt=ChatPromptTemplate.from_messages([
        ("system","You are a helpful assistant."),
        ("human","{input}")
    ])
    ## create chain
    chain=prompt | llm | StrOutputParser()
    return chain

# get chain
chain=get_chain(api_key,model_name)

if not chain:
    st.warning("Please enter your GROQ API Key to start chatting.")
    st.markdown("[Get your free API Key at console.groq.com](https://console.groq.com/signup)")
else:

    ## display message
    for message in st.session_state.messages:
     

     if isinstance(message, dict):

        role = message["role"]
        content = message["content"]
     else:
        role = message.type
        content = message.content

     with st.chat_message(role):
        st.write(content)
     

    


## User input
if input := st.chat_input("Type your message here..."):

    # Display user message
    with st.chat_message("user", avatar="🧑"):
        st.write(input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": input
    })

    # Get AI response
    response = chain.invoke({"input": input})

    # Display AI response
    with st.chat_message("assistant", avatar="🤖"):
        st.write(response)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })