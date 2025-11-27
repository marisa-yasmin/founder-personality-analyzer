import json
from .config import client, MODEL_NAME, TEMPERATURE

def _extract_json(text: str) -> dict:
    """
    Try to extract a JSON object from the model output.
    Handles cases where the model wraps JSON in prose or ```json fences.
    """
    text = text.strip()
    # If the model wrapped output in ```json ... ```
    if "```" in text:
        # take everything between the first { and last }
        if "{" in text and "}" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            text = text[start:end]

    # Fallback: also trim before first { and after last }
    if "{" in text and "}" in text:
        start = text.find("{")
        end = text.rfind("}") + 1
        text = text[start:end]

    return json.loads(text)


def score_chunk(chunk: str) -> dict:
    """
    Call the LLM to score a transcript chunk.
    Returns a dict with numeric and text fields.
    Falls back to a simple heuristic if JSON parsing fails.
    """
    prompt = f"""
    You are helping a venture investor evaluate founders based on call transcripts.

    Analyze the following founder transcript segment and score it across:
    - clarity (1-10)
    - domain_expertise (1-10)
    - reasoning_quality (1-10)
    - momentum_signals (1-10)
    - risk_flags (short text)
    - overall_score (1-10)

    Be critical in your assessment, and include low scores where appropriate.
    Return ONLY a JSON object. Do not include any explanation or backticks.
    Example format:
    {{
      "clarity": 8.5,
      "domain_expertise": 9.0,
      "reasoning_quality": 8.0,
      "momentum_signals": 7.5,
      "risk_flags": "sometimes hand-wavy on metrics",
      "overall_score": 8.3
    }}

    Transcript segment:
    {chunk}
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
    )

    raw = response.choices[0].message.content

    # Support both "plain string" and "list of content parts" formats
    if isinstance(raw, list):
        # concatenate any text parts
        text = "".join(
            getattr(part, "text", "") or ""
            for part in raw
            if getattr(part, "type", "") == "text"
        )
    else:
        text = raw or ""

    try:
        return _extract_json(text)
    except Exception as e:
        # Debug output so you can see what went wrong if needed
        print("Warning: could not parse JSON from model, got:\n", text)
        print("Error was:", e)

        # Very simple fallback so the pipeline still runs
        # (you can tweak these defaults if you like)
        return {
            "clarity": 6.0,
            "domain_expertise": 6.0,
            "reasoning_quality": 6.0,
            "momentum_signals": 6.0,
            "risk_flags": f"JSON parse error: {e}",
            "overall_score": 6.0,
        }