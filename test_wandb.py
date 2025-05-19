import random
import wandb
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create OpenAI client using API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize wandb run
run = wandb.init(
    entity="aayush-drishte-tredence",
    project="LLMOPS_CUSTOMER_SUPPORT_CHATBOT",
    config={
        "model": "gpt-4.1-nano",
        "temperature": 0.5,
        "prompt": "You are a helpful customer support assistant. How can I reset my password?",
        "test_type": "OpenAI API + wandb logging",
    },
)

# Call OpenAI API
completion = client.chat.completions.create(
    model=run.config["model"],
    messages=[
        {"role": "user", "content": run.config["prompt"]}
    ],
    temperature=run.config["temperature"]
)

# Extract and print result
response_text = completion.choices[0].message.content


print("Response:", response_text)
print("Usage:", usage)

# Log to wandb
run.log({
    "response": response_text,
    "prompt_tokens": usage.get("prompt_tokens", 0),
    "completion_tokens": usage.get("completion_tokens", 0),
    "total_tokens": usage.get("total_tokens", 0),
})

# End wandb run
run.finish()
