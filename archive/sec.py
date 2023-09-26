import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from langchain.chains.summarize import load_summarize_chain
import tempfile
from langchain.docstore.document import Document

def load_module(module_path):
    loader = TextLoader(module_path) # Select the appropriate Loader
    docs = loader.load()
    return docs

def terraformScanner(module_string):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0
    )
    system_template = """You are a security assistant designed to scan for vulnerabilities in the provided terraform module string content."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please scan the following terraform module string for any potential vulnerabilities: '{module_string}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(module_string=module_string)
    return result # returns string   

def display_vulnerabilities(vulnerabilities):
    if vulnerabilities:
        st.markdown(f"**Vulnerabilities Found:** {vulnerabilities}")
    else:
        st.markdown("No vulnerabilities found.")

st.title('Scan for vulnerabilities')

uploaded_file = st.file_uploader("Upload Terraform Module File", type=["tf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        module_path = temp_file.name
        st.session_state['module_path'] = module_path
else:
    st.session_state['module_path'] = ""

if 'module_path' in st.session_state and st.session_state['module_path']:
    module_doc = load_module(st.session_state['module_path'])
else:
    module_doc = []

module_string = "".join([doc.page_content for doc in module_doc]) if module_doc else ""

if st.button('Scan for vulnerabilities'):
    if module_string:
        vulnerabilities = terraformScanner(module_string)
    else:
        vulnerabilities = ""

    display_vulnerabilities(vulnerabilities)