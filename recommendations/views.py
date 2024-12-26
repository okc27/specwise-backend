from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import json
from langchain import PromptTemplate, LLMChain
from langchain_huggingface import HuggingFaceEndpoint
from huggingface_hub import login
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# HuggingFace API Key and login
sec_key = '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'
#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
login(sec_key)
os.environ["HUGGINGFACE_API_TOKEN"] = sec_key

# HuggingFace model details
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id=repo_id, temperature=0.1, model_kwargs={'max_length': 200, 'token': sec_key})

# Utility functions
def clean_text_output(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    return text.strip()

def clean_field(field):
    field = re.sub(r'[^\w\s]+$', '', field)
    field = re.sub(r'\d+$', '', field)
    return field.strip()

# Function to classify query as hardware recommendation-related or not
def is_hardware_related(question):
    template = """
    You are a PC hardware recommendation classifier. Answer 'Yes' if the question explicitly requests PC hardware recommendations. Otherwise, answer 'No'.

    Make sure to consider the following:
    - Questions in which the user defines their task related to PC and wants a setup recommendation to perform this task should be classified as 'Yes'.
    - Questions that focus on **technical concepts** (e.g., "How SSDs work", "CPU thermal throttling", "Effect of Any Hardware", "asks about hardware performance", "asks about Importance of component") should be classified as 'No'.

    Examples:
    - "What GPU should I buy for gaming?" -> Yes
    - "How does an SSD work?" -> No
    - "Does faster RAM improve FPS in games?" -> No

    Question: {question}
    Answer:
    """
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.invoke({"question": question})
    return response.get('text', '').strip().lower()

# Function to extract recommendation details
def extract_recommendation_details(question):
    template = """
    You are an expert in analyzing hardware recommendation questions. Extract the following information from the user's question:
    1. Software Name: Identify any specific software mentioned if any software name is written wrong so give the nearest software that it can be according to the nature of given question.
    2. Task to perform: Determine the user's main task (e.g., gaming, rendering, design).
    3. Hardware Mentioned : List any hardware components mentioned among (GPU, SSD, CPU, RAM, Motherboard, Powersupply) these so use them although if no hardware is mentioned or it refer general term like "Pc" or "hardware" among these, consider it as a complete PC and list it as "PC".
    4. Special Task (if any) either "None": Extract any mention of special tasks like large-scale projects, high-resolution graphics, fast rendering speeds.

    Question: {question}
    Response:
    Strictly avoid providing any additional information, explanations, or details beyond these components.
    """
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.invoke({"question": question})
    extracted_text = clean_text_output(response.get('text', '').strip())
    software_name = re.search(r'Software Name: (.*?)(?= Task to perform:)', extracted_text, re.IGNORECASE)
    task_to_perform = re.search(r'Task to perform: (.*?)(?= Hardware Mentioned:)', extracted_text, re.IGNORECASE)
    hardware_mentioned = re.search(r'Hardware Mentioned: (.*?)(?= Special Task:)', extracted_text, re.IGNORECASE)
    special_task = re.search(r'Special Task: (.*)', extracted_text, re.IGNORECASE)
    return {
        "Software Name": clean_field(software_name.group(1)) if software_name else "None",
        "Task to Perform": clean_field(task_to_perform.group(1)) if task_to_perform else "None",
        "Hardware Mentioned": clean_field(hardware_mentioned.group(1)) if hardware_mentioned else "PC",
        "Special Task": clean_field(special_task.group(1)) if special_task else "None"
    }

# Utility functions to clean text and parse LLM output
def clean_text(text):
    text = re.sub(r'\d+\.\s+', '', text)  # Remove numbers followed by a dot
    text = re.sub(r'-\s+', '', text)  # Remove dashes
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def parse_llm_output(llm_output):
    lines = llm_output.strip().split("\n")
    structured_output = {
        "option1": clean_text(lines[0]) if len(lines) > 0 else None,
        "option2": clean_text(lines[1]) if len(lines) > 1 else None,
        "note": clean_text(" ".join(lines[2:])) if len(lines) > 2 else None
    }
    return structured_output

# Function to recommend hardware based on extracted details
def recommend_hardware_with_llm(extracted_details, recommendation_type):
    if recommendation_type not in ["minimum", "suitable"]:
        raise ValueError("Invalid recommendation type. Choose 'minimum' or 'suitable'.")

    recommendations = {
        "Software Name": extracted_details.get("Software Name", "None"),
        "Task to Perform": extracted_details.get("Task to Perform", "None"),
        "Hardware Mentioned": extracted_details.get("Hardware Mentioned", "PC"),
        "Special Task": extracted_details.get("Special Task", "None")
    }

    hardware_types = recommendations["Hardware Mentioned"].split(", ")
    if len(hardware_types) == 1 and hardware_types[0].lower() == "pc":
        hardware_types = ["CPU", "GPU", "RAM", "SSD", "Motherboard", "Power Supply"]

    llm_recommendations = {}

    for hardware in hardware_types:
        template_text = f"""
        You are an expert in PC hardware recommendations. Based on the following details:
        - Software Name: {{software_name}}
        - Task to Perform: {{task_to_perform}}
        - Special Task: {{special_task}}
        
        Recommend a list of only 2 different options {{hardware}} components {recommendation_type} required for these requirements.
        Provide only the list of hardware without any explanations.
        """
        prompt = PromptTemplate(
            template=template_text,
            input_variables=["software_name", "task_to_perform", "special_task", "hardware"]
        )
        llm_chain = LLMChain(prompt=prompt, llm=llm)

        try:
            response = llm_chain.invoke({
                "software_name": recommendations["Software Name"],
                "task_to_perform": recommendations["Task to Perform"],
                "special_task": recommendations["Special Task"],
                "hardware": hardware
            })
            llm_output = response.get('text', '').strip()
            llm_recommendations[hardware] = parse_llm_output(llm_output)
        except Exception as e:
            print(f"Error during LLM invocation for {hardware}: {str(e)}")
            llm_recommendations[hardware] = {
                "option1": "Error",
                "option2": "Error",
                "note": str(e)
            }

    return llm_recommendations




@api_view(['POST'])
def classify_query(request):
    """
    API to classify if a question is hardware recommendation-related.
    """
    try:
        question = request.data.get("question", "").strip()
        if not question:
            return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Classify the query
        result = is_hardware_related(question)
        
        return Response({
            "question": question,
            "is_hardware_related": result
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
def question_details(request):
    """
    API to extract hardware recommendation details if the query is hardware-related.
    """
    try:
        question = request.data.get("question", "").strip()
        if not question:
            return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        classification_result = is_hardware_related(question)
        if classification_result == "yes":
            recommendation_details = extract_recommendation_details(question)
            return Response({"question": question, "recommendation_details": recommendation_details}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "The question is not hardware recommendation-related."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API View to handle hardware recommendation request
@api_view(['POST'])
def hardware_recommendation(request):
    try:
        # Extract query details (This will be extracted through your existing logic or API)
        recommendation_details = request.data.get("recommendation_details", {})
        if not recommendation_details:
            return Response({"error": "Extracted details are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Define recommendation types
        recommendation_types = ["minimum", "suitable"]
        
        # Use ThreadPoolExecutor to run tasks in parallel for minimum and suitable recommendations
        with ThreadPoolExecutor() as executor:
            future_to_type = {
                executor.submit(recommend_hardware_with_llm, recommendation_details, rec_type): rec_type
                for rec_type in recommendation_types
            }

            results = {}
            for future in as_completed(future_to_type):
                rec_type = future_to_type[future]
                try:
                    results[rec_type] = future.result()
                except Exception as e:
                    print(f"Error with {rec_type} recommendation: {str(e)}")
        
        return Response({
            "recommendations": results
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)