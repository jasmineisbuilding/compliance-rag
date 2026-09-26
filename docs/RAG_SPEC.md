# compliance-qa — Project Spec (v3, 2026-09-25)

A RAG question-answering system over public Canadian banking regulatory guidance (OSFI guidelines).
Portfolio project: raw material for resume bullets, behavioral stories, and system design discussions.

## Differentiation (why this isn't "yet another PDF Q&A")

1. **Eval-driven comparison, backed by data**: baseline vs. improved versions, with metrics strictly aligned to each improvement (see Eval Design).
2. **An honest system**: when the answer isn't in the documents, say so explicitly. Tested in pairs (should-refuse / should-not-refuse).
3. **Genuine banking domain knowledge** (not generic practices dressed up):
   - Which version of a guideline an answer is based on, and its effective date
   - Cross-references between clauses
   - Eval questions modeled on what compliance staff actually ask

## Document Scope

- **First batch (W1)**: B-20 (Residential Mortgage Underwriting), E-23 (Model Risk Management), B-10 (Third-Party Risk Management) — moderate length, clear clause numbering.
- **Later (optional)**: large documents such as CAR and LAR (hundreds of pages, many tables and formulas), added after the main pipeline works.
- **Source format**: prefer the **HTML** versions on the OSFI website (heading hierarchy is far easier to parse than PDF); fall back to PDF only when HTML is unavailable.

## Tech Stack

- Embedding: Cohere embed (or OpenAI text-embedding-3-small)
- Vector store: Chroma (local)
- Keyword retrieval: BM25 (rank_bm25)
- Rerank: Cohere rerank
- LLM: a current low-cost model, configurable/swappable (enables model comparison experiments)
- Demo: a single Streamlit app, deployed to Hugging Face Spaces (free tier)
  - No separate FastAPI service; add `api.py` later only if an API is needed

## File Structure

```
compliance-qa/
├── README.md
├── data/
│   ├── raw/             # original HTML/PDF downloaded from OSFI
│   └── processed/       # chunks.jsonl (one per chunking strategy)
├── src/
│   ├── download.py      # fetch guideline pages into data/raw/
│   ├── parse_chunk.py   # parse → chunk (structure-aware / naive 500-token)
│   ├── index.py         # embed → write to Chroma; embeddings cached locally to avoid re-paying while tuning chunking
│   ├── retrieve.py      # dense / hybrid (dense + BM25) / + rerank, configurable
│   ├── generate.py      # build prompt → LLM answer with citations; citations must be clause-level;
│   │                    # programmatic check: every cited clause must appear in the retrieved results
│   └── config.py        # experiment config (chunking strategy, retrieval mode, top-k, model)
├── eval/
│   ├── questions.jsonl  # test set (format below)
│   ├── run_eval.py      # run eval + scoring
│   └── results.csv      # config + scores per experiment; the README comparison table is generated from this
├── notes/               # devlog, decisions, document structure notes
├── app.py               # Streamlit demo
├── .env.example         # API key template (real .env is never committed)
└── requirements.txt
```

### Chunk Schema

```json
{
  "chunk_id": "B-20_3.2.1",
  "doc": "B-20",
  "doc_title": "Residential Mortgage Underwriting Practices and Procedures",
  "clause": "3.2.1",
  "section_path": "3 > 3.2 > 3.2.1",
  "section_title": "...",
  "version": "...",
  "effective_date": "YYYY-MM-DD",
  "url": "https://...#anchor",
  "text": "..."
}
```

(HTML sources use anchor URLs to locate the original text; PDF sources add a `page` field.)

## Milestones (4 weeks) — build the ruler before optimizing

- **W1: Ingestion**
  - Read B-20 end to end; record its structural patterns (section/clause numbering, footnotes, tables, cross-reference style)
  - `parse_chunk.py`: structure-aware chunking + metadata (clause number / version / effective date / URL)
  - Also implement naive chunking (fixed 500 tokens) for the baseline
  - Print chunks and manually inspect a random sample of 20
- **W2: Naive end-to-end loop + baseline**
  - `index.py` + dense-only retrieval + `generate.py`, able to answer questions
  - Hand-write 30 high-quality questions (~20% unanswerable from the documents)
  - `run_eval.py` produces the **baseline scores**, written to `results.csv`
- **W3: Incremental improvements, re-run eval after each**
  - Structure-aware chunking → hybrid (+BM25) → +rerank; run and record eval after each step
  - Expand to ~100 questions (LLM drafts → manually rewritten in realistic phrasing)
  - Implement version/effective-date display + cross-reference expansion (see below)
- **W4: Deployment + README**
  - Launch on HF Spaces, record GIF, complete all required README sections
  - Latency/cost statistics

## Banking-Specific Features

- **Version / effective date** (required):
  - Every chunk carries `version` + `effective_date`; answers state explicitly which version and effective date they rely on
  - Add several version-related questions to the eval set
- **Cross-references** (stretch goal, W3 if time permits):
  - If a retrieved clause says "see section X", automatically pull clause X into the context
  - Show the effect on multi-hop questions via a comparison experiment

## Eval Design

### Question Format

```json
{
  "id": "q001",
  "question": "What is OSFI's maximum LTV for non-conforming mortgages?",
  "gold_clauses": ["B-20 §x.x"],
  "gold_answer": "...",
  "type": "factual | multi-hop | version | out-of-scope",
  "source": "handwritten | llm-assisted"
}
```

- **Gold labels use clause numbers, not chunk_id**: different chunking strategies produce different chunks; binding to chunk_id would invalidate all labels whenever chunking changes.
- Recall criterion: whether any retrieved chunk contains the content of the gold clause.
- Question mix: ~60% factual, ~20% multi-hop / version, ~20% out-of-scope.

### Metrics (aligned with improvements, reported separately)

- **Retrieval**: Recall@5 (naive → structure-aware → hybrid → +rerank)
- **Generation**: faithfulness, citation accuracy
  - Method: LLM-as-judge scoring, with a manual check of 20 samples to calibrate the judge
- **Paired refusal testing**:
  - Refusal rate when refusal is correct (prevents fabrication)
  - False refusal rate when an answer exists (prevents over-caution)

### Credibility

- **Honest baseline definition**: naive = fixed 500-token chunks + dense-only retrieval (stated in the README).
- **Honest sample size**: start with 30 questions; final report uses ~100, or states the sample size limitation in the README.
- **Report handwritten questions separately**: LLM-generated questions tend to reuse the source wording and overstate Recall; scores on the 30 handwritten questions are the most convincing.

## Demo Requirements

- Live demo (HF Spaces) + GIF embedded in the README (free Spaces sleep when idle; the GIF is the fallback).
- API key protection: rate limiting + daily call cap; keys stored in HF Spaces Secrets.
- Example question buttons (including one unanswerable question to show honest refusal); the GIF also shows a "not found" case.
- Show the cited source clauses next to the answer (with version, effective date, and link to the original).
- Prominent disclaimer: "For learning/demo purposes only — not legal or compliance advice."
- Record and publish: average query latency (seconds) and average cost per query.

## Required README Sections

1. Problem background (the pain of looking up clauses in banking compliance)
2. Architecture diagram + data flow
3. Key trade-offs (chunking strategy, hybrid weighting, rerank)
4. Eval results (with baseline definition, sample size note, handwritten-subset scores)
5. **Failure case analysis**: 3–5 wrong answers, root cause + how they were fixed
6. Latency and cost
7. Limitations + "what I'd do with more time"
