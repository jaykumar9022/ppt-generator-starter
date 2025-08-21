import json
import re
from openai import OpenAI

client = OpenAI()


def extract_json(text):
    # Try to find the first JSON array/object in the LLM output
    m = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if not m:
        raise ValueError("No JSON found in LLM response.")
    jtxt = m.group(0)
    return json.loads(jtxt)

def call_llm_for_slide_plan(text, guidance, api_key, model="gpt-4o-mini"):
    """Call an LLM provider using the user-supplied API key.
    This helper uses OpenAI-style HTTP calls if the 'openai' package is available.
    It falls back to a simple heuristic if not available (for local testing).
    The expected return is a Python list of slide definitions:
    [
      {"title":"...", "type":"title_and_bullets", "bullets":[".."], "notes":"..."},
      ...
    ]
    """
    prompt = f"You are an expert slide writer. Given the input text and optional guidance, split it into a reasonable slide deck. Output ONLY valid JSON (an array of slide objects) with keys: title, type (title|title_and_bullets|bullet_only|image), bullets (array), notes (string). Max slides: 12.\n\nGuidance: {guidance}\n\nText:\n{text[:3000]}\n\nRespond with JSON only."

    # Attempt to use openai (if installed). Use user-supplied key.
    try:
        import openai
        openai.api_key = api_key
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs slide plans as JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800
     )
        content = resp.choices[0].message.content 
        plan = extract_json(content)
        if not isinstance(plan, list):
            raise ValueError("LLM did not return a JSON array.")
        return plan
    except Exception as e:
        # Fallback: very naive splitter — create 3-5 slides by splitting text into paragraphs.
        slides = []
        paras = [p.strip() for p in text.split('\n') if p.strip()]
        num = min(6, max(1, len(paras)))
        chunk_size = max(1, len(paras)//num)
        for i in range(0, len(paras), chunk_size):
            chunk = ' '.join(paras[i:i+chunk_size])
            title = chunk.split('.')[:1][0]
            bullets = chunk.split('.')[:4]
            slides.append({
                "title": title[:60],
                "type": "title_and_bullets",
                "bullets": [b.strip() for b in bullets if b.strip()][:4],
                "notes": ""
            })
        return slides
