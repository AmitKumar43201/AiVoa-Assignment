from dotenv import load_dotenv
import os
load_dotenv()

api = os.getenv("Groq_API_KEY")

from groq import Groq

client = Groq(
    api_key=api,
)