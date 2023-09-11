from langchain.llms import VertexAI

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