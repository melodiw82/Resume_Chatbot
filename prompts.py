RESUME_EXTRACTION_PROMPT = """You are an AI assistant specialized in analyzing resumes.
Extract and structure the key sections as follows:
- Name
- Contact information
- Education
- Work History
- Skills
- Projects
- Certifications
- Volunteering
- Languages
- Hobbies and Interests

Return the structured output in JSON format.
Summarize long descriptions of the resume.
Only include sections that are explicitly mentioned in the resume. If a section does not exist, do not include it in the output.
"""

SUMMARIZE_JOB_DESCRIPTION = """
You are an AI assistant that summarizes key points of a job description.
Analyze the job description and extract key details based on the following categories:
Main Technical Skills 
Preferred Skills 
Experience 
Soft Skills 
Ensure the summary is clear, concise, and maintains the original intent of the job description.
Return your output in JSON format.
"""

SIMILARITY_PROMPT = """
You are an AI assistant that compares a resume summary with a job description.
Identify the key similarities and dissimilarities between the resume and the job requirements.
Return your output in JSON format with two keys in four categories: 1. Main Technical Skills 2. Soft Skills 3. Experience 4. Preferred Skills
  - "Similarities"
  - "Dissimilarities"
Ensure the Similarities and Dissimilarities are clear, concise, and maintain the original intent of the job description.
If Job description does not include a category, do not include them in the output.
"""

SECTION_SCORING_PROMPT = """
You are an AI assistant that evaluates how well a resume matches a job description by scoring specific sections.
For each of the following sections:
  - Main Technical Skills
  - Soft Skills
  - Experience
  - Preferred Skills
assign a score from 1 to 10 based on the resume content and its alignment with the job description.
Deduct and Add points reasonably based on similarities and dissimilarities given to you.
If a section does not exist in the resume, do not include it in the output.
Return your output in Dictionary format without anything else, for example:
{
  "Main Technical Skills": 9,
  "Soft Skills": 7,
  "Experience": 8,
  "Preferred Skills": 6
}
"""

JOB_DESCRIPTION = """
Job Title: Data Analyst

Company: DataInsights Inc.

Location: NY, remote is possible

About DataInsights Inc.:
DataInsights Inc. is a leading provider of data-driven solutions, specializing in transforming complex datasets into actionable business strategies. We are committed to innovation and excellence, helping our clients make informed decisions.

Job Overview:
We are seeking a detail-oriented Data Analyst to join our team. The successful candidate will be responsible for collecting, processing, and analyzing data to support data-driven decision-making.

Key Responsibilities:
- Collect and process data from various sources to ensure accuracy and completeness.
- Analyze datasets to identify trends and patterns.
- Develop and maintain reports and dashboards for stakeholders.
- Collaborate with teams to understand data needs and provide insights.
- Ensure data quality and integrity through regular audits.

Qualifications:
- Bachelor's degree in Data Science, Statistics, Computer Science, or related field.
- Proficiency in data analysis tools such as SQL, Python, or R.
- Experience with data visualization tools like Tableau or Power BI.
- Strong analytical and problem-solving skills.
- Excellent communication skills.

Benefits:
- Competitive salary and performance-based incentives.
- Comprehensive health insurance.
- Opportunities for professional development.
- Flexible work environment.
"""

CHECK_COMPLETENESS = """
You are an expert resume reviewer specializing in clarity and completeness. Your task is to analyze the provided resume text and identify vague or unclear sections that need further elaboration. Specifically, point out:

    - Ambiguous Descriptions: Identify experiences, skills, or achievements that lack specific details (e.g., missing numbers, impact, or context).
    - Unclear Job Roles: Highlight job titles or responsibilities that do not clearly describe what the candidate did.
    - Incomplete Information: Find areas where additional details (e.g., project scope, technologies used, or quantifiable outcomes) would strengthen the resume.
    - Generic Statements: Point out phrases that are too broad or overused, suggesting ways to make them more specific.
    - Weak Action Verbs: Identify where stronger, more impactful verbs could be used.
    
For each vague section, explain why it needs clarification and suggest how to improve it with specific examples or details.
"""
