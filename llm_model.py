from prompts import *

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import ast
import PyPDF2
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
    openai_api_key=openai_api_key
)

default_weights = {
    "Main Technical Skills": 0.4,
    "Soft Skills": 0.2,
    "Experience": 0.3,
    "Preferred Skills": 0.1
}

memory = ConversationBufferMemory()

def extract_resume_topics(resume_text: str):
    messages = [
        SystemMessage(content=RESUME_EXTRACTION_PROMPT ),
        HumanMessage(content=resume_text),
    ]
    response = llm.invoke(messages)
    return response.content

def summarize_job_description(job_description: str):
    summarize_input = f"Job Description:\n{job_description}"
    messages = [
        SystemMessage(content=SUMMARIZE_JOB_DESCRIPTION),
        HumanMessage(content=summarize_input),
    ]
    response = llm.invoke(messages)
    return response.content

def compare_similarity(resume_summary: str, summarized_job_description: str):
    comparison_input = f"Resume Summary:\n{resume_summary}\n\nJob Description:\n{summarized_job_description}"
    messages = [
        SystemMessage(content=SIMILARITY_PROMPT),
        HumanMessage(content=comparison_input),
    ]
    response = llm.invoke(messages)
    return response.content

def section_scoring(resume_similarity: str):
    section_input = f"Resume Similarity Dissimilarity:\n{resume_similarity}"
    messages = [
        SystemMessage(content=SECTION_SCORING_PROMPT),
        HumanMessage(content=section_input),
    ]
    response = llm.invoke(messages)
    return response.content

def compute_weighted_average(section_scores: str, weights: dict):
    available_weights = {section: weight for section, weight in weights.items() if section in section_scores}
    total_weight = sum(available_weights.values())

    if total_weight == 0:
        return 0.0

    normalized_weights = {section: weight / total_weight for section, weight in available_weights.items()}

    section_scores = ast.literal_eval(section_scores)
    section_scores = {section: int(score) for section, score in section_scores.items()}
    weighted_sum = sum(section_scores[section] * normalized_weights[section] for section in normalized_weights)
    return weighted_sum

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def chatbot():
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            break

        past_data = memory.load_memory_variables({}).get("history", "")
        messages = [
            SystemMessage(content="""You are a concise and precise AI assistant specialized in resume analysis.  
            Upon welcoming the user, provide their average score and individual section scores.  
            Answer additional questions based on similarity analysis and expand on them if necessary since they are just a summary, ensuring responses are accurate and derived only from the provided data."""),
            HumanMessage(content=f"Past Data:\n{past_data}\n\nUser Question: {user_input}"),
        ]
        response = llm.invoke(messages)
        print(f"AI: {response.content}")

def main_func(pdf_path: str, job_description: str) -> dict:
    resume_text = extract_text_from_pdf(pdf_path)
    resume_summary = extract_resume_topics(resume_text)
    summarized_job_description = summarize_job_description(job_description)
    similarity_analysis = compare_similarity(resume_summary, summarized_job_description)
    section_scores = section_scoring(similarity_analysis)

    weighted_score = compute_weighted_average(section_scores, default_weights)

    memory.save_context(
        {"input": "Resume Analysis"},
        {
            "output": f"Similarity Analysis: {similarity_analysis}\n"
                      f"Section Scoring: {section_scores}\n"
                      f"Weighted Score: {weighted_score}"
        }
    )

    result = {
        "Resume Summary": resume_summary,
        "Similarity Analysis": similarity_analysis,
        "Section Scores": section_scores,
        "Weighted Score": weighted_score,
        "Summarized Job Description": summarized_job_description,
    }

    return  result
