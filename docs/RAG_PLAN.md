# compliance-qa — 28-Day Execution Plan

Companion to `RAG_SPEC.md` (v3). Assumes **2–3 hours per day**; day 7 of each week is a buffer + retro for catching up.

**Fixed routine for the last 15 minutes of every day**: write the devlog → sync any trade-offs to `decisions.md` → commit.

---

## 1. Note-Keeping System (set up on D1, used daily)

```
compliance-qa/
└── notes/
    ├── devlog/            # daily logs: day-01.md, day-02.md ...
    ├── weekly/            # weekly retros: w1.md ... w4.md
    ├── decisions.md       # decisions & trade-offs (core interview material)
    ├── doc-structure.md   # OSFI document structure notes (D2 output)
    └── interview-bank.md  # interview prep (gitignored, private)
```

How they differ:
- **devlog**: a running log of what happened. Write fast; completeness not required.
- **decisions.md**: only the places where a choice was made. Each entry should be good for a 1-minute interview answer.
- **interview-bank.md**: distilled from the other two into ready-to-use talking points and numbers.

### Template 1: Daily devlog (`notes/devlog/day-XX.md`)

```markdown
# Day XX — YYYY-MM-DD — <topic>

## What I did
-

## Problems & how I solved them
- Problem:
  - Tried:
  - Result:

## Decisions / trade-offs (→ sync to D-XXX in decisions.md)
-

## Numbers (chunk counts, scores, latency, cost...)
-

## Learnings / surprises
-

## Tomorrow
-

## Commits
-
```

### Template 2: Decision record (append to `notes/decisions.md`)

```markdown
### D-XXX <title> (Day XX)
- **Context**: what problem is being solved
- **Options**: A / B / C
- **Choice**: which one, and why
- **Cost**: what was given up, what the risks are
- **Evidence**: data / experiment results / observations ("TBD" if none yet; backfill later)
- **Interview one-liner**:
```

### Template 3: Interview bank (`notes/interview-bank.md`)

```markdown
## 30-second / 2-minute project pitch
## Key numbers (baseline → final)
## STAR stories (one each: challenge, failure, trade-off)
## Anticipated follow-up questions & answers
## Resume bullet drafts
```

### Commit Convention

Format: `type(scope): description`

| type | used for |
|---|---|
| `feat` | new functionality |
| `fix` | bug fixes |
| `eval` | test set, eval scripts, experiment results |
| `refactor` | refactoring |
| `docs` | README and other public docs |
| `notes` | devlog / decisions and other personal notes |
| `chore` | environment, dependencies, config |

- **Small commits**: one logical change per commit; at least 1 functional commit + 1 notes commit per day.
- Experiment commits include numbers, e.g. `eval: add hybrid retrieval, Recall@5 0.62 → 0.78`.
- `.env` is never committed; commit `data/raw/` or only the download script depending on size.

---

## 2. Daily Plan

Each day lists: **Task** / ✅ Done when / 📝 Considerations to record (interview material) / 💾 Example commit

### Week 1: Ingestion

**D1 — Set up repo, download documents**
- Task: create repo, venv, directory structure, `.gitignore`, `.env.example`, `notes/` with templates; download B-20, E-23, B-10 from the OSFI website (HTML preferred)
- ✅ 3 documents in `data/raw/`; repo pushed to GitHub
- 📝 Why these 3 documents and not CAR? Why HTML rather than PDF?
- 💾 `chore: init project structure` / `feat(data): add download script for OSFI guidelines`

**D2 — Read B-20 end to end, write structure notes**
- Task: no code. Read all of B-20; record section/clause numbering, footnotes, tables, cross-reference style, where version and effective date appear; skim E-23 and B-10 for differences
- ✅ `notes/doc-structure.md` complete
- 📝 What does this structure imply for chunking? (first "domain knowledge drives engineering decisions" story)
- 💾 `notes: document structure analysis of B-20/E-23/B-10`

**D3 — Structure-aware parsing of B-20**
- Task: `parse_chunk.py` parses B-20 HTML → chunks by clause → outputs chunk JSON (per spec schema)
- ✅ B-20 chunks printed with correct clause numbers and hierarchy
- 📝 What's the right clause granularity? Split very long clauses further? How to handle tables?
- 💾 `feat(ingest): structure-aware chunking for B-20`

