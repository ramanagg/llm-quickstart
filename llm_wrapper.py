"""Level 0: First contact with an LLM.

Run one of:
    python hello_llm.py gemini
    python hello_llm.py nvidia

Goal: send one email to a model, get a summary back, and see what a
"prompt", "temperature" and "tokens" really are.
"""
import os
import sys


from dotenv import load_dotenv

load_dotenv()  # reads your keys from the .env file

# ---- The input: one email --------------------------------------------------
EMAIL = """Subject: Refund request for invoice 4821

Hi team, we were charged twice for March. Please refund the duplicate
payment of 1,200. Invoice 4821 is attached. Thanks, Freshstart Accounts"""

# ---- The prompt: this is the part you will experiment with -----------------
PROMPT = f"Summarize this email in one sentence:\n\n{EMAIL}"

# ---- Temperature: 0 = predictable, higher = more varied --------------------
TEMPERATURE = 0.2


def ask_gemini(prompt):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
        config=types.GenerateContentConfig(temperature=TEMPERATURE),
    )
    usage = response.usage_metadata
    return response.text, usage.prompt_token_count, usage.candidates_token_count


def ask_nvidia(prompt):
    # NVIDIA's API is OpenAI-compatible, so we use the OpenAI client
    # and just point it at NVIDIA's address.
    from openai import OpenAI

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ["NVIDIA_API_KEY"],
    )
    response = client.chat.completions.create(
        model=os.environ.get("NVIDIA_MODEL", "meta/muse-glimmer-30b"),
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
    )
    usage = response.usage
    return response.choices[0].message.content, usage.prompt_tokens, usage.completion_tokens


if __name__ == "__main__":
    provider = sys.argv[1] if len(sys.argv) > 1 else "gemini"
    ask = {"gemini": ask_gemini, "nvidia": ask_nvidia}[provider]

    text, tokens_in, tokens_out = ask(PROMPT)

    print(f"Provider : {provider}")
    print(f"Tokens   : {tokens_in} in, {tokens_out} out")
    print(f"Summary  : {text}")
