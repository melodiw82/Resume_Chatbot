from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
    openai_api_key=openai_api_key
)


def resume_improvement_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an AI assistant helping users improve their resumes.
        Based on the topic '{topic}', and the description '{description}',
        ask the user a relevant question to help them provide more details for their resume. 
        Keep the question short so it's easy to answer.
        You will be conversing interactively, so ensure your response is framed to gather further details."""),
        MessagesPlaceholder(variable_name="chat_history"),
    ])

    chain = (
            RunnablePassthrough.assign(
                chat_history=lambda inputs: inputs.get('chat_history', [])
            )
            | prompt
            | llm
    )

    return chain


def resume_validation_chain():
    validation_prompt = ChatPromptTemplate.from_messages([
        ("system", """Evaluate whether {user_input} is relevant to {asked_question}.

    **Response Criteria:**
    - **"ACCEPT"** if the input has any connection, even indirect or minimal, to any part of the question.
    - **"REJECT"** only if the input has absolutely no conceivable link to the question.
    - When in doubt, **lean toward ACCEPT** rather than rejecting valid but brief responses.

    **Guidelines:**
    - Consider synonyms, implications, or loosely related topics.
    - Even a single word or phrase that touches on the topic should be accepted.
    - If relevance is vague but possible, err on the side of acceptance.

    **Response Format:**
    - **ACCEPT** or **REJECT**
    - A very short explanation justifying your decision.
    """),
        ("human", "Question: {asked_question}\nUser Input: {user_input}")
    ])

    validation_chain = validation_prompt | llm

    return validation_chain


def resume_enhancement_chain():
    enhancement_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert resume editor. 
            Enhance the existing resume text by incorporating the new user input.

            Guidelines:
            - Maintain the original resume's tone and style
            - Use action verbs and quantifiable achievements
            - Ensure the new text is concise and impactful
            - Highlight the most impressive aspects of the input
            - Do not make stuff up and only use user input.
            - Summarize the key points if you have to.

            Current Resume Text: {resume_text}
            New Information to Incorporate: {user_input}
            Topic: {topic}
            """),
    ])

    enhancement_chain = enhancement_prompt | llm

    return enhancement_chain
