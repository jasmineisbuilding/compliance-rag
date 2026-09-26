# Day 01 — 2026-09-25 — Repo setup, document download

## What I did
- `git init`; created directory structure (docs / data / src / eval / notes)
- Added `.gitignore`, `.env.example`, `requirements.txt`, `CLAUDE.md`, placeholder README
- `notes/` templates: devlog template, decisions.md, doc-structure.md, interview-bank.md (gitignored)
- venv (Python 3.12) with all dependencies installed
- `src/download.py`: downloads B-20, E-23, B-10 HTML from the OSFI website into `data/raw/` and writes `manifest.json` (URL + fetch date)

## Problems & how I solved them
- Problem: the top search result for B-20 ("Final Revised Guideline B-20") has only an "Annex" heading
  - Tried: inspected the page's heading structure — it's the release notice, not the guideline text
  - Result: switched to `residential-mortgage-underwriting-practices-procedures-guideline-2017`, which has the full text

## Decisions / trade-offs (→ decisions.md)
- D-001 First batch is B-20 / E-23 / B-10, not CAR
- D-002 HTML instead of PDF

## Numbers
- Raw HTML (including site navigation): B-20 128K chars / E-23 112K / B-10 153K

## Learnings / surprises
- B-20 headings carry clause-number anchors (e.g. `<h3 id="2.3.3">Debt service coverage`) → easy structure-aware chunking and deep links
- E-23 and B-10 use letter+number numbering (A.1 / A1.); the three documents are formatted inconsistently → consider on D3/D4
- **The E-23 page is the 2027 version, effective 2027-05-01; the version currently in force is from 2017** → exactly the real-world case the spec's version/effective-date feature is for; look closer on D2

## Tomorrow
- D2: read B-20 end to end, fill in `notes/doc-structure.md`

## Commits
-
