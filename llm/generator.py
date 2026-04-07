import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Clients
gemini = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

ollama = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)


SYSTEM_PROMPT = """
You are a trading strategy generator.

STRICT RULES:
- Generate ONLY ONE class
- The class MUST have method: on_step(self, env)
- DO NOT define BaseStrategy
- DO NOT include explanations

The strategy MUST:
- Execute trades (buy/sell)
- Avoid staying idle
- Use simple conditions that trigger frequently
- Not be overly restrictive

Use ONLY:
- env.get_price()
- env.buy(qty)
- env.sell(qty)
- env.get_cash()
- env.get_position()

Return ONLY Python code.
"""


def generate_strategy(user_prompt, model="gemini"):
    if model == "gemini":
        client = gemini
        model_name = "gemini-2.5-flash"

    elif model == "llama":
        client = ollama
        model_name = "llama3.2"

    else:
        raise ValueError("Unsupported model")

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    code = response.choices[0].message.content

    # clean markdown
    code = code.replace("```python", "").replace("```", "")

    return code