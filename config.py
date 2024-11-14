import os
from dotenv import load_dotenv

def load_config():
    """
    Load environment variables from the .env file and return the Groq API key.
    """
    load_dotenv()  
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment variables.")
    
    return groq_api_key
