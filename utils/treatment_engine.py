import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq


@st.cache_resource
def initializeLLM():
    groq_api_key = st.secrets["GROQ_API_KEY"]

    # Initialize the Groq LLM
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.1-8b-instant")

    return llm

@st.cache_resource
def load_vectordb(persist_dir: str = "../chroma_db", top_k: int = 15):
    print(f"Restoring Chroma DB")

    embedding_model = HuggingFaceEmbeddings(model_name="intfloat/e5-large-v2")

    # Load the Chroma database
    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": top_k})
    print(f"Chroma DB loaded and retriever ready (k={top_k})")

    return retriever

@st.cache_resource
def create_retrieval_chain(_retriever, llm):
    prompt_template = """
    <|start_header_id|>user<|end_header_id|>
    You are a clinical assistant supporting a licensed therapist.
    Draft a professional, evidence-based treatment plan **directly addressed to the therapist** for a patient.

    Guideline context:
    {context}

    Instructions for the treatment plan:
    1. Begin by stating the diagnosis and severity clearly.
    2. List treatment goals that are measurable and achievable.
    3. Provide detailed treatment recommendations, including:
        - Psychological interventions: specify type, frequency, duration, and objectives.
        - Medication guidance: applicable or not, if applicable specify class, typical examples, dose ranges, duration, and monitoring.
        - Safety considerations: e.g., side effect monitoring, suicide risk assessment, and follow-up schedule.
    4. Include additional considerations, such as lifestyle interventions, patient engagement, and escalation if the patient does not improve.
    5. Use clear, concise language suitable for a therapist.
    6. Do NOT repeat the guideline context or instructions.
    7. Structure the output with headings and bullet points for easy reading.

    Now draft the treatment plan.
    <|end_header_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    QA_PROMPT = PromptTemplate(template=prompt_template, input_variables=["context"])

    # Create RetrievalQA chain
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever= _retriever,
    chain_type_kwargs={"prompt": QA_PROMPT})

    print("RAG chain ready.")
    return qa

# Initialize the LLM
llm = initializeLLM()

# Load the Chroma vector database
retriever = load_vectordb("../chroma_db", top_k=15)

# Create the retrieval chain
qa_chain = create_retrieval_chain(retriever, llm)

def generate_treatment_plan(condition, severity):
    # Generate a treatment plan given a condition and severity
    query = f"treatment for {severity} {condition}"

    result = qa_chain.invoke({"query": query})
    plan = result["result"]

    return plan
