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
    
 

