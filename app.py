import os
import streamlit as st
from langchain import LLMChain
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from initialization import initialize_llm, initialize_tracing
from prompts import PROMPT_IMPROVER_PROMPT

PROJECT_ID="landing-zone-demo-341118"
REGIONS=["us-central1"]
MODEL_NAMES=['text-bison','text-bison-32k','code-bison','code-bison-32k']

st.sidebar.write("Project ID: ",f"{PROJECT_ID}") 
project_id=PROJECT_ID
region=st.sidebar.selectbox("Please enter the region",REGIONS)
model_name = st.sidebar.selectbox('Enter model name',MODEL_NAMES)
max_tokens = st.sidebar.number_input('Enter max token output',min_value=1,max_value=8192,step=100,value=1024)
temperature = st.sidebar.number_input('Enter temperature',min_value=0.0,max_value=1.0,step=0.1,value=0.1)
top_p = st.sidebar.number_input('Enter top_p',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
top_k = st.sidebar.number_input('Enter top_k',min_value=1,max_value=40,step=1,value=40)

# Initialize tracing variables
tracing = st.sidebar.toggle('Enable Langsmith Tracing')
langsmith_endpoint = st.sidebar.text_input(label="Langsmith Endpoint", value="https://api.smith.langchain.com", disabled=not tracing)
langsmith_project = st.sidebar.text_input(label="Langsmith Project", value="GCP AI OPS", disabled=not tracing)
# langsmith_key = get_from_secrets_manager("langchain-api-key", PROJECT_ID, "")

initialize_tracing(tracing,langsmith_endpoint,langsmith_project)

if tracing:
    tracing=True
    os.environ["LANGCHAIN_TRACING_V2"]="True"
    # initialize_tracing(tracing,langsmith_endpoint,langsmith_project)
else:
    tracing=False
    os.environ["LANGCHAIN_TRACING_V2"]="False"
    # initialize_tracing(tracing,langsmith_endpoint,langsmith_project)



css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.15rem;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)
tab1, tab2, tab3, tab4, tab5= st.tabs(["Improve Prompt / ", "Inspect My Prompt / ","Run My Prompt / ", "Generate gCloud Commands / ","Generate Terraform"])

llm = initialize_llm(project_id,region,model_name,max_tokens,temperature,top_p,top_k)


with tab1:
    initial_prompt = st.text_area("Enter your prompt:", height=200,max_chars=None, key=1)
    
    # Initialize LLMChain
    prompt_improver_chain = LLMChain(llm=llm, prompt=PROMPT_IMPROVER_PROMPT)

    # Run LLMChain
    # if st.button('Generate Improved Prompt',disabled=not (project_id) or not (initial_prompt)):
    if st.button('Generate Improved Prompt',disabled=not (project_id)):
        if initial_prompt:
            with st.spinner("Generating Improved Prompt..."):
                improved_prompt = prompt_improver_chain.run(initial_prompt)
                st.markdown("""
                                ### Improved Prompt:
                                """)
                st.code(improved_prompt)
        else:
            st.error(f"Please provide a prompt")
with tab2:
    def securityInspector(prompt):
    
        llm = initialize_llm(project_id,region,model_name,max_tokens,temperature,top_p,top_k)

        system_template = """You are a security analyst. Your task is to inspect the given prompt for any potential security issues."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = """Please inspect the following prompt for security issues: '{prompt}'."""
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=llm, prompt=chat_prompt)
        result = chain.run(prompt=prompt)
        return result # returns string
    
    def safePromptSuggester(inspection_result):

        system_template = """You are an AI assistant designed to suggest a modified, safe prompt if security issues are found in the original prompt."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = """Based on the inspection result: '{inspection_result}', please suggest a modified, safe prompt."""
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=llm, prompt=chat_prompt)
        result = chain.run(inspection_result=inspection_result)
        return result # returns string
    def displaySafePrompt(safe_prompt):
        if safe_prompt:
            st.markdown(f"**Modified, Safe Prompt:** {safe_prompt}")
        else:
            st.markdown("No modifications needed.")
                    
    prompt=st.text_area("Enter your prompt:",height=200, max_chars=None, key=None)
    if st.button('Inspect and Modify Prompt',disabled=not (project_id)):
        if prompt:
            with st.spinner('Inspecting prompt...'):
                inspection_result = securityInspector(prompt)
            st.text_area('Inspection Result', inspection_result, height=200, max_chars=None, key=None)
            # print(inspection_result)
            # if (inspection_result != "System: The prompt you provided does not contain any security issues."):
            if ("does not contain any security issues" not in inspection_result):
                with st.spinner('Creating Safe Prompt...'):
                    safe_prompt = safePromptSuggester(inspection_result)
                displaySafePrompt(safe_prompt)
        else:
            st.markdown("Please enter a prompt.")
with tab3:
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
    prompt = st.text_area('Enter your prompt:',height=200, max_chars=None, key=3)
    
    if st.button('Execute Prompt'):
        if prompt:
            execution_result = promptExecutor(prompt)
            display_result(execution_result)
        else:
            st.warning('Please enter a prompt before executing.')
with tab4:
    def gcpCliCommandGenerator(user_input):
    
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
            # st.markdown(f"**Generated GCP CLI Command:** {gcp_command}")
            st.markdown(f"**Generated GCP CLI Command:")
            st.code(gcp_command)

        else:
            st.markdown("No command generated. Please enter a valid GCP operation.")

    user_input = st.text_area("Enter the desired GCP operation:",height=200, max_chars=None, key=None)

    if st.button('Generate GCP CLI Command',disabled=not (project_id)):
        if user_input:
            with st.spinner('Generating command...'):
                gcp_command = gcpCliCommandGenerator(user_input)
            display_gcp_command(gcp_command)
        else:
            st.markdown("No command generated. Please enter a valid GCP operation.")
with tab5:
    def terraformGenerator(description):
    
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
            # st.markdown(f"### Generated Terraform Files: \n {terraform_files}")
            st.markdown(f"### Generated Terraform Files:")
            st.code(terraform_files)
        else:
            st.markdown("No Terraform files generated. Please provide a valid description.")        

    description = st.text_area("Enter the description of the desired architecture on GCP:",height=200, max_chars=None, key=None)
    if st.button('Generate Terraform Files',disabled=not (project_id)):

        if description:
            terraform_files = terraformGenerator(description)
            display_terraform_files(terraform_files)
        else:
            st.markdown("No description provided. Please enter a valid description.")
    else:
        terraform_files = ""
        # display_terraform_files(terraform_files)