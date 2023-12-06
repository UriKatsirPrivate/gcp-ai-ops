import os
import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from initialization import initialize_llm, initialize_tracing
from placeholders import *
from system_prompts import *
import requests

# https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
st.set_page_config(
    page_title="GCP AI Ops",
    page_icon="icons/vertexai.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://cloud.google.com/vertex-ai?hl=en',
        # 'About': "# This is a header. This is an *extremely* cool app!"
        'About': "#### Created by [Uri Katsir](https://www.linkedin.com/in/uri-katsir/)"
    }
)

LANGSMITH_KEY_NAME="langchain-api-key"
REGIONS=["europe-west4","us-central1","us-west4","us-west1","us-east4","northamerica-northeast1","europe-west1","europe-west2","europe-west3","europe-west9"]
MODEL_NAMES=['text-bison-32k','text-bison','code-bison','code-bison-32k']

def get_project_id():
    metadata_server_url = "http://metadata.google.internal/computeMetadata/v1/"
    metadata_flavor = {'Metadata-Flavor': 'Google'}
    try:
        response = requests.get(metadata_server_url + "project/project-id", headers=metadata_flavor)
        if response.status_code == 200:
            project_id = response.text
            return project_id
        else:
            print(f"Failed to retrieve project ID. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

PROJECT_ID=st.sidebar.text_input(label="Project ID",value="Your Project ID")
if PROJECT_ID=="" or PROJECT_ID=="Your Project ID":
    # print("getting project id")
    PROJECT_ID=get_project_id()

st.sidebar.write("Project ID: ",f"{PROJECT_ID}") 
project_id=PROJECT_ID
region=st.sidebar.selectbox("Please enter the region",REGIONS)
model_name = st.sidebar.selectbox('Enter model name',MODEL_NAMES)
max_tokens = st.sidebar.slider('Enter max token output',min_value=1,max_value=8192,step=100,value=8192)
temperature = st.sidebar.slider('Enter temperature',min_value=0.0,max_value=1.0,step=0.1,value=0.1)
top_p = st.sidebar.slider('Enter top_p',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
top_k = st.sidebar.slider('Enter top_k',min_value=1,max_value=40,step=1,value=40)

if not ('32k' in model_name) and max_tokens>1024:
  st.error(f'{max_tokens} output tokens is not a valid value for model {model_name}')

# Initialize tracing variables
tracing = st.sidebar.toggle('Enable Langsmith Tracing',disabled=True)
langsmith_endpoint = st.sidebar.text_input(label="Langsmith Endpoint", value="https://api.smith.langchain.com", disabled=not tracing)
langsmith_project = st.sidebar.text_input(label="Langsmith Project", value="gcp-ai-ops", disabled=not tracing)

# Check if initialize_tracing() has already been called
# if 'tracing_initialized' not in st.session_state:
#     initialize_tracing(tracing,langsmith_endpoint,langsmith_project,PROJECT_ID,LANGSMITH_KEY_NAME)
#     # Set the flag to indicate that initialize_tracing() has been called
#     st.session_state.tracing_initialized = True

# if tracing:
#     os.environ["LANGCHAIN_TRACING_V2"]="True"
# else:
#     os.environ["LANGCHAIN_TRACING_V2"]="False"

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.15rem;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)
tab1, tab2, tab3, tab4, tab5= st.tabs(["Run Prompt / "
                                             , "Generate gCloud Command / "
                                             ,"Generate Terraform /"
                                             ,"Inspect IaC /"
                                             ,"TF Converter /"
                                             
                                             ])

llm = initialize_llm(project_id,region,model_name,max_tokens,temperature,top_p,top_k)

with tab1:
    def promptExecutor(prompt):
    
        system_template = """You are an AI assistant designed to execute the given prompt: '{prompt}'."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = """Please execute the following prompt: '{prompt}'."""
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=llm, prompt=chat_prompt)
        result = chain.run(prompt=prompt)
        return result # returns string   

    def display_result(execution_result):
        if execution_result != "":
            # st.markdown(f"**Execution Result:** {execution_result}")
            st.code(execution_result)
        else:
            st.warning('No result to display.')

    #Get the prompt from the user
    prompt = st.text_area('Enter your prompt:',height=200, key=3,placeholder=RUN_PROMPT_PLACEHOLDER)
    
    if st.button('Execute Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
        if prompt:
            with st.spinner('Running prompt...'):
                execution_result = promptExecutor(prompt)
            display_result(execution_result)
        else:
            st.warning('Please enter a prompt before executing.')
with tab2:
    def gcpCliCommandGenerator(user_input):
    
        system_template = """You are a virtual assistant capable of generating the corresponding Google Cloud Platform (GCP) command-line interface (CLI) command based on the user's input."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = """The user's input is: '{user_input}'. Please generate the corresponding GCP CLI command. 
                            Be as elaborate as possible.
                            For every flag you use, explain its purpose. also, make sure to provide a working sample command. """
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=llm, prompt=chat_prompt)
        result = chain.run(user_input=user_input)
        return result # returns string
    
    def display_gcp_command(gcp_command):
        if gcp_command != "":
            # st.markdown(f"**Generated GCP CLI Command:** {gcp_command}")
            st.markdown(f"**Generated GCP CLI Command:")
            st.code(gcp_command)

        else:
            st.markdown("No command generated. Please enter a valid GCP operation.")

    user_input = st.text_area("Enter the desired GCP operation:",height=200, placeholder=GCLOUD_PLACEHOLDER)

    if st.button('Generate GCP CLI Command',disabled=not (project_id)):
        if user_input:
            with st.spinner('Generating command...'):
                gcp_command = gcpCliCommandGenerator(user_input)
            display_gcp_command(gcp_command)
        else:
            st.markdown("No command generated. Please enter a valid GCP operation.")
with tab3:
    def terraformGenerator(description):
    
        system_template = """You are a terraform expert capable of generating Terraform files based on the user's description."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = """Please generate the appropriate Terraform files based on this description.
                            Use input variables as much a possible.
                            When makes sense,split the result into modules. Also, create the accompanying .tfvars file.
                            The user's description is: '{description}'"""
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=llm, prompt=chat_prompt)
        result = chain.run(description=description)
        return result # returns string
    def display_terraform_files(terraform_files):
        if terraform_files:
            # st.markdown(f"### Generated Terraform Files: \n {terraform_files}")
            st.markdown(f"### Generated Terraform Files:")
            st.code(terraform_files)
        else:
            st.markdown("No Terraform files generated. Please provide a valid description.")        

    description = st.text_area("Enter the description of the desired architecture on GCP:",height=200, placeholder=GENERATE_TF_PLACEHOLDER)
    if st.button('Generate Terraform Files',disabled=not (project_id)):

        if description:
            with st.spinner('Generating Terraform...'):
                terraform_files = terraformGenerator(description)
            display_terraform_files(terraform_files)
        else:
            st.markdown("No description provided. Please enter a valid description.")
    else:
        terraform_files = ""
        # display_terraform_files(terraform_files)
