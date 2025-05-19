import os
import uuid
import json
import time
import re
from typing import List

import openai
import wandb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv
from ChatbotPrompts import CUSTOMER_QUERIES, FINAL_PROMPT_TEMPLATE, EVAL_PROMPT_TEMPLATE, GUARDRAIL_DETECTOR_PROMPT

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")
eval_model = os.getenv("MODEL")
temperature = 0.7
eval_temperature=0
max_tokens=500

client = openai.OpenAI(api_key=api_key)

MODEL_PRICES = {
    "gpt-3.5-turbo": 0.0015,
    "gpt-4.1-mini": 0.00015,
    "gpt-4.1-nano": 0.00000525
}

# Schemas
class GuardrailResult(BaseModel):
    toxicity: bool
    profanity: bool
    prompt_injection: bool
    malicious_request:bool
    issues: List[str]
    summary: str

# class QueryRequest(BaseModel):
#     query: str
#     model: str = "gpt-4.1-mini"
#     eval_model: str = "gpt-4.1-mini"
#     temperature: float = 0.7
#     max_tokens: int = 500
class QueryInput(BaseModel):
    query: str
# App setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

run = wandb.init(
    project="llm-chatbot-guardrails-api",
    name="llm-app-api-run",
    save_code=True
)

# Init W&B Table
table = wandb.Table(columns=[
    "id", "query", "chatbot_response",
    "query_guardrail_summary", "query_issues",
    "response_guardrail_summary", "response_issues",
    "eval_scores", "eval_comments", "eval_overall",
    "tokens_prompt", "tokens_completion", "tokens_total",
    "cost_usd", "latency_query", "latency_eval"
])

# Utility functions
def call_chat(model, messages, temperature=0.7, max_tokens=500):
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    latency = time.time() - start
    usage = response.usage
    content = response.choices[0].message.content.strip()
    cost = (usage.prompt_tokens + usage.completion_tokens) / 1000 * MODEL_PRICES[model]
    return content, usage, cost, latency

def check_guardrails(text: str, model="gpt-4.1-mini") -> dict:
    prompt = GUARDRAIL_DETECTOR_PROMPT.format(text=text)
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=500
    )
    raw_content = response.choices[0].message.content.strip()
    cleaned = re.sub(r"^```json\n|\n```$", "", raw_content)

    try:
        result = GuardrailResult.model_validate_json(cleaned)
        return json.loads(result.model_dump_json())
    except ValidationError:
        return {
            "toxicity": False,
            "profanity": False,
            "prompt_injection": False,
            "malicious_request":False,
            "issues": ["Pydantic parsing error"],
            "summary": "Invalid JSON format from guardrail LLM"
        }

# @app.post("/query")
# def handle_query(payload: QueryRequest):
#     qid = str(uuid.uuid4())
#     query = payload.query

#     # Step 1: Check guardrails on query
#     query_guardrail = check_guardrails(query, payload.model)
#     if query_guardrail["issues"]:
#         table.add_data(
#             qid, query, "[REJECTED]",
#             query_guardrail["summary"], query_guardrail["issues"],
#             None, None, None, None, None,
#             0, 0, 0, 0, 0, 0
#         )
#         wandb.log({
#             "rejected_query": query,
#             "query_guardrail_summary": query_guardrail["summary"],
#             "query_guardrail_issues": query_guardrail["issues"],
#             "interaction_table": table
#         })
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "status": "rejected",
#                 "message": "Invalid input. Cannot process this request.",
#                 "summary": query_guardrail["summary"],
#                 "issues": query_guardrail["issues"]
#             }
#         )
#     # Step 2: Generate response
#     prompt = FINAL_PROMPT_TEMPLATE.format(customer_query=query)
#     response, usage_gen, cost_gen, latency_gen = call_chat(
#         payload.model, [{"role": "user", "content": prompt}],
#         temperature=payload.temperature, max_tokens=payload.max_tokens
#     )

#     # Step 3: Guardrails on response
#     response_guardrail = check_guardrails(response, payload.model)

