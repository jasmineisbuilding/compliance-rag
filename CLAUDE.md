# compliance-qa

A RAG question-answering system over public Canadian OSFI regulatory guidelines. This is an interview portfolio project; the author has 8 years of banking/compliance experience.

- Design spec: `docs/RAG_SPEC.md` (single source of truth for technical spec and eval design)
- Execution plan: `docs/RAG_PLAN.md` (28-day day-by-day plan)
- Personal notes: `notes/` (devlog, decisions, doc-structure)

## Language
- **Everything committed to the repo must be in English**: code, comments, commit messages, README, docs, and all files under `notes/`.
- Chat with the author in Chinese.
- Exception: `notes/interview-bank.md` is gitignored and may be in any language.

## Working with the author
- The author must be able to explain every line of code in an interview. For core logic (chunking, retrieval, eval), the author writes it first: explain the approach and review their code; do not write full implementations unless explicitly asked. Boilerplate (download scripts, Streamlit UI, glue code) can be written directly.
- When making a non-obvious choice, call out the trade-off so it can be recorded in `notes/decisions.md`.

## Conventions
- Commit format: `type(scope): description`, type ∈ feat / fix / eval / refactor / docs / notes / chore. Eval commits include numbers (e.g. `Recall@5 0.62 → 0.78`).
- Do not add `Co-Authored-By` or any AI attribution lines to commit messages or PR descriptions.
- Daily log: `notes/devlog/day-XX.md`, copied from `notes/devlog/_template.md`.
- Never commit `.env`. `notes/interview-bank.md` is private and gitignored.
- Eval gold labels use clause numbers (e.g. `B-20 §3.2`), never chunk_id.

## Environment
- Python 3.12, virtualenv at `.venv/`: `source .venv/bin/activate`
- API keys live in `.env` (see `.env.example`)