**D4 — Extend to E-23 and B-10, complete metadata**
- Task: adapt the parser to the other two documents; add version, effective_date, url anchors
- ✅ `chunks_structured.jsonl` generated for all 3 documents
- 📝 One generic parser or per-document rules? (generality vs. accuracy)
- 💾 `feat(ingest): support E-23 and B-10, add version metadata`

**D5 — Naive chunking + statistics**
- Task: implement fixed 500-token chunking (for the baseline); compute chunk counts and length distributions for both strategies
- ✅ `chunks_naive.jsonl` and `chunks_structured.jsonl` exist; stats recorded in the devlog
- 📝 Why 500 tokens? How much overlap? What does naive chunking do to clauses (save an example — great for interviews)
- 💾 `feat(ingest): add naive fixed-size chunking for baseline`

**D6 — Manual spot check + bug fixes**
- Task: small script to randomly sample 20 chunks; check each one and fix issues found
- ✅ All 20 samples pass, or issues are recorded
- 📝 How do you validate data quality? What edge cases came up?
- 💾 `fix(ingest): handle <specific issue>`

**D7 — Buffer + W1 retro**
- Task: catch up; write `notes/weekly/w1.md` (done, blockers, risks for next week); tidy this week's decisions
- 💾 `notes: week 1 retro`

### Week 2: Naive End-to-End Loop + Baseline

**D8 — Embedding + indexing**
- Task: `index.py`: call embedding API → write to Chroma; cache embeddings keyed by "text hash + model name"
- ✅ One collection per chunking strategy; a second run hits the cache with no API calls
- 📝 Cohere or OpenAI embeddings? Why cache? (cost awareness)
- 💾 `feat(index): embed chunks into Chroma with local cache`

**D9 — Dense retrieval**
- Task: dense mode in `retrieve.py`; experiment settings in `config.py`; CLI takes a question and prints top-5
- ✅ Ask 5 questions manually, check results, record obvious failures
- 📝 What top-k? Can similarity scores serve as confidence?
- 💾 `feat(retrieve): dense retrieval baseline`

**D10 — Cited answer generation**
- Task: `generate.py`: number the retrieved results in the prompt; require per-sentence clause citations; answer "not found in the documents" when unsupported
- ✅ End-to-end CLI Q&A with clause-level citations
- 📝 Prompt design (citation format, refusal instruction); before/after comparison for each prompt iteration
- 💾 `feat(generate): cited answer generation with refusal`

**D11 — Citation verification + configuration**
- Task: programmatically check that cited clauses appear in the retrieved results; make the LLM configurable
- ✅ Detects answers citing clauses that weren't retrieved
- 📝 What happens when verification fails: flag it, retry, or drop the sentence?
- 💾 `feat(generate): citation verification`

**D12 — Hand-write 30 questions**
- Task: write `questions.jsonl` per spec: ~18 factual, 6 multi-hop/version, 6 out-of-scope; gold labels by clause number
- ✅ 30 questions written, each checked against the source
- 📝 Where the questions came from (what colleagues actually asked at work); why gold labels don't use chunk_id
- 💾 `eval: add 30 handwritten questions`

**D13 — Eval script (retrieval + refusal)**
- Task: `run_eval.py` computes Recall@5, refusal rate, false refusal rate; writes to `results.csv`; run the **baseline** (naive chunking + dense retrieval)
- ✅ First baseline row in `results.csv`
- 📝 Recall criterion; baseline definition
- 💾 `eval: baseline Recall@5 = X.XX`

**D14 — LLM-as-judge + W2 retro**
- Task: add faithfulness and citation accuracy judges; manually check 20 samples to calibrate; write `w2.md`
- ✅ Judge–human agreement rate recorded in the devlog
- 📝 How reliable is the judge? Where does it disagree with humans?
- 💾 `eval: add LLM judge for faithfulness and citation accuracy`

### Week 3: Incremental Improvements (re-run eval after each)

**D15 — Switch to structure-aware chunking**
- Task: retrieve over `chunks_structured`; run eval
- ✅ New row in `results.csv`
- 📝 How much did structure-aware chunking help? Which questions improved, which got worse?
- 💾 `eval: structured chunking, Recall@5 X → Y`

