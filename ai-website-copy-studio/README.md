# AI Website Copy Studio

A simple web app that drafts landing-page, product-page, service-page, and about-page copy from a brand brief.

## Features
- Select audience, page type, tone, and language
- Generate hero copy, benefits, features, FAQs, and CTA
- Prompt template included in `prompts/website_copy.md`
- Demo mode works without an API key
- Optional OpenAI-compatible chat-completions integration

## Run locally
```bash
pip install -r requirements.txt
```
Copy `.env.example` to `.env`, optionally add your API key, then run:
```bash
streamlit run app.py
```

Without an API key, sample demo copy is generated. Review all claims before publishing.
