# 📘 LLMOps System for Customer Support Chatbot

---

## 🧠 1. Prompt Engineering  

**Goal:** Design prompts to elicit accurate, safe, and helpful responses from the LLM.

- Prompt variants are defined in [`promts.py`](promts.py) under the `PROMPT_VARIANTS` dictionary.
- Variants include bad to better to best examples, zero-shot, one-shot, and few-shot prompting styles.
- Examples:
  - **Bad:** `"Answer this: {customer_query}"`
  - **Better:** `"You are a support agent. {customer_query}"`
  - **Best:** `"You are an award-winning support agent. Give clear, helpful, warm answers: {customer_query}"`
- Chain-of-thought and safety-aware prompts are also included.
- The notebook [`PromptEngineering.ipynb`](PromptEngineering.ipynb)  experiments applying these variants to customer queries.
- Metrics and qualitative reasoning are logged via W&B.
- Screenshots and outputs of model responses are captured in W&B runs.

---
### Prompt Engineering Experiment Runs
![`Prompt Engineering Variants`](./Images/promptEngineeringRuns1.png)

![`Prompt Engineering Runs`](./Images/promptEngineeringRuns2.png)

---

## 📊 2. Experiment Tracking  

**Goal:** Track prompt versions, outputs, performance metrics, and evaluations using Weights & Biases (W&B).
- W&B is initialized in ['PromptEvaluation.ipynb'](PromptEvaluation.ipynb) and [`chatbot_api_backend.py`](chatbot_api_backend.py) for experiment and application tracing and monitoring
- Setup example:
  ```python
  wandb.init(project="chatbot-prompt-eval", name=variant_name, config={"prompt": prompt_template}, reinit=True)
  ```
- Logged artifacts include prompts, chatbot responses, evaluation scores, latency, and cost.
- Interaction data is stored in W&B Tables.
- Links to W&B dashboards and run logs are available in the `wandb/` directory.
- Comparison charts of prompt variants are generated from logged metrics.

---
## 3. Finetuning

In this project, we skip the traditional finetuning process and instead leverage the OpenAI API directly, utilizing the 'gpt-4.1-mini' model to achieve efficient and effective performance.

---

## 🛡 4. Guardrails  

**Goal:** Prevent model from generating or accepting toxic, profane, manipulative, or unsafe inputs.

- Guard categories include:
  - Toxicity (hate, threats, slurs)
  - Profanity (explicit language)
  - Prompt Injection (e.g., "Ignore previous instructions")
  - Malicious or unsafe requests (hacking, fraud, illegal activities)
- Guardrail detection prompt is defined in [`ChatbotPrompts.py`](ChatbotPrompts.py) as `GUARDRAIL_DETECTOR_PROMPT`.
- Guardrail logic is implemented in [`chatbot_api_backend.py`](chatbot_api_backend.py) and [`GuardRails.ipynb`](GuardRails.ipynb).
- The `check_guardrails` function sends input or output text to the LLM for safety evaluation.
- Violations cause rejection of queries or responses, with detailed logging to W&B.
- Example blocked inputs and logs are captured in W&B run logs and debug outputs.

---
### GuardRails Eval Experiments
![`Image 1`](./Images/guardrailsEvalRuns1.png)
![`Image 2`](./Images/guardrailsEvalRuns2.png)

---

## 📈 5. Evaluation  

**Goal:** Evaluate model performance on quality, safety, and helpfulness.

- Evaluation prompt template `EVAL_PROMPT_TEMPLATE` is defined in [`ChatbotPrompts.py`](ChatbotPrompts.py).
- Metrics evaluated include:
  - Helpfulness
  - Correctness
  - Tone
  - Clarity
  - Safety
  - Toxicity
  - Profanity
- The ['PromptEvaluation.ipynb'](PromptEvaluation.ipynb) module implements `evaluate_response` to call the LLM for scoring.
- The API backend evaluates each chatbot response and logs results.
- Evaluation results for different prompt variants are saved and visualized via W&B.
- Tables and charts of evaluation scores are available in W&B dashboards.

---


## 📉 6. Model Monitoring  

**Goal:** Continuously monitor the deployed chatbot for issues, performance drops, or inappropriate usage.

- Metrics logged per interaction include guardrail violations, evaluation scores, latency, token usage, and cost.
- W&B dashboards provide real-time monitoring and historical trends.
- Logs include detailed interaction tables and error tracking.
- Alerts can be configured based on guardrail violations or performance degradation (not implemented but supported by logs).
- Monitoring setup is integrated into the FastAPI backend.

---
### Monitoring
![`Image 1`](./Images/apiMonitoringRuns.png)
![`Image 2`](./Images/apiMonitoringRuns2.png)
---
## 🚀 7. Deployment  

**Goal:** Deploy chatbot to production (website, API, or messaging app).

- Backend API implemented with FastAPI in [`chatbot_api_backend.py`](chatbot_api_backend.py).
- Frontend implemented using Chainlit in [`chainlit_FE.py`](chainlit_FE.py).
- Frontend sends user queries to backend API and displays chatbot responses.
- Environment variables managed via `.env` and [`config.py`](config.py).
- Containerization supported with `Dockerfile` and `docker-compose.yml`.
- Hosting can be done on platforms supporting Docker containers.
- Example API endpoint: `/chat` accepts queries, enforces guardrails, generates and evaluates responses, and returns results.

---
![`ChatbotRun`](./Images/custormerSupportApp.png)
![`ChatbotRuns`](./Images/chatbotrun1.png)
![`Jail Break Bug Detection`](./Images/Bug_1_Jailbreaking_edge_Case_failure.png)
![`Application Improvement  ---- Jail Break Bug Fix'](./Images/added_malicious_request_guardrail.png)
![`Tests'](./Images/jailBreakingAttempt.png)

---
