from langchain import LLMChain
import streamlit as st
from prompts import PROMPT_IMPROVER_PROMPT
from  initialization import initialize_llm


# Set up Streamlit Interface
st.sidebar.write("Project ID: landing-zone-demo-341118") 
project_id="landing-zone-demo-341118"
region=st.sidebar.selectbox("Please enter the region",['us-central1'])
model_name = st.sidebar.selectbox('Enter model name',['text-bison','text-bison-32k','code-bison','code-bison-32k'])
max_tokens = st.sidebar.number_input('Enter max token output',min_value=1,max_value=8192,step=100,value=1024)
temperature = st.sidebar.number_input('Enter temperature',min_value=0.0,max_value=1.0,step=0.1,value=0.1)
top_p = st.sidebar.number_input('Enter top_p',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
top_k = st.sidebar.number_input('Enter top_k',min_value=1,max_value=40,step=1,value=40)

# with st.container():
st.markdown("""## Prompt Improver:""")
# initial_prompt = st.text_input(label="Prompt Input", label_visibility='collapsed', placeholder="Generate a workout schedule", key="prompt_input")
initial_prompt = st.text_input("Please enter your prompt here:")

# Initialize LLM
llm = initialize_llm(project_id,region,model_name,max_tokens,temperature,top_p,top_k)
        
# Initialize LLMChain
prompt_improver_chain = LLMChain(llm=llm, prompt=PROMPT_IMPROVER_PROMPT)

# Run LLMChain
if st.button('Generate Improved Prompt',disabled=not (project_id) or not (initial_prompt)):
    if initial_prompt:
        with st.spinner("Generating Improved Prompt..."):
            improved_prompt = prompt_improver_chain.run(initial_prompt)
            st.markdown("""
                            ## Improved Prompt:
                            """)
            st.code(improved_prompt)
    else:
        st.error(f"Please provide a prompt")      


    