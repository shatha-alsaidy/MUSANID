import streamlit as st
from langchain_groq import ChatGroq

@st.cache_resource
def initializeLLM():
    groq_api_key = st.secrets["GROQ_API_KEY"]

    # Initialize the Groq LLM
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.1-8b-instant"
    )

    return llm

def make_prompt_for_patient_summary(
    name: str,
    age: int,
    sex: str,
    diagnosis: str,
    severity: str,
    treatment_plan: str,
    therapist_notes: str
) -> str:
    """
    Build a system/user prompt to ask the LLM to generate a comprehensive patient summary
    for the therapist based on personal info, diagnosis, severity, treatment plan, and notes.
    """
    prompt = (
        "<|start_header_id|>user<|end_header_id|>"
        "You are a clinical assistant supporting a licensed therapist.\n\n"
        "Patient Information:\n"
        "Name: {name}\n"
        "Age: {age}\n"
        "Sex: {sex}\n\n"
        "Clinical Information:\n"
        "Diagnosis: {diagnosis}\n"
        "Severity: {severity}\n"
        "Treatment Plan: {treatment_plan}\n"
        "Therapist Notes: {therapist_notes}\n\n"
        "Task:\n"
        "Write a professional, concise, and comprehensive patient summary suitable for a therapist. "
        "Include relevant personal details, clinical status, key points from the treatment plan, "
        "and important observations from the therapist's notes. "
        "Structure the summary with clear headings and bullet points for easy reading. "
        "Do NOT add unrelated advice or extra instructions. "
        "Output ONLY the summary text.\n"
        "<|end_header_id|>"
        "<|start_header_id|>assistant<|end_header_id|>"
    )
    
    return prompt.format(
        name=name,
        age=age,
        sex=sex,
        diagnosis=diagnosis,
        severity=severity,
        treatment_plan=treatment_plan,
        therapist_notes=therapist_notes
    )

def generate(prompt):
   # Generate text using LLM.
    llm = initializeLLM()
    
    response = llm.invoke(prompt) 

    # Extract text first
    if hasattr(response, "content"):
        q = response.content
    else:
        q = str(response)
    # Then cleanup like before
    q = q.strip().splitlines()[0].strip()
    return q 


def generate_summary(
    name: str,
    age: int,
    sex: str,
    diagnosis: str,
    severity: str,
    treatment_plan: str,
    therapist_notes: str) -> str:
    
    # Generate a comprehensive patient summary using the LLM.

    # Build the prompt
    prompt = make_prompt_for_patient_summary(
        name=name,
        age=age,
        sex=sex,
        diagnosis=diagnosis,
        severity=severity,
        treatment_plan=treatment_plan,
        therapist_notes=therapist_notes
    )

    # Generate summary
    summary = generate(prompt)  # returns string

    return summary
