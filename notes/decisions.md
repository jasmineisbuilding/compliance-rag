# Decisions & Trade-offs

Each entry should be good for a 1-minute interview answer. Template:

```
### D-XXX <title> (Day XX)
- **Context**: what problem is being solved
- **Options**: A / B / C
- **Choice**: which one, and why
- **Cost**: what was given up, what the risks are
- **Evidence**: data / experiment results / observations ("TBD" if none yet; backfill later)
- **Interview one-liner**:
```

---

### D-001 First batch of documents: B-20 / E-23 / B-10 (Day 01)
- **Context**: OSFI publishes many guidelines; 4 weeks is limited
- **Options**: A. all at once / B. start with 3 moderate-length, well-structured guidelines / C. start with CAR, the most important one
- **Choice**: B
- **Cost**: narrow coverage; table- and formula-heavy documents like CAR aren't tackled until later
- **Evidence**: TBD (check chunking quality once all 3 are processed)
- **Interview one-liner**: (write in your own words)

### D-002 Use HTML rather than PDF as the source (Day 01)
- **Context**: OSFI publishes each guideline as both a web page and a PDF
- **Options**: A. PDF (universal, but hierarchy must be inferred from fonts/layout) / B. HTML (heading hierarchy and anchors directly available)
- **Choice**: B
- **Cost**: the parser depends on OSFI's site template and breaks if the site is redesigned; doesn't generalize to PDF-only documents
- **Evidence**: B-20 HTML headings carry clause-number anchors, e.g. `id="2.3.3"`
- **Interview one-liner**: (write in your own words)