#     # Step 4: Evaluation
#     eval_prompt = EVAL_PROMPT_TEMPLATE.format(query=query, chatbot_response=response)
#     eval_response, usage_eval, cost_eval, latency_eval = call_chat(
#         payload.eval_model, [{"role": "user", "content": eval_prompt}],
#         temperature=0.0
#     )

#     try:
#         eval_data = json.loads(eval_response)
#     except:
#         eval_data = {}

#     get_score = lambda k: eval_data.get(k, {}).get("score", 0)
#     get_comment = lambda k: eval_data.get(k, {}).get("comment", "")

#     eval_scores = {
#         "helpfulness": get_score("helpfulness"),
#         "correctness": get_score("correctness"),
#         "tone": get_score("tone"),
#         "clarity": get_score("clarity"),
#         "safety": get_score("safety"),
#         "toxicity": get_score("toxicity"),
#         "profanity": get_score("profanity")
#     }

#     eval_comments = {
#         "helpfulness": get_comment("helpfulness"),
#         "correctness": get_comment("correctness"),
#         "tone": get_comment("tone"),
#         "clarity": get_comment("clarity"),
#         "safety": get_comment("safety")
#     }

#     overall_comment = eval_data.get("overall_comment", "")

#     # Step 5: Log to W&B + Table
#     table.add_data(
#         qid, query, response,
#         query_guardrail["summary"], query_guardrail["issues"],
#         response_guardrail["summary"], response_guardrail["issues"],
#         eval_scores, eval_comments, overall_comment,
#         usage_gen.prompt_tokens, usage_gen.completion_tokens, usage_gen.total_tokens,
#         cost_gen + cost_eval, latency_gen, latency_eval
#     )

#     wandb.log({
#         "query": query,
#         "response": response,
#         "query_guardrails": query_guardrail,
#         "response_guardrails": response_guardrail,
#         "eval_scores": eval_scores,
#         "cost_usd": cost_gen + cost_eval,
#         "latency_query": latency_gen,
#         "latency_eval": latency_eval,
#         "tokens_prompt": usage_gen.prompt_tokens,
#         "tokens_completion": usage_gen.completion_tokens,
#         "tokens_total": usage_gen.total_tokens,
#         "interaction_table": table
#     })

