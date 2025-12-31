from openai import OpenAI
import json
from datetime import date
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an expense parsing assistant.
Return ONLY valid JSON.

Rules:
- Do not invent categories
- Use only provided categories
- If date missing, use today
Schema:
{
  "name": string,
  "amount": number,
  "date": string,
  "categories": string[]
}
"""

def parse_text(text: str, allowed_categories: list) -> dict:
    today = date.today().isoformat()

    prompt = f"""
Text: {text}
Allowed categories: {allowed_categories}
Default date: {today}
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    raw = resp.choices[0].message.content.strip()
    return json.loads(raw)
