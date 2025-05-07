import os

def get_config():
    return {
        "user_agent": os.getenv("USER_AGENT"),
        "groq_api_key": os.getenv("GROQ_API_KEY"),
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "pdf_path": os.getenv("PDF_PATH")
    }
