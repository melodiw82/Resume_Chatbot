import PyPDF2


def summarize_job_description(job_description: str):
    summarize_input = f"Job Description:\n{job_description}"
    messages = [
        SystemMessage(content=SUMMARIZE_JOB_DESCRIPTION),
        HumanMessage(content=summarize_input),
    ]
    response = llm.invoke(messages)
    return response.content


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def check_ambiguity(resume_text: str, summarized_job_description: str):
    ambiguity_input = f"Resume Text:\n{resume_text}\n\nJob Description:\n{summarized_job_description}"
    messages = [
        SystemMessage(content=AMBIGUITY_PROMPT),
        HumanMessage(content=ambiguity_input),
    ]
    response = llm.invoke(messages)
    return response.content
