# MailTriage Agent

An open source agentic workflow that reads a support inbox, classifies each email by **intent and sentiment**, routes it to the right internal person, and answers knowledge-transfer (KT) requests directly from your documentation using RAG.

> Demo GIF goes here: angry client mail gets escalated, KT request gets a grounded reply.

## What it does

| Category | Action |
|---|---|
| Hotfix | Forward to CTO and project lead |
| Bug report | Forward to QA |
| Feature request | Forward to project manager |
| Appraisal | Forward to project manager (or HR) |
| Client angry | Forward to project manager and CTO |
| Refund | Forward to project manager |
| KT request | **Never forwarded.** Retrieve docs, reply to the sender |

Every forward includes an AI-written summary so the recipient knows why it landed with them.

## Architecture

```
Inbox (Gmail / Outlook / IMAP)
        |
   Mail adapter  -->  clean text (strip signatures, quoted replies)
        |
   Classifier agent (LLM)  -->  {category, sentiment, confidence, summary}
        |
   Router (plain code, routing table + guards)
     |-- low confidence  -->  Needs-Review label (human)
     |-- KT request      -->  KT agent (RAG over docs) --> draft reply
     |-- everything else -->  forward to recipients from routing table
        |
   Label as processed + audit log
```

## Design decisions

1. **Routing is code, not an LLM call.** The model picks a category. A routing table decides who gets the mail. Emails are untrusted input and a prompt can be talked around; code cannot.
2. **Sender allowlist is checked in code** before any KT reply, so internal docs never go to unknown senders.
3. **Drafts first.** KT replies are created as drafts for human approval until you enable auto-send.
4. **Confidence threshold.** Uncertain classifications go to a human folder instead of being guessed.
5. **Prompt injection is assumed.** Email text is passed to the model as data, never as instructions, and the model has no tool that can forward to arbitrary addresses.
6. **Provider adapters.** Gmail, Outlook (Microsoft Graph) and IMAP implement one small interface, so the rest of the system is provider-independent.

## Project structure

```
mailtriage/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── pyproject.toml
├── config/
│   ├── routing.yaml          # category -> recipients
│   ├── allowlist.yaml        # client domains allowed KT replies
│   └── settings.yaml         # confidence threshold, dry-run, draft mode
├── src/mailtriage/
│   ├── adapters/
│   │   ├── base.py           # fetch_new(), forward(), reply(), label()
│   │   ├── gmail.py
│   │   ├── outlook.py
│   │   ├── imap.py
│   │   └── folder.py         # demo mode: reads sample .eml/.json files
│   ├── agents/
│   │   ├── classifier.py     # ADK LlmAgent, structured JSON output
│   │   └── kt_responder.py   # ADK LlmAgent + retrieval tool
│   ├── router.py             # routing table + guards
│   ├── rag/
│   │   ├── ingest.py         # chunk and embed KT docs
│   │   └── search.py
│   ├── cleaning.py           # signature / quote stripping
│   ├── audit.py              # log every action
│   └── pipeline.py           # ADK SequentialAgent wiring
├── data/
│   ├── sample_emails.json    # synthetic labeled emails
│   └── kt_docs/              # sample module documentation
├── eval/
│   ├── run_eval.py           # accuracy per category, confusion matrix
│   └── results/
├── tests/
└── docs/
    └── architecture.png
```

## Quick start (demo mode, no inbox needed)

```bash
pip install -e .
python -m mailtriage --adapter folder --dry-run
```

Dry-run prints what would happen, for example `Would forward to: qa@example.com`.

## Evaluation

Run `python eval/run_eval.py` against `data/sample_emails.json`. Report accuracy per category and a confusion matrix here after each model or prompt change.

| Category | Precision | Recall | Count |
|---|---|---|---|
| (fill in after first run) | | | |

## Safety and privacy

- Use synthetic data only in this repo. Never commit real emails.
- Each user supplies their own OAuth credentials; the project never holds anyone's mail access.
- Read-only scopes where possible; send scope only when auto-send is enabled.
- Full audit log of every classification and action.

## Roadmap

- [ ] Classifier with eval set
- [ ] Router with dry-run
- [ ] KT branch with RAG
- [ ] Gmail adapter
- [ ] Outlook adapter
- [ ] IMAP adapter
- [ ] Simple web UI for reviewing low-confidence mails
- [ ] Multi-language email support

## Contributing

See CONTRIBUTING.md. Good first issues are tagged `good first issue`.

## License

Apache 2.0
