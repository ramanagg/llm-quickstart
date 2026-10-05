<!-- @format -->

# llm-quickstart

A tiny, readable starting point for calling an LLM from Python. One small script works with **Google Gemini** and **NVIDIA's hosted models**, so you can compare two providers side by side and see what stays the same across LLM APIs.

This is **Level 0** of a longer learning path that ends in an AI email-triage agent. It is deliberately simple: no frameworks, just the provider SDKs.

## What you will learn

-   How to send a prompt to an LLM and read the reply
-   What **temperature** does (predictable vs. varied output)
-   What **tokens** are, and how to see how many each call uses
-   How the same task looks with two different providers
-   How to keep API keys out of your code and out of Git

## Project files

| File                 | Purpose                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `llm_wrapper.py`     | Sends one hard-coded email to a model and prints a summary                                  |
| `demo.py`            | Picks an email from `sample_emails.json` (random, or by id) and sends it through the prompt |
| `sample_emails.json` | 23 synthetic emails with labels (category, sentiment) for practice                          |
| `requirements.txt`   | Python packages to install                                                                  |
| `.env.example`       | Template for your API keys (placeholders only)                                              |
| `.gitignore`         | Keeps `.env` and `venv/` out of Git                                                         |

## Setup

You need Python 3.10 or newer and an API key for Gemini, NVIDIA, or both.

```bash
git clone https://github.com/ramanagg/llm-quickstart.git
cd llm-quickstart

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # then open .env and add your real keys
```

Get keys here:

-   Gemini: Google AI Studio (aistudio.google.com)
-   NVIDIA: build.nvidia.com

## Usage

```bash
# One hard-coded email
python llm_wrapper.py                 # uses gemini (the default)
python llm_wrapper.py nvidia

# Emails from sample_emails.json
python demo.py              # random email, gemini
python demo.py nvidia       # random email, nvidia
python demo.py gemini 22    # a specific email by id
```

Each run prints the provider, the token counts, what the model said, and (for sample emails) the label stored in the file so you can compare.

## How the defaults work

Nothing asks you which provider or model to use. The script decides in this order:

1. **What you typed.** `python llm_wrapper.py nvidia` selects NVIDIA. With no word, it falls back to `gemini`.
2. **What is in `.env`.** `GEMINI_MODEL` and `NVIDIA_MODEL` choose the model.
3. **A default written in the code**, used only if `.env` has no value.

To switch models, edit `.env`. No code change needed.

## Experiments to try

1. Run the same email 3 times. Does the summary change?
2. Set `TEMPERATURE = 0`, then `1.5`, in `llm_wrapper.py` and compare.
3. Change the prompt ("in 5 words", "for a CEO", "what does the sender want and how urgent is it?").
4. Run email 22 (a prompt-injection attempt). Does the model follow the email's instructions or stay on task?
5. Run emails of different categories and compare the model's answer to the label in the file.

## Troubleshooting

| Error                         | Likely cause                                                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `KeyError: 'GEMINI_API_KEY'`  | The key is missing or misspelled in `.env`                                                                                            |
| `404 page not found` (NVIDIA) | Wrong model name or base URL. Use the plain model ID (no `nvidia_nim/` prefix) and the base URL `https://integrate.api.nvidia.com/v1` |
| `model not found`             | Model names change. Check the current list in Google AI Studio or build.nvidia.com and update `.env`                                  |
| `401` / authentication error  | The key is wrong or expired                                                                                                           |

To list the model IDs your NVIDIA key can use:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://integrate.api.nvidia.com/v1",
                api_key=os.environ["NVIDIA_API_KEY"])
for m in client.models.list():
    print(m.id)
```

## Keep your keys safe

-   Real keys go **only** in `.env`, which is listed in `.gitignore`.
-   `.env.example` must contain placeholders only.
-   Run `git status` before every commit and confirm `.env` is not listed.
-   If a key is ever committed, revoke it and create a new one. Deleting the file in a later commit does not remove it from history.

## What's next

**Level 1: structured output.** Make the model return JSON (`category`, `sentiment`, `confidence`, `summary`) so code can use the answer, and validate it with Pydantic. That classifier becomes the first piece of an email-triage agent.

## License

MIT
