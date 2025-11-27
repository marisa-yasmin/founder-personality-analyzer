from openai import OpenAI
import json
from .config import client, MODEL_NAME

client = OpenAI()

def score_chunk(chunk: str) -> dict:
    prompt = f"""
    Analyze the following founder transcript segment and score it across:
    - clarity
    - domain expertise
    - reasoning quality
    - momentum signals
    - risk flags (e.g. overconfidence, evasion)
    Return strict JSON with an 'overall_score' 1-10.

    Segment:
    {chunk}
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)
