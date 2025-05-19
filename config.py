from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4.1-mini"
OUTPUT_FILE = "data/synthetic_data.csv"
NUM_SAMPLES = 300
