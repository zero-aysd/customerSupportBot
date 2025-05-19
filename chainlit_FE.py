import chainlit as cl
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("FEURL")  # Adjust if hosted elsewhere

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hi! I'm your Customer Support Bot with Guardrails!").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_query = message.content

    # Call FastAPI backend
    try:
        response = requests.post(API_URL, json={"query": user_query})
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        result = response.json()
        print(result)
        #await cl.Message(content=f"❌ Error contacting backend: {e}").send()
        # return

    # # Check guardrail results
    # if result.get("query_guardrail", {}).get("issues"):
    #     summary = result["query_guardrail"]["summary"]
    #     await cl.Message(content=f"⚠️ Prompt Rejected due to guardrail violation:\n\n**{summary}**").send()
    #     return

    # Send chatbot response
    bot_response = result.get("response", "🤖 (No response)")
    await cl.Message(content=bot_response).send()

    # # Show evaluation and metadata
    # eval_data = result.get("evaluation", {})
    # query_gr = result.get("query_guardrail", {})
    # resp_gr = result.get("response_guardrail", {})
    # cost = result.get("cost_usd", 0.0)
    # latency_query = result.get("latency_query", 0.0)
    # latency_eval = result.get("latency_eval", 0.0)

    # # Optional rich metadata display
    # await cl.Message(
    #     author="system",
    #     content="📊 *Metadata & Evaluation*",
    #     elements=[
    #         cl.Text(name="Evaluation", content=str(eval_data)), 
    #         cl.Text(name="Query Guardrails", content=str(query_gr)),
    #         cl.Text(name="Response Guardrails", content=str(resp_gr)),
    #         # cl.Text(
    #         #     name="Usage Info",
    #         #     content=f"💰 Cost: ${cost:.6f}\n⚡ Latency: Query {latency_query:.2f}s | Eval {latency_eval:.2f}s"
    #         # )
    #     ]
    # ).send()
