import json
from .config import client, MODEL_NAME, TEMPERATURE

def generate_questions(analysis: dict) -> list:
    """
    Call the LLM to generate follow-up questions for the next investor call,
    based on the aggregated founder analysis.
    """
    prompt = f"""
    You are an experienced early-stage VC.

    Based on the scoring in this founder analysis:

    {analysis}

    Generate 5 sharp, concise follow-up questions for the next investor call.
    Each question should be a single sentence, focused on gathering implicit information about the dimensions in the founder analysis and de-risking especially the dimensions where the founder achieved a low score.

    Return ONLY a JSON list of strings, like:
    ["Question 1", "Question 2", ...]
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
    )

    raw = response.choices[0].message.content

    # Again, support both string and list-of-parts formats
    if isinstance(raw, list):
        text = "".join(
            getattr(part, "text", "") or ""
            for part in raw
            if getattr(part, "type", "") == "text"
        )
    else:
        text = raw or ""

    text = text.strip()

    try:
        questions = json.loads(text)
        if isinstance(questions, list):
            return [str(q) for q in questions]
        else:
            return [str(questions)]
    except Exception as e:
        print("Warning: could not parse questions JSON, got:\n", text)
        print("Error was:", e)
        # Fallback: return the whole text as one "question"
        return [text or "Could not generate questions – JSON parse error."]