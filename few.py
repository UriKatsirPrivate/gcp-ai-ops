import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
from initialization import initialize_llm
st.title('Prompt Magic')
# Import necessary libraries

PROJECT_ID="landing-zone-demo-341118"
LANGSMITH_KEY_NAME="langchain-api-key"
REGIONS=["us-central1"]
MODEL_NAMES=['text-bison','text-bison-32k','chat-bison','code-bison','code-bison-32k']

st.sidebar.write("Project ID: ",f"{PROJECT_ID}") 
project_id=PROJECT_ID
region=st.sidebar.selectbox("Please enter the region",REGIONS)
model_name = st.sidebar.selectbox('Enter model name',MODEL_NAMES)
max_tokens = st.sidebar.slider('Enter max token output',min_value=1,max_value=8192,step=100,value=1024)
temperature = st.sidebar.slider('Enter temperature',min_value=0.0,max_value=1.0,step=0.1,value=0.1)
top_p = st.sidebar.slider('Enter top_p',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
top_k = st.sidebar.slider('Enter top_k',min_value=1,max_value=40,step=1,value=40)

llm=initialize_llm(project_id,region,model_name,max_tokens,temperature,top_p,top_k)

# Get openai_api_key
# openai_api_key = st.sidebar.text_input(
#     "OpenAI API Key",
#     placeholder="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",
#     value="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",
#     type="password",
# )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to convert zero-shot prompt into a few-shot prompt


def fewShotPromptConverter(zero_shot_prompt):
#     chat = ChatOpenAI(
#         model="gpt-3.5-turbo-16k",
#         openai_api_key=openai_api_key,
#         temperature=0
#     )
    chat = llm
    system_template = """You are an assistant designed to convert a zero-shot prompt into a few-shot prompt."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """The zero-shot prompt is: '{zero_shot_prompt}'. Please convert it into a few-shot prompt."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(zero_shot_prompt=zero_shot_prompt)
    return result  # returns string


# Create a form
with st.form(key='prompt_magic'):
    # Under the form, take all the user inputs
    zero_shot_prompt = st.text_area("Enter zero-shot prompt",height=200,)
    submit_button = st.form_submit_button(label='Submit Prompt')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # if not openai_api_key.startswith('sk-'):
        #     st.warning('Please enter your OpenAI API key!', icon='⚠')
        #     few_shot_prompt = ""
        if zero_shot_prompt:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                few_shot_prompt = fewShotPromptConverter(zero_shot_prompt)
        else:
            few_shot_prompt = ""
        # Display the few-shot prompt to the user
        if few_shot_prompt is not None and len(str(few_shot_prompt)) > 0:
            st.text(few_shot_prompt)