#     return {
#         "status": "accepted",
#         "query_id": qid,
#         "response": response,
#         "query_guardrail": query_guardrail,
#         "response_guardrail": response_guardrail,
#         "evaluation": {
#             "scores": eval_scores,
#             "comments": eval_comments,
#             "overall_comment": overall_comment
#         },
#         "usage": {
#             "tokens_prompt": usage_gen.prompt_tokens,
#             "tokens_completion": usage_gen.completion_tokens,
#             "tokens_total": usage_gen.total_tokens,
#             "cost_usd": round(cost_gen + cost_eval, 6),
#             "latency_gen": latency_gen,
#             "latency_eval": latency_eval
#         }
#     }
@app.post("/chat")
def handle_query(payload: QueryInput):
    qid = str(uuid.uuid4())
    query = payload.query

    # Step 1: Guardrail check on input
    query_guardrail = check_guardrails(query, model)
    query_issues_count = len(query_guardrail["issues"])
    query_toxic = int(query_guardrail["toxicity"])
    query_profanity = int(query_guardrail["profanity"])
    query_injection = int(query_guardrail["prompt_injection"])
    query_malicious = int(query_guardrail["malicious_request"])

    if query_guardrail["issues"]:
        table.add_data(
            qid, query, "[REJECTED]",
            query_guardrail["summary"], query_guardrail["issues"],
            None, None, None, None, None,
            0, 0, 0, 0, 0, 0
        )
        wandb.log({
            "rejected": 1,
            "query_issues_count": query_issues_count,
            "query_toxicity": query_toxic,
            "query_profanity": query_profanity,
            "query_prompt_injection": query_injection,
            "query_malicious_request":query_malicious,
            "interaction_table": table
        })
        wandb.summary["last_rejected_query"] = query
        wandb.summary["last_rejected_summary"] = query_guardrail["summary"]
        wandb.summary["last_rejected_issues"] = ", ".join(query_guardrail["issues"])
        return {
                    "status": "rejected",
                    "response": "Invalid input. Cannot process this request.",
                    "summary": query_guardrail["summary"],
                    "issues": query_guardrail["issues"]
                }
                
        

    # Step 2: Generate response
    prompt = FINAL_PROMPT_TEMPLATE.format(customer_query=query)
    response, usage_gen, cost_gen, latency_gen = call_chat(
        model, [{"role": "user", "content": prompt}],
        temperature=temperature, max_tokens=max_tokens
    )

    # Step 3: Guardrails on response
    response_guardrail = check_guardrails(response, model)
    response_issues_count = len(response_guardrail["issues"])
    response_toxic = int(response_guardrail["toxicity"])
    response_profanity = int(response_guardrail["profanity"])
    response_injection = int(response_guardrail["prompt_injection"])

    # Step 4: Evaluation
    eval_prompt = EVAL_PROMPT_TEMPLATE.format(query=query, chatbot_response=response)
    eval_response, usage_eval, cost_eval, latency_eval = call_chat(
        eval_model, [{"role": "user", "content": eval_prompt}],
        temperature=0.0
    )

    try:
        eval_data = json.loads(eval_response)
    except:
        eval_data = {}

    def get_score(k): return eval_data.get(k, {}).get("score", 0)
    def get_comment(k): return eval_data.get(k, {}).get("comment", "")

    eval_scores = {
        "helpfulness": get_score("helpfulness"),
        "correctness": get_score("correctness"),
        "tone": get_score("tone"),
        "clarity": get_score("clarity"),
        "safety": get_score("safety"),
        "toxicity": get_score("toxicity"),
        "profanity": get_score("profanity")
    }

    eval_comments = {
        "helpfulness": get_comment("helpfulness"),
        "correctness": get_comment("correctness"),
        "tone": get_comment("tone"),
        "clarity": get_comment("clarity"),
        "safety": get_comment("safety")
    }

    overall_comment = eval_data.get("overall_comment", "")
    total_cost = cost_gen + cost_eval

    # Step 5: Log to Table
    table.add_data(
        qid, query, response,
        query_guardrail["summary"], query_guardrail["issues"],
        response_guardrail["summary"], response_guardrail["issues"],
        eval_scores, eval_comments, overall_comment,
        usage_gen.prompt_tokens, usage_gen.completion_tokens, usage_gen.total_tokens,
        total_cost, latency_gen, latency_eval
    )

    # Step 6: Log Chartable Metrics
    wandb.log({
        "rejected": 0,
        "query_toxicity": query_toxic,
        "query_profanity": query_profanity,
        "query_prompt_injection": query_injection,
        "query_malicious_request": query_malicious,
        "query_issues_count": query_issues_count,
        "response_toxicity": response_toxic,
        "response_profanity": response_profanity,
        "response_prompt_injection": response_injection,
        "response_issues_count": response_issues_count,
        "eval_helpfulness": eval_scores["helpfulness"],
        "eval_correctness": eval_scores["correctness"],
        "eval_tone": eval_scores["tone"],
        "eval_clarity": eval_scores["clarity"],
        "eval_safety": eval_scores["safety"],
        "eval_toxicity": eval_scores["toxicity"],
        "eval_profanity": eval_scores["profanity"],
        "latency_query": latency_gen,
        "latency_eval": latency_eval,
        "tokens_prompt": usage_gen.prompt_tokens,
        "tokens_completion": usage_gen.completion_tokens,
        "tokens_total": usage_gen.total_tokens,
        "cost_usd": total_cost,
        "interaction_table": table
    })

    return {
        "status": "accepted",
        "query_id": qid,
        "response": response,
        "query_guardrail": query_guardrail,
        "response_guardrail": response_guardrail,
        "evaluation": {
            "scores": eval_scores,
            "comments": eval_comments,
            "overall_comment": overall_comment
        },
        "usage": {
            "tokens_prompt": usage_gen.prompt_tokens,
            "tokens_completion": usage_gen.completion_tokens,
            "tokens_total": usage_gen.total_tokens,
            "cost_usd": round(total_cost, 6),
            "latency_gen": latency_gen,
            "latency_eval": latency_eval
        }
    }
