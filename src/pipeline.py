from .parser import load_transcript, chunk_text
from .llm_scoring import score_chunk
from .question_generator import generate_questions

def analyze_transcript(path: str):
    text = load_transcript(path)
    chunks = chunk_text(text)

    scores = [score_chunk(c) for c in chunks]

    # simple average
    aggregated = {}
    for k in scores[0].keys():
        try:
            aggregated[k] = sum(s[k] for s in scores) / len(scores)
        except:
            aggregated[k] = " / ".join(s[k] for s in scores)

    questions = generate_questions(aggregated)

    return aggregated, questions
