import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="AI Website Copy Studio", page_icon="✍️", layout="wide")

def demo_copy(brand, business, audience, page_type, tone, features, cta, language):
    return f"""# {brand or 'Your Brand'}

## Hero section
### {business or 'A better way to get things done'}
A practical solution designed for {audience.lower() if audience else 'your audience'}.

**Primary CTA:** {cta or 'Get started'}

## Why choose us
- **Simple to start:** A clear experience with helpful guidance.
- **Designed around you:** Built with your audience's needs in mind.
- **Focused on outcomes:** Practical features without unnecessary complexity.

## Key features
{features or '• Easy onboarding\n• Helpful support\n• Flexible options'}

## Frequently asked questions
**Who is this for?**  
It is designed for {audience.lower() if audience else 'people looking for a practical solution'}.

**How do I get started?**  
Choose the next step above and contact the team if you need help.

## Page settings
- Page type: {page_type}
- Tone: {tone}
- Language: {language}

> Demo output only. Add an API key for live AI-generated copy.
"""

def live_copy(prompt):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL") or None)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are an expert conversion copywriter and UX writer. Follow the user's brief and do not invent facts."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

st.title("✍️ AI Website Copy Studio")
st.caption("Draft copy for a landing page, product page, or service website.")
with st.sidebar:
    st.header("Brand brief")
    brand = st.text_input("Brand name", "BrightPath")
    business = st.text_input("What do you offer?", "Personalized online tutoring")
    audience = st.text_input("Target audience", "Parents of school-age children")
    page_type = st.selectbox("Page type", ["Landing page", "Product page", "Service page", "About page"])
    tone = st.selectbox("Writing tone", ["Clear and professional", "Friendly and warm", "Bold and energetic", "Premium and minimal"])
    language = st.selectbox("Output language", ["English", "Telugu", "Hindi", "Swedish", "German"])
    features = st.text_area("Features or proof points", "Personalized learning plans\nProgress updates for parents\nFlexible online sessions")
    cta = st.text_input("Preferred call to action", "Book a free trial")
    use_live = st.toggle("Use live AI (requires API key)", value=bool(os.getenv("OPENAI_API_KEY")))

prompt = f"""Create website copy from this brief.
Brand: {brand}
Offer: {business}
Audience: {audience}
Page type: {page_type}
Tone: {tone}
Language: {language}
Features:
{features}
Preferred CTA: {cta}

Follow prompts/website_copy.md. Return polished Markdown with a hero, benefits, features, FAQs, and CTA.
Do not invent statistics, testimonials, certifications, guarantees, or facts not provided.
"""
left, right = st.columns(2)
with left:
    st.subheader("Brief preview")
    st.write({"brand": brand, "offer": business, "audience": audience, "page_type": page_type, "tone": tone, "language": language})
with right:
    st.subheader("Prompt preview")
    st.code(prompt, language="text")

if st.button("Generate website copy", type="primary", use_container_width=True):
    try:
        with st.spinner("Drafting copy..."):
            if use_live:
                if not os.getenv("OPENAI_API_KEY"):
                    st.error("Add OPENAI_API_KEY to .env first.")
                    st.stop()
                result, mode = live_copy(prompt), "Live AI"
            else:
                result, mode = demo_copy(brand, business, audience, page_type, tone, features, cta, language), "Demo mode"
            st.session_state["result"], st.session_state["mode"] = result, mode
    except Exception as exc:
        st.error(f"Generation failed: {exc}")
if "result" in st.session_state:
    st.divider()
    st.caption(f"Output mode: {st.session_state.get('mode', 'Unknown')}")
    st.markdown(st.session_state["result"])
    st.download_button("Download copy as Markdown", st.session_state["result"], "website-copy.md", "text/markdown")
