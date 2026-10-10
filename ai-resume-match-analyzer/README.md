# AI Resume Match Analyzer

A career-support web app that compares resume text with a job description and highlights areas to review.

## Features
- Paste resume and job description text
- Local keyword comparison works without an API key
- Optional AI-generated analysis
- Prompt template included
- Download the analysis as Markdown

## Run locally
```bash
pip install -r requirements.txt
```
Copy `.env.example` to `.env`, optionally add an API key, then run:
```bash
streamlit run app.py
```

This is a career-support tool, not a hiring decision system. Do not use it as the sole basis for hiring or rejection. Remove private contact details before testing.
