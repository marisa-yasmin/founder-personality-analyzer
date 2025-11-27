# Founder personality analyzer

This project implements a lightweight agentic pipeline to analyze founder call transcripts 
and generate structured insights for early-stage investment decisions. 

The system uses an LLM to:
1. Parse and extract key communication patterns
2. Evaluate founders on dimensions observed in historical top-performer profiles
3. Detect "outlier" traits or risk patterns
4. Generate tailored follow-up questions for the next call

This MVP uses fully synthetic transcript data to preserve confidentiality of past work 
conducted in a venture capital context. 

---

## 🔧 Architecture
Transcript (.txt)
↓
Parser → Structured Text Chunks
↓
LLM Scoring Module (JSON output)
↓
Question Generator (next-call prompts)
↓
Result Report (Markdown/JSON)

Scoring categories:
- Clarity and reasoning structure  
- Depth of domain understanding  
- Problem framing ability  
- Grit and momentum signals  
- Communication anomalies (hesitation, overconfidence, evasion)  

---

## 🧠 Example Outputs

Run the notebook in `notebooks/demo.ipynb` to produce:
- Founder insights JSON  
- 1-page summary  
- Auto-generated follow-up questions  

Outputs are based on synthetic example transcripts in `data/`.

---

## 🚀 Running the Demo

To run the LLM pipeline locally:

1. Create a `.env` file in the project root:
   
   OPENAI_API_KEY=your_key_here

2. Install dependencies:

   pip install -r requirements.txt

3. Run the demo notebook or pipeline scripts.


---

## 📦 Notes

This repository contains no actual call transcripts or other proprietary / confidential information. It demonstrates only the *architecture and mechanisms* of an LLM-based founder evaluation tool.

---
