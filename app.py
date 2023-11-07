import os
import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from initialization import initialize_llm, initialize_tracing
import vertexai
from vertexai.preview.vision_models import Image, ImageGenerationModel
# from prompts import PROMPT_IMPROVER_PROMPT
from placeholders import *
from system_prompts import *

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

PROJECT_ID="landing-zone-demo-341118"
LANGSMITH_KEY_NAME="langchain-api-key"
REGIONS=["europe-west4","us-central1","us-west4","us-west1","us-east4","northamerica-northeast1","europe-west1","europe-west2","europe-west3","europe-west9"]
MODEL_NAMES=['text-bison','text-bison-32k','code-bison','code-bison-32k']

st.sidebar.write("Project ID: ",f"{PROJECT_ID}") 
project_id=PROJECT_ID
region=st.sidebar.selectbox("Please enter the region",REGIONS)
model_name = st.sidebar.selectbox('Enter model name',MODEL_NAMES)
max_tokens = st.sidebar.slider('Enter max token output',min_value=1,max_value=8192,step=100,value=1024)
temperature = st.sidebar.slider('Enter temperature',min_value=0.0,max_value=1.0,step=0.1,value=0.1)
top_p = st.sidebar.slider('Enter top_p',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
top_k = st.sidebar.slider('Enter top_k',min_value=1,max_value=40,step=1,value=40)

if not ('32k' in model_name) and max_tokens>1024:
  st.error(f'{max_tokens} output tokens is not a valid value for model {model_name}')

# Initialize tracing variables
tracing = st.sidebar.toggle('Enable Langsmith Tracing')
langsmith_endpoint = st.sidebar.text_input(label="Langsmith Endpoint", value="https://api.smith.langchain.com", disabled=not tracing)
langsmith_project = st.sidebar.text_input(label="Langsmith Project", value="GCP AI OPS", disabled=not tracing)

# Check if initialize_tracing() has already been called
if 'tracing_initialized' not in st.session_state:
    initialize_tracing(tracing,langsmith_endpoint,langsmith_project,PROJECT_ID,LANGSMITH_KEY_NAME)
    # Set the flag to indicate that initialize_tracing() has been called
    st.session_state.tracing_initialized = True

if tracing:
    os.environ["LANGCHAIN_TRACING_V2"]="True"
else:
    os.environ["LANGCHAIN_TRACING_V2"]="False"

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.15rem;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)
tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["Run Prompt / "
                                             , "Generate gCloud Commands / "
                                             ,"Generate Terraform /"
                                             ,"Inspect IaC /"
                                             ,"TF Converter /"
                                             ,"Images"
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
    
    if st.button('Execute Prompt'):
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
        human_template = """Please scan the following terraform module gcloud commands string for any potential vulnerabilities: '{module_string}'."""
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
        human_template = """Convert the following AWS Terraform to equivalent GCP Terraform: '{module_string}'."""
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
with tab6:
    def GenerateImagePrompt(description,number):
        
        system_template = GenerateImageSystemPrompt
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = f"""Please generate {number} prompts about: {description} ."""
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=llm, prompt=chat_prompt)
        result = chain.run(module_string=description)
        # print (f" result is: {result}")
        return result # returns string
    
    def GenerateImage(description,num_of_images):
        try:
            vertexai.init(project=project_id, location=region)

            # model = ImageGenerationModel.from_pretrained(model_name)
            model = ImageGenerationModel.from_pretrained("imagegeneration@002")
            images = model.generate_images(
            prompt=description,
            # Optional:
            number_of_images=num_of_images,
            # seed=1,
            )
            return images
        except:
            ""
    def display_images(images):
        for image in images:
            image.save(location="./gen-img1.png", include_generation_parameters=True)
            st.image("./gen-img1.png",use_column_width="auto")
   
    link="https://cloud.google.com/vertex-ai/docs/generative-ai/image/img-gen-prompt-guide"
    desc="Write your prompt below, See help icon for a prompt guide: (Images will be generated using the imagegeneration@002 model)"
    description = st.text_area(desc,height=200,key=55,placeholder=GENERATE_IMAGES,help=link)
    # num_of_images=st.number_input("How many images to generate",min_value=1,max_value=8,value=4)
    
    col1, col2 = st.columns(2,gap="large")
    with col1:
        with st.form(key='prompt_magic',clear_on_submit=False):
            num_of_prompts=st.number_input("How many prompts to generate",min_value=1,max_value=3,value=2)
            if st.form_submit_button('Generate Prompt(s)',disabled=not (project_id)):
                if description:
                    with st.spinner('Generating Prompt(s)...'):
                        improved_prompt = GenerateImagePrompt(description,num_of_prompts)
                    st.markdown(improved_prompt)
                else:
                    st.markdown("No prompts generated. Please enter a valid prompt.")        
    with col2:
        with st.form(key='prompt_magic1',clear_on_submit=False):                
        
            num_of_images=st.number_input("How many images to generate",min_value=1,max_value=8,value=4)
            if st.form_submit_button('Generate Image(s)',disabled=not (project_id)):
                if description:
                    with st.spinner('Generating Image(s)...'):
                        images = GenerateImage(description,num_of_images)
                        if images:
                            display_images(images)
                        else:
                           st.markdown("No images generated. Prompt was blocked.")     
                else:
                    st.markdown("No images generated. Please enter a valid prompt.")