**D16 — Hybrid retrieval**
- Task: add BM25; fuse with RRF or weighted scores; run eval
- ✅ New row; look specifically at clause-number queries
- 📝 RRF or weighted fusion? How to set weights? Why do regulatory documents need keyword retrieval?
- 💾 `feat(retrieve): hybrid BM25 + dense with RRF`

**D17 — Rerank**
- Task: add Cohere rerank (e.g. retrieve 20, keep top 5 after rerank); run eval; record latency and cost
- ✅ New row including latency
- 📝 How much accuracy does rerank buy for its latency and cost? Is it worth it?
- 💾 `feat(retrieve): add Cohere rerank`

**D18 — Failure analysis**
- Task: pull every wrong answer and categorize: retrieval miss / generation error / refusal error; analyze 3–5 representative cases in depth
- ✅ Failure breakdown + 3–5 case drafts in the devlog (reused in the README)
- 📝 **The most important day** — interviewers love "where does your system fail?"
- 💾 `notes: failure analysis`

**D19 — Version / effective date**
- Task: show the version and effective date an answer relies on; add version-related eval questions
- ✅ Version info visible in answers; new questions evaluated
- 📝 Why versions matter in real compliance work (your banking story)
- 💾 `feat(generate): surface guideline version and effective date`

**D20 — Expand to ~100 questions**
- Task: LLM drafts, you rewrite in realistic phrasing and verify; re-run all configs; score the handwritten subset separately
- ✅ Final results table: 4 configs × all metrics, handwritten subset and full set reported separately
- 📝 What biases do LLM-generated questions have? (compare handwritten vs. full-set scores)
- 💾 `eval: expand to ~100 questions, rerun all configs`

**D21 — Buffer / cross-references + W3 retro**
- Task: if time permits, implement cross-reference expansion and run eval; otherwise catch up; write `w3.md`
- 💾 `feat(retrieve): cross-reference expansion` (optional) / `notes: week 3 retro`

### Week 4: Demo, Deployment, Interview Prep

**D22 — Streamlit app**
- Task: `app.py`: answer on the left, cited source clauses on the right (with version, date, link); example question buttons (including one unanswerable); disclaimer
- ✅ Full flow works locally
- 💾 `feat(app): Streamlit demo`

**D23 — Production details**
- Task: rate limiting + daily call cap; log latency and cost per query; ship a prebuilt index
- ✅ Latency and cost stats available
- 📝 Gap between a demo and a production system (interview topic: "what else would it take to go live?")
- 💾 `feat(app): rate limiting and cost tracking`

**D24 — Deploy to HF Spaces**
- Task: deploy; API keys in Secrets; test every example question online
- ✅ Public link works
- 📝 Deployment pitfalls
- 💾 `chore: deploy to Hugging Face Spaces`

**D25 — README (part 1)**
- Task: problem background, architecture diagram, key trade-offs (distilled from `decisions.md`)
- 💾 `docs: README architecture and trade-offs`

**D26 — README (part 2) + GIF**
- Task: eval results table, failure cases, latency and cost, limitations; record GIF (including one "not found")
- 💾 `docs: README eval results and demo GIF`

**D27 — Interview prep**
- Task: complete `interview-bank.md`: 30-second and 2-minute pitch, 3 STAR stories, 10 anticipated follow-ups, resume bullets; say it out loud and record yourself
- ✅ Can deliver the 2-minute pitch without notes

**D28 — Buffer + final retro**
- Task: catch up; write `w4.md` and an overall retro; final repo check (no leaked keys, all README links work)

---

## 3. Recurring Interview Follow-Up Checklist

Check against this when writing the devlog; note down any question you can now answer:

1. Why RAG instead of fine-tuning?
2. How did you choose the chunking strategy? Is there data behind it?
3. How do you know the system got better? Is the eval set trustworthy?
4. When does the system fail?
5. How do you prevent hallucinations? How do you ensure citations are accurate?
6. What are the latency and cost? Where's the bottleneck?
7. What happens when a document is updated?
8. What would need to change if the corpus grew 100×?
9. What's missing to deploy this at a real bank? (access control, audit, data security…)
10. Which decision are you proudest of? Which do you regret?