with tab4:
    def terraformScanner(module_string):
        
        system_template = """You are a security assistant designed to scan for vulnerabilities in the provided terraform module or gcloud commands string content."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = """Please scan the following terraform module or gcloud command for any potential vulnerabilities.
                            For each vulnerability that you find, provide a secure terraform or gCloud alternative.
                            Here is the module: '{module_string}'."""
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=llm, prompt=chat_prompt)
        result = chain.run(module_string=module_string)
        return result # returns string
    def display_vulnerabilities(vulnerabilities):
        if vulnerabilities:
            st.markdown(f"**Vulnerabilities Found:** {vulnerabilities}")
            # st.code(vulnerabilities)
        else:
            st.markdown("No vulnerabilities found.")   
    
    description = st.text_area("Enter Terraform:",height=200, placeholder=INSPECT_IAC_PLACEHOLDER)
    if st.button('Scan',disabled=not (project_id)):
        if description:
            with st.spinner('Scanning for vulnerabilities...'):
                gcp_command = terraformScanner(description)
            display_vulnerabilities(gcp_command)
        else:
            st.markdown("No command generated. Please enter a valid GCP operation.")
with tab5:
    def terraformConverter(module_string):
        
        system_template = """You are a devops expert, specializing in infrastructure ad code and terraform"""
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = """Convert the following AWS Terraform to equivalent GCP Terraform. Use input variables as much a possible.
                            When makes sense,split the result into modules. Also, create the accompanying .tfvars file.
                            Here is the module:'{module_string}'."""
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=llm, prompt=chat_prompt)
        result = chain.run(module_string=module_string)
        return result # returns string
    def display_tf(converted):
        if converted:
             st.code(converted)
        else:
            st.markdown("Not found.")   
    
    description = st.text_area("Enter AWS Terraform:",height=200,placeholder=TF_CONVERTER_PLACEHOLDER)
    if st.button('Convert to GCP',disabled=not (project_id)):
        if description:
            with st.spinner('Converting...'):
                gcp_tf = terraformConverter(description)
            display_tf(gcp_tf)
        else:
            st.markdown("No terraform generated. Please enter a valid AWS terraform.")