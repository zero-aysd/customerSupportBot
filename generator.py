import openai
from openai import OpenAI
import random
import time
from tqdm import tqdm
import pandas as pd
from config import OPENAI_API_KEY, MODEL_NAME

print(MODEL_NAME)

api_key = OPENAI_API_KEY
client = OpenAI(api_key=api_key)
PERSONAS = [
    "polite user", "frustrated user", "confused first-time user",
    "angry user", "non-native speaker"
]

CATEGORIES = [
    "Billing", "Account Access", "Product Inquiry", "Refund/Returns",
    "Shipping/Delivery", "Technical Issue", "Subscription Management"
]

def build_prompt(persona, category):
    return f"""
You are simulating a customer support conversation.

Persona: {persona}
Category: {category}

Generate a realistic customer query and an appropriate helpful, empathetic support response.
Return format:
Customer: <customer_query>
Support: <bot_response>
"""

def generate_example(persona, category):
    prompt = build_prompt(persona, category)
    # try:
    if 1:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        content = response.choices[0].message.content.strip()
        if "Customer:" in content and "Support:" in content:
            customer_query = content.split("Customer:")[1].split("Support:")[0].strip()
            bot_response = content.split("Support:")[1].strip()
            return {
                "persona": persona,
                "category": category,
                "customer_query": customer_query,
                "bot_response": bot_response
            }
    # except Exception as e:
    #     print(f"Error generating example: {e}")
    # return None

def generate_dataset(num_samples):
    data = []
    for _ in tqdm(range(num_samples), desc="Generating Examples"):
        persona = random.choice(PERSONAS)
        category = random.choice(CATEGORIES)
        result = generate_example(persona, category)
        if result:
            data.append(result)
        time.sleep(0.6)  # To stay within rate limits
    return pd.DataFrame(data)
