from llm_model import main_func, chatbot
from prompts import JOB_DESCRIPTION

if __name__ == "__main__":
    PDF_PATH = "Rafiei.pdf"
    results = main_func(PDF_PATH, JOB_DESCRIPTION)

    print("Resume Summary:")
    print(results["Resume Summary"])

    print("\nSummarized Job Description:")
    print(results["Summarized Job Description"])

    print("\nSimilarity Analysis:")
    print(results["Similarity Analysis"])

    print("\nSection Scores:")
    print(results["Section Scores"])

    print("\nWeighted Score:")
    print(results["Weighted Score"])

    print("\nCompleteness:")
    print(results["Completeness"])

    if results:
        chatbot()
