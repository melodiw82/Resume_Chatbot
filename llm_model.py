from prompts import *

from langchain.chains import ConversationChain
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
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

memory = ConversationBufferMemory(memory_key='history', return_messages=True)

template = """
You are a precise AI assistant specialized in resume analysis.
Upon greeting the user, provide their average score along with individual section scores.
Use the similarity analysis to answer questions, expanding where necessary while ensuring accuracy.
Scoring breakdown:
- Main Technical Skills: 40%
- Soft Skills: 20%
- Experience: 30%
- Preferred Skills: 10%

Current conversation:{history}
Human: {input}
"""

prompt = PromptTemplate(input_variables=["history", "input"], template=template)

chain = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True
)


def extract_resume_topics(resume_text: str):
    messages = [
        SystemMessage(content=RESUME_EXTRACTION_PROMPT),
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

        response = chain.predict(input=user_input)
        print(f"AI: {response}")


def main_func(pdf_path: str, job_description: str) -> dict:
    resume_text = extract_text_from_pdf(pdf_path)
    resume_summary = extract_resume_topics(resume_text)
    summarized_job_description = summarize_job_description(job_description)
    similarity_analysis = compare_similarity(resume_summary, summarized_job_description)
    section_scores = section_scoring(similarity_analysis)

    weighted_score = compute_weighted_average(section_scores, {
        "Main Technical Skills": 0.4,
        "Soft Skills": 0.2,
        "Experience": 0.3,
        "Preferred Skills": 0.1
    })

    memory.save_context(
        {"input": "Resume Analysis"},
        {
            "output": f"Similarity Analysis: {similarity_analysis}\n"
                      f"Section Scoring: {section_scores}\n"
                      f"Weighted Score: {weighted_score}"
        }
    )

    return {
        "Resume Summary": resume_summary,
        "Similarity Analysis": similarity_analysis,
        "Section Scores": section_scores,
        "Weighted Score": weighted_score,
        "Summarized Job Description": summarized_job_description,
    }
