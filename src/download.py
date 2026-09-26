"""Download OSFI guideline HTML pages into data/raw/.

Usage: python -m src.download
"""
import json
import time
from datetime import date
from pathlib import Path

import requests

BASE = "https://www.osfi-bsif.gc.ca/en/guidance/guidance-library/"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
HEADERS = {"User-Agent": "Mozilla/5.0 (compliance-rag research project)"}

SOURCES = [
    {
        "doc": "B-20",
        "title": "Residential Mortgage Underwriting Practices and Procedures",
        "slug": "residential-mortgage-underwriting-practices-procedures-guideline-2017",
    },
    {
        "doc": "E-23",
        "title": "Model Risk Management (2027)",
        "slug": "guideline-e-23-model-risk-management-2027",
    },
    {
        "doc": "B-10",
        "title": "Third-Party Risk Management",
        "slug": "third-party-risk-management-guideline",
    },
]


def download_all() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for src in SOURCES:
        url = BASE + src["slug"]
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        path = RAW_DIR / f"{src['doc']}.html"
        path.write_text(resp.text, encoding="utf-8")
        manifest.append({**src, "url": url, "file": path.name, "fetched": date.today().isoformat()})
        print(f"{src['doc']}: {len(resp.text):,} chars -> {path.name}")
        time.sleep(1)  # be polite to the server

    (RAW_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    download_all()
