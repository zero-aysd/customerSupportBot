PROMPT_VARIANTS = {
   
    "bare-minimum": "Answer this: {customer_query}",
    "no-context": "Reply to a customer: {customer_query}",
    "basic-support": "You are a support agent. {customer_query}",
    "no-tone": "You're a chatbot. Help the customer with their question: {customer_query}",
    "robotic": "Provide a formal and structured answer to this: {customer_query}",

    "ok-tone": "Answer politely and clearly: {customer_query}",
    "good-clarity": "You are a helpful support agent. Assist this user: {customer_query}",
    "with-role": "You are a customer service rep. Here's a query: {customer_query}",
    "contextualized": "You are a support agent for an e-commerce platform. Help the customer: {customer_query}",
    "tone-aware": "Respond empathetically and clearly to this user question: {customer_query}",

    
    "context-tone": "You’re a friendly and knowledgeable support agent. Help with this query: {customer_query}",
    "product-aware": "You support an online subscription service. Respond empathetically and informatively: {customer_query}",
    "task-aware": "You're an expert in billing, subscriptions, and tech help. Help the customer: {customer_query}",
    "persona-aware": "You support frustrated customers. Respond helpfully: {customer_query}",
    "rich-context": "You're a support agent for a SaaS product. Be empathetic and precise: {customer_query}",
    "top-tier": "You are an award-winning support agent. Give clear, helpful, warm answers: {customer_query}",
    "holistic": "Respond with a helpful solution, emotional tone, and safe advice to: {customer_query}",

    
    "cot-clarification": (
        "You are a support agent. First, think about what the customer's question is asking. "
        "Then break the problem down and respond in a step-by-step manner.\n\n"
        "Customer Query: {customer_query}"
    ),
    "cot-safety-check": (
        "Think carefully before answering. First, consider if the query involves any sensitive or risky topics. "
        "Then, answer in a polite and safe way.\n\nCustomer Query: {customer_query}"
    ),

    "fewshot-basic": (
        "You are a customer support agent. Here are examples of good responses:\n\n"
        "Example 1:\nCustomer: I can't log in to my account.\nSupport: I'm sorry you're having trouble logging in. Let's get this fixed. Can you try resetting your password using the 'Forgot Password' link?\n\n"
        "Example 2:\nCustomer: I was charged twice for my subscription.\nSupport: I'm really sorry about that. I've checked your account and see the duplicate charge. I've issued a refund, and you should see it within 3–5 business days.\n\n"
        "Now answer this query:\nCustomer: {customer_query}"
    ),
    "fewshot-tone-aware": (
        "You are a warm, empathetic support agent. Learn from the examples:\n\n"
        "Example 1:\nCustomer: My package is late.\nSupport: I completely understand how frustrating that is. Let me check on the status for you and get it sorted right away.\n\n"
        "Example 2:\nCustomer: I'm getting error 403.\nSupport: That error usually means there's a permission issue. Could you try logging out and back in?\n\n"
        "Now handle this:\nCustomer: {customer_query}"
    ),
    "fewshot-with-cot": (
        "You are a thoughtful support agent. Here’s how to handle queries step-by-step:\n\n"
        "Example:\nCustomer: I want to cancel my subscription.\nSupport: First, check if the user is on a free or paid plan. Then, provide the cancellation link or instructions. Respond with empathy.\n\n"
        "Now apply the same reasoning:\nCustomer: {customer_query}"
    ),

 
    "optimized": (
        "You're a highly trained support rep for a SaaS company. Read the customer's question carefully, think step-by-step if needed, and answer clearly, empathetically, and safely.\n\n"
        "Customer: {customer_query}"
    ),
    "cot": (
        "You're a customer support expert at a subscription-based SaaS company. First, think about the intent of the query. "
        "Make sure your answer is:\n1. Accurate\n2. Helpful\n3. Polite and empathetic\n4. Safe\n\n"
        "Then write your response:\n\nCustomer: {customer_query}"
    )
}
