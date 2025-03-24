from prompts import *
from utils import *
from chains import *

from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory

import ast
import json


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
    enhancement_chain = resume_enhancement_chain()

    memory = ResumeChatMemory()

    enhanced_resume = {}
    for topic, details in ambiguity_dict.items():
        for entry in details:
            description = entry["description"]
            resume_text = entry["resume_text"]

        response = question_chain.invoke({
            "topic": topic,
            "description": description,
            "chat_history": memory.get_memory_variables()['chat_history']
        })

        asked_question = response.content
        # memory.add_ai_question(topic, asked_question)

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
                # memory.add_human_response(user_input)
                enhancement_response = enhancement_chain.invoke({
                    "resume_text": resume_text,
                    "user_input": user_input,
                    "topic": topic
                })

                enhanced_resume[topic] = {
                    "original": resume_text,
                    "enhanced": enhancement_response.content
                }

                print("\nEnhanced:")
                print(enhancement_response.content)
                break
            else:
                print("Please provide a more relevant response.")

    return enhanced_resume


def main_func(pdf_path: str, job_description: str) -> dict:
    # resume_text = extract_text_from_pdf(pdf_path)
    # summarized_job_description = summarize_job_description(job_description)
    # ambiguity_str = check_ambiguity(resume_text, summarized_job_description)
    ambiguity_str = """{
  "Soft Skills": [
    {
      "description": "Soft skills are mentioned but lack specific examples of how they were applied in projects or work experience.",
      "resume_text": "Soft Skills: Problem-solving, Time Management, Adaptability, Communication (English)"
    }
  ],
  "Experience": [
    {
      "description": "Experience in data analysis is not explicitly highlighted. The internship covers data science, but specific analytical tasks related to business insights or reporting are missing.",
      "resume_text": "Intern - Data Science Task-Oriented Bootcamp: Demonstrated proficiency in Python, SQL, deep learning and machine learning algorithms, linear algebra, data visualization using Power BI, and probability and statistics."
    }
  ],
  "Projects": [
    {
      "description": "Projects involve data analysis but do not specify key outcomes, metrics, or business impact. A more direct connection to decision-making insights would strengthen alignment.",
      "resume_text": "Phone Analysis - GSMarena Website: Analyzed smartphone specs from GSMarena for market trends, brand preferences, and tech advancements."
    }
  ],
  "Data Visualization": [
    {
      "description": "Experience with Power BI is mentioned, but no specific dashboard creation or stakeholder reporting is detailed.",
      "resume_text": "Skills: Tools & Technologies - Power BI"
    }
  ],
  "Communication": [
    {
      "description": "While communication is listed as a skill, there are no examples of written reports, presentations, or stakeholder interactions.",
      "resume_text": "Soft Skills: Communication (English)"
    }
  ]
}
"""
    ai_ask(ambiguity_str)

    return {
        # "Resume Text": resume_text,
        # "Job Description": summarized_job_description,
        "Ambiguity": ambiguity_str
    }
