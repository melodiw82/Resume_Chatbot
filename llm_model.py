from prompts import *
from utils import *
from chains import *

from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory

import ast
import json


# FIXME This is a demo of project that works, but not well.
#  1.AMBIGUITY_PROMPT should be improved to have parts of resume that contains ambiguity.
#  2. Chat history is not necessary in this context since it asks questions based on history, but they are not related.
#  3. Another chain should be added to improve user's resume based on their ACCEPTED answer.

class ResumeChatMemory:
    def __init__(self):
        self.chat_history = ChatMessageHistory()

    def add_ai_question(self, topic: str, question: str):
        ai_message = AIMessage(content=f"Question for {topic}: {question}")
        self.chat_history.add_message(ai_message)

    def add_human_response(self, user_input: str):
        human_message = HumanMessage(content=user_input)
        self.chat_history.add_message(human_message)

    def get_memory_variables(self):
        return {"chat_history": self.chat_history.messages}


def ai_ask(ambiguity_str: str):
    ambiguity_dict = ast.literal_eval(ambiguity_str)
    question_chain = resume_improvement_chain()
    validation_chain = resume_validation_chain()

    memory = ResumeChatMemory()

    questions = {}
    for topic, description in ambiguity_dict.items():
        response = question_chain.invoke({
            "topic": topic,
            "description": description,
            "chat_history": memory.get_memory_variables()['chat_history']
        })

        asked_question = response.content
        memory.add_ai_question(topic, asked_question)

        while True:
            print(f"\n{asked_question}")

            user_input = input("> ").strip()
            validation_response = validation_chain.invoke({
                "asked_question": asked_question,
                "user_input": user_input
            })

            print("\nAI Validation:")
            print(validation_response.content)

            if "ACCEPT" in validation_response.content:
                memory.add_human_response(user_input)
                questions[topic] = user_input
                break
            else:
                print("Please provide a more relevant response.")

    print(json.dumps(questions, indent=2))


def main_func(pdf_path: str, job_description: str) -> dict:
    # resume_text = extract_text_from_pdf(pdf_path)
    # summarized_job_description = summarize_job_description(job_description)
    # ambiguity_str = check_ambiguity(resume_text, summarized_job_description)
    ambiguity_str = """{
        "Main Technical Skills": "SQL and Python are mentioned, but R is not included. If experienced with R, add it; otherwise, consider learning it.",
        "Data Visualization Tools": "Power BI is listed, but Tableau is not mentioned. If familiar with Tableau, include that experience; if not, consider gaining basic knowledge.",
        "Experience Alignment": "The resume states a B.S. in Computer Engineering, which is not directly in Data Science. Emphasize any relevant coursework or projects that align with data analysis and visualization.",
        "Data Analysis Experience": "The resume mentions data analysis in projects but lacks specific examples of data analysis tasks or methodologies used. Include more details on data analysis experiences.",
        "Soft Skills": "Soft skills are mentioned but lack specific examples. Provide instances demonstrating detail orientation, analytical skills, and collaboration in team settings.",
        "Communication Skills": "While communication is listed as a soft skill, there are no specific examples of how these skills were applied in teaching or teamwork. Include examples of effective communication in your roles."
    }"""
    ai_ask(ambiguity_str)

    return {
        # "Resume Text": resume_text,
        # "Job Description": summarized_job_description,
        "Ambiguity": ambiguity_str
    }
