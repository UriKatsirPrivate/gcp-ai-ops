import os
from langchain.llms import VertexAI
from google.cloud import secretmanager
import streamlit as st

# Initialize LLM
def initialize_llm(project_id,region,model_name,max_output_tokens,temperature,top_p,top_k):
    
    # Initialize VertexAI and set up the LLM
    return VertexAI(
        project=project_id,
        location=region,
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        verbose=True,
    )

# Initialize Tracing
def initialize_tracing(tracing,endpoint,langsmith_key,langsmith_project):
    # print("tracing = " + str(tracing))
    # print("endpoint = " + endpoint)
    os.environ["LANGCHAIN_TRACING_V2"]=str(tracing)
    os.environ["LANGCHAIN_ENDPOINT"] =endpoint
    os.environ["LANGCHAIN_API_KEY"] = langsmith_key
    os.environ["LANGCHAIN_PROJECT"] = langsmith_project

def get_from_secrets_manager(secret_name,project_id,langsmith_key):

    # print("key= " + str(langsmith_key))

    if langsmith_key=="":

        # print("token")
        client = secretmanager.SecretManagerServiceClient()

        # name = f"projects/{PROJECT_ID}/secrets/langchain-api-key/versions/1"
        name = f"projects/{project_id}/secrets/{secret_name}/versions/1"

        # Access the secret version.
        response = client.access_secret_version(request={"name": name})

        # Extract the payload.
        payload = response.payload.data.decode("UTF-8")

        return payload