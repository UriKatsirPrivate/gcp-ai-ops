import streamlit as st
from langchain import LLMChain
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from initialization import initialize_llm

# Step-2 Write all the function definitions
def terraformGenerator(description):
    llm = initialize_llm(project_id,region,model_name,max_tokens,temperature,top_p,top_k)

    system_template = """You are a terraform expert capable of generating Terraform files based on the user's description."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The user's description is: '{description}'. Please generate the appropriate Terraform files based on this description."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=llm, prompt=chat_prompt)
    result = chain.run(description=description)
    return result # returns string   

def display_terraform_files(terraform_files):
    if terraform_files:
        st.markdown(f"### Generated Terraform Files: \n {terraform_files}")
    else:
        st.markdown("No Terraform files generated. Please provide a valid description.")

st.title('TF Generator')
description = st.text_area("Please enter the description of the desired architecture on GCP")
st.sidebar.write("Project ID: landing-zone-demo-341118") 
project_id="landing-zone-demo-341118"
region=st.sidebar.selectbox("Please enter the region",['us-central1'])
model_name = st.sidebar.selectbox('Enter model name',['text-bison','text-bison-32k','code-bison','code-bison-32k'])
max_tokens = st.sidebar.number_input('Enter max token output',min_value=1,max_value=8192,step=100,value=1024)
temperature = st.sidebar.number_input('Enter temperature',min_value=0.0,max_value=1.0,step=0.1,value=0.1)
top_p = st.sidebar.number_input('Enter top_p',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
top_k = st.sidebar.number_input('Enter top_k',min_value=1,max_value=40,step=1,value=40)

if st.button('Generate Terraform Files'):

    if description:
        terraform_files = terraformGenerator(description)
        display_terraform_files(terraform_files)
    else:
        st.markdown("No description provided. Please enter a valid description.")
else:
    terraform_files = ""
    display_terraform_files(terraform_files)