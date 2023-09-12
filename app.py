import streamlit as st
from langchain import LLMChain
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from initialization import initialize_llm
from prompts import PROMPT_IMPROVER_PROMPT


st.sidebar.write("Project ID: landing-zone-demo-341118") 
project_id="landing-zone-demo-341118"
region=st.sidebar.selectbox("Please enter the region",['us-central1'])
model_name = st.sidebar.selectbox('Enter model name',['text-bison','text-bison-32k','code-bison','code-bison-32k'])
max_tokens = st.sidebar.number_input('Enter max token output',min_value=1,max_value=8192,step=100,value=1024)
temperature = st.sidebar.number_input('Enter temperature',min_value=0.0,max_value=1.0,step=0.1,value=0.1)
top_p = st.sidebar.number_input('Enter top_p',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
top_k = st.sidebar.number_input('Enter top_k',min_value=1,max_value=40,step=1,value=40)

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.15rem;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)
tab1, tab2, tab3, tab4= st.tabs(["Improve Prompt / ", "Inspect My Prompt / ","Generate CLI Commands / ","Generate Terraform"])

llm = initialize_llm(project_id,region,model_name,max_tokens,temperature,top_p,top_k)

with tab1:
    initial_prompt = st.text_area("Please enter your prompt here:", height=200,max_chars=None, key=None)
    
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
                    
    prompt=st.text_area("Enter your prompt",height=200, max_chars=None, key=None)
    if st.button('Inspect and Modify Prompt',disabled=not (project_id)):
        if prompt:
            with st.spinner('Inspecting prompt...'):
                inspection_result = securityInspector(prompt)
            st.text_area('Inspection Result', inspection_result, height=200, max_chars=None, key=None)
            if inspection_result:
                with st.spinner('Creating Safe Prompt...'):
                    safe_prompt = safePromptSuggester(inspection_result)
                displaySafePrompt(safe_prompt)
        else:
            st.markdown("Please enter a prompt.")
with tab3:
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

    user_input = st.text_area("Please enter the desired GCP operation",height=200, max_chars=None, key=None)

    if st.button('Generate GCP CLI Command',disabled=not (project_id)):
        if user_input:
            with st.spinner('Generating command...'):
                gcp_command = gcpCliCommandGenerator(user_input)
            display_gcp_command(gcp_command)
        else:
            st.markdown("No command generated. Please enter a valid GCP operation.")
with tab4:
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

    description = st.text_area("Please enter the description of the desired architecture on GCP",height=200, max_chars=None, key=None)
    if st.button('Generate Terraform Files',disabled=not (project_id)):

        if description:
            terraform_files = terraformGenerator(description)
            display_terraform_files(terraform_files)
        else:
            st.markdown("No description provided. Please enter a valid description.")
    else:
        terraform_files = ""
        # display_terraform_files(terraform_files)