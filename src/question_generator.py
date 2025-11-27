from openai import OpenAI
from .config import client, MODEL_NAME

client = OpenAI()

def generate_questions(analysis: dict) -> list:
    prompt = f"""
    Based on this analysis of a founder:

    {analysis}

    Generate 5 pointed follow-up questions for the next investor call.
    Return them as a Python list.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return eval(response.choices[0].message.content)
