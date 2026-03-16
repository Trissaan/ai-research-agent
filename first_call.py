import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key = os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model = "claude-haiku-4-5-20251001",
    max_tokens = 256, 
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)

print(message.content[0].text)

# --- Structured JSON output ---
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    system="You respond ONLY with raw valid JSON. No markdown, no backticks, no explanation. Just the JSON object.",
    messages=[{
        "role": "user",
        "content": "Give me a person with fields: name, age, skills (list of 3)"
    }]
)
raw_text = response.content[0].text
# Strip markdown code blocks if present
if raw_text.startswith("```"):
    raw_text = raw_text.split("```")[1].strip()
    if raw_text.startswith("json"):
        raw_text = raw_text[4:].strip()
data = json.loads(raw_text)
print(data)