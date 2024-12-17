# backend/views.py
import re
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain_huggingface import HuggingFaceEndpoint
from huggingface_hub import login
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


# HuggingFace API Key and login
sec_key = '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'
login(sec_key)
os.environ["HUGGINGFACE_API_TOKEN"] = sec_key

# HuggingFace model details
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id=repo_id, temperature=0.5, model_kwargs={'max_length': 200, 'token': sec_key})

@api_view(['POST'])
def get_hardware_recommendations(request):
    question = request.data.get('question', '')
    
    # Prompt template for hardware recommendations
    template = """
    give the compatible hardware recommendations for my
    Question: {question}
    Respond only with recommendations for the following components: 'CPU', 'GPU'(if necessary), 'RAM', 'SSD', 'HDD', 'Motherboard', and 'Power Supply'. Provide 2 most popular options from different companies if available. Avoid providing any additional information, explanations, or details beyond these components.
    """
    
    # Create the prompt and LLM chain for hardware recommendations
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    
    # Invoke the chain to get hardware recommendations
    response = llm_chain.invoke(question)
    
    # Extract the text from the response dictionary
    response_text = response.get('text', '')
    
    # Clean up and remove unnecessary prefixes
    response_text = response_text.replace('Answer:', '').strip()

    # Use a robust regex pattern to match each component and its value
    pattern = r"\d\.\s*(CPU|GPU|RAM|SSD|HDD|Motherboard|Power Supply):\s*\n\s*-\s*([^\n]+)\n\s*-\s*([^\n]+)"
    
    # Find all matches in the response
    matches = re.findall(pattern, response_text)

    # Convert matches to a dictionary
    hardware_dict = {}
    for component, option1, option2 in matches:
        hardware_dict[component] = [option1.strip(), option2.strip()]

    return Response(hardware_dict)

