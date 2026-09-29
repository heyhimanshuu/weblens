# WebLens — AI Web Research Assistant

Status: Day 1 - project scaffold only. No functionality yet.

An open-source AI web research assistant demonstrating production-oriented
RAG, web extraction, retrieval, grounding and evaluation. Built incrementally,
day by day, as a learning project - not presented as a novel idea.

## Setup (Day 1)

```bash
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Structure

See `app/` for backend modules (crawler, extraction, chunking, embeddings,
retrieval, llm, rag, api), `frontend/` for the Streamlit UI (added later),
and `tests/` for pytest tests.
