def load_transcript(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def chunk_text(text: str, max_len=800):
    # Simple chunking for long transcripts
    words = text.split()
    chunks = []
    current = []
    for word in words:
        current.append(word)
        if len(current) > max_len:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks
