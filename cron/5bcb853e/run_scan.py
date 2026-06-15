#!/usr/bin/env python3
"""AI-Erdős & autoformalization daily scan (cron 5bcb853e).

Sources (gated by AI-method keyword filter except wiki diff):
1. arXiv new lists for math.CO, math.NT, math.LO (last 14 days, AI-method keyword match).
2. Tao wiki "AI contributions to Erdős problems" diff vs prior snapshot
   (GitHub raw markdown URL, all added/changed rows pass regardless of date).
3. arXiv backstop search: autoformalization, Lean theorem proving,
   neural theorem proving, AlphaEvolve (last 7 days).

State: seen_items.json (dedupes arxiv identifiers + wiki row hashes).
Snapshot hygiene: tmp + size>=10k + os.replace atomic rename.

Output: run_findings_YYYY-MM-DD.json with keys
  arxiv_new, arxiv_backstop_new, wiki_new_rows, scan_date, errors.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
STATE = HERE / "seen_items.json"
WIKI_URL = "https://raw.githubusercontent.com/wiki/teorth/erdosproblems/AI-contributions-to-Erd%C5%91s-problems.md"
WIKI_MIN_BYTES = 10_000

AI_TERMS = [
    "Aletheia", "FunSearch", "AlphaEvolve", "Aristotle", "AlphaProof",
    "autoformalization", "Lean", "neural theorem proving", "LLM",
    "AI-assisted", "large language model", "Gemini Deep Think", "Codex",
    "Harmonic", "Rethlas", "UlamAI", "GPT-5", "ChatGPT", "Claude Opus",
    "Claude Sonnet", "proof assistant", "ProofCouncil",
]
ARXIV_CATS = ["math.CO", "math.NT", "math.LO"]
BACKSTOP_TERMS = ["autoformalization", "Lean theorem proving",
                  "neural theorem proving", "AlphaEvolve"]


def http_get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": "ai-erdos-scan/1.0",
        "Accept": "text/markdown, text/html, application/xml;q=0.9, */*;q=0.5",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def load_state() -> dict:
    if not STATE.exists():
        return {"arxiv_ids": [], "wiki_row_hashes": [], "wiki_last_snapshot_date": None}
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {"arxiv_ids": [], "wiki_row_hashes": [], "wiki_last_snapshot_date": None}


def save_state(state: dict) -> None:
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True))
    os.replace(tmp, STATE)


def matches_ai(text: str) -> bool:
    t = text.lower()
    return any(term.lower() in t for term in AI_TERMS)


def parse_arxiv_atom(xml: str) -> list[dict]:
    items = []
    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)
    for e in entries:
        def grab(tag: str) -> str:
            m = re.search(fr"<{tag}[^>]*>(.*?)</{tag}>", e, re.DOTALL)
            return (m.group(1).strip() if m else "")
        ident = grab("id")
        arxiv_id = ""
        m = re.search(r"arxiv\.org/abs/([\w./-]+?)(v\d+)?$", ident)
        if m:
            arxiv_id = m.group(1)
        title = re.sub(r"\s+", " ", grab("title"))
        summary = re.sub(r"\s+", " ", grab("summary"))
        published = grab("published")
        items.append({
            "id": arxiv_id,
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "title": title,
            "abstract": summary,
            "published_date": published[:10] if published else "",
        })
    return items


def fetch_arxiv_recent(category: str, days: int = 14, max_results: int = 200) -> list[dict]:
    q = f"cat:{category}"
    url = ("http://export.arxiv.org/api/query?"
           f"search_query={urllib.parse.quote(q)}&sortBy=submittedDate&sortOrder=descending"
           f"&max_results={max_results}")
    try:
        xml = http_get(url, timeout=45)
    except Exception as e:
        return [{"_error": f"fetch {category}: {e}"}]
    items = parse_arxiv_atom(xml)
    cutoff = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    return [it for it in items if it.get("published_date", "") >= cutoff]


def fetch_arxiv_backstop(term: str, days: int = 7, max_results: int = 50) -> list[dict]:
    q = f'all:"{term}"'
    url = ("http://export.arxiv.org/api/query?"
           f"search_query={urllib.parse.quote(q)}&sortBy=submittedDate&sortOrder=descending"
           f"&max_results={max_results}")
    try:
        xml = http_get(url, timeout=45)
    except Exception as e:
        return [{"_error": f"backstop {term}: {e}"}]
    items = parse_arxiv_atom(xml)
    cutoff = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    return [it for it in items if it.get("published_date", "") >= cutoff]


def fetch_wiki_snapshot() -> str:
    txt = http_get(WIKI_URL, timeout=45)
    if len(txt) < WIKI_MIN_BYTES:
        raise RuntimeError(f"wiki snapshot too small ({len(txt)} bytes); refusing to overwrite")
    return txt


def extract_wiki_rows(md: str) -> list[str]:
    rows = []
    for line in md.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        if re.match(r"^\|[\s\-:|]+\|$", s):
            continue
        rows.append(s)
    return rows


def hash_row(row: str) -> str:
    return hashlib.sha256(row.encode("utf-8")).hexdigest()[:16]


def write_atomic(path: Path, content: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content)
    if path.exists() and tmp.stat().st_size < WIKI_MIN_BYTES:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"refusing to write tiny snapshot {tmp.stat().st_size} bytes")
    os.replace(tmp, path)


def main() -> int:
    scan_date = os.environ.get("SCAN_DATE") or dt.date.today().isoformat()
    state = load_state()
    seen_arxiv = set(state.get("arxiv_ids", []))
    seen_rows = set(state.get("wiki_row_hashes", []))
    errors: list[str] = []

    arxiv_new = []
    for cat in ARXIV_CATS:
        for it in fetch_arxiv_recent(cat):
            if "_error" in it:
                errors.append(it["_error"])
                continue
            if not it.get("id") or it["id"] in seen_arxiv:
                continue
            text = f"{it.get('title','')} {it.get('abstract','')}"
            if not matches_ai(text):
                continue
            it["category"] = cat
            arxiv_new.append(it)
            seen_arxiv.add(it["id"])
        time.sleep(3)

    wiki_new_rows = []
    try:
        snapshot = fetch_wiki_snapshot()
        snap_path = HERE / f"tao_wiki_fetch_{scan_date}.md"
        write_atomic(snap_path, snapshot)
        rows = extract_wiki_rows(snapshot)
        first_run = state.get("wiki_last_snapshot_date") is None
        for row in rows:
            h = hash_row(row)
            if h in seen_rows:
                continue
            if first_run:
                seen_rows.add(h)
                continue
            wiki_new_rows.append({"row": row, "hash": h})
            seen_rows.add(h)
        state["wiki_last_snapshot_date"] = scan_date
    except Exception as e:
        errors.append(f"wiki: {e}")

    arxiv_backstop_new = []
    for term in BACKSTOP_TERMS:
        for it in fetch_arxiv_backstop(term):
            if "_error" in it:
                errors.append(it["_error"])
                continue
            if not it.get("id") or it["id"] in seen_arxiv:
                continue
            text = f"{it.get('title','')} {it.get('abstract','')}"
            if not matches_ai(text):
                continue
            it["backstop_term"] = term
            arxiv_backstop_new.append(it)
            seen_arxiv.add(it["id"])
        time.sleep(3)

    findings = {
        "scan_date": scan_date,
        "arxiv_new": arxiv_new,
        "arxiv_backstop_new": arxiv_backstop_new,
        "wiki_new_rows": wiki_new_rows,
        "errors": errors,
    }
    out = HERE / f"run_findings_{scan_date}.json"
    out.write_text(json.dumps(findings, indent=2, sort_keys=True))

    state["arxiv_ids"] = sorted(seen_arxiv)
    state["wiki_row_hashes"] = sorted(seen_rows)
    save_state(state)

    print(f"scan_date={scan_date}")
    print(f"arxiv_new={len(arxiv_new)}")
    print(f"arxiv_backstop_new={len(arxiv_backstop_new)}")
    print(f"wiki_new_rows={len(wiki_new_rows)}")
    print(f"errors={len(errors)}")
    print(f"findings_file={out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
