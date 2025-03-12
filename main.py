from llm_model import main_func
from prompts import JOB_DESCRIPTION

if __name__ == "__main__":
    PDF_PATH = "Rafiei.pdf"
    results = main_func(PDF_PATH, JOB_DESCRIPTION)

    # print("\nAmbiguity:")
    # print(results["Ambiguity"])
