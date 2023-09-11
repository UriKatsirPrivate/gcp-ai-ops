import streamlit as st
from langchain import LLMChain
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from initialization import initialize_llm

def gcpCliCommandGenerator(user_input):
    
    llm = initialize_llm(project_id,region,model_name,max_tokens,temperature,top_p,top_k)
    
    system_template = """You are a virtual assistant capable of generating the corresponding Google Cloud Platform (GCP) command-line interface (CLI) command based on the user's input."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The user's input is: '{user_input}'. Please generate the corresponding GCP CLI command."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=llm, prompt=chat_prompt)
    result = chain.run(user_input=user_input)
    return result # returns string   

def display_gcp_command(gcp_command):
    if gcp_command != "":
        st.markdown(f"**Generated GCP CLI Command:** {gcp_command}")
    else:
        st.markdown("No command generated. Please enter a valid GCP operation.")

# Step-1 Get input from the user
user_input = st.text_input("Please enter the desired GCP operation")
st.sidebar.write("Project ID: landing-zone-demo-341118") 
project_id="landing-zone-demo-341118"
region=st.sidebar.selectbox("Please enter the region",['us-central1'])
model_name = st.sidebar.selectbox('Enter model name',['text-bison','text-bison-32k','code-bison','code-bison-32k'])
max_tokens = st.sidebar.number_input('Enter max token output',min_value=1,max_value=8192,step=100,value=1024)
temperature = st.sidebar.number_input('Enter temperature',min_value=0.0,max_value=1.0,step=0.1,value=0.1)
top_p = st.sidebar.number_input('Enter top_p',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
top_k = st.sidebar.number_input('Enter top_k',min_value=1,max_value=40,step=1,value=40)


# Step-2 Put a submit button with an appropriate title
if st.button('Generate GCP CLI Command',disabled=not (project_id)):
    # Step-3 Call functions only if all user inputs are taken and the button is clicked.
    if user_input:
        with st.spinner('Generating command...'):
            gcp_command = gcpCliCommandGenerator(user_input)
        display_gcp_command(gcp_command)
    else:
        st.markdown("No command generated. Please enter a valid GCP operation.")