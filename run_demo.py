from src.pipeline import analyze_transcript

if __name__ == "__main__":
    import sys

    # Default: strong founder transcript
    path = "data/synthetic_transcript_1.txt"

    # If user passes another file
    if len(sys.argv) > 1:
        path = sys.argv[1]

    analysis, questions = analyze_transcript(path)

    print("=== Aggregated founder analysis ===")
    print(analysis)

    print("\n=== Suggested follow-up questions ===")
    for q in questions:
        print("- " + q)