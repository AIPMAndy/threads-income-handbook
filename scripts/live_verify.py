#!/usr/bin/env python3
"""After deploy, check published Pages bytes against the exact checked-out commit.

Offline PR builds must use build.py --check and check.py. This gate runs only
after GitHub's deploy-pages action finishes and requires real HTTPS resources.
"""
from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aipmandy.github.io/threads-income-handbook/"
FILES = (
    "index.html",
    "lab.html",
    "assets/app.js",
    "assets/style.css",
    "robots.txt",
    "sitemap.xml",
    "guide/pricing.html",
    "pdf/threads-income-handbook-guide.pdf",
)
ATTEMPTS = 12
WAIT_SECONDS = 10


def check_once():
    errors = []
    for path in FILES:
        expected = (ROOT / path).read_bytes()
        want = hashlib.sha256(expected).hexdigest()
        # Query does not change the resource: helps bypass CDN copies of an
        # earlier deployment while preserving direct path-based verification.
        url = BASE + path + "?edition=" + want[:16]
        req = Request(url, headers={
            "User-Agent": "AIPMAndy-pages-live-verifier/1.0",
            "Cache-Control": "no-cache",
            "Accept-Encoding": "identity",
        })
        try:
            with urlopen(req, timeout=25) as response:
                status = response.status
                content_type = response.headers.get("Content-Type", "")
                actual = response.read()
            got = hashlib.sha256(actual).hexdigest()
            if status != 200 or want != got:
                errors.append(f"{path}: HTTP {status}, expected {want}, live {got}")
            elif path.endswith(".pdf") and not actual.startswith(b"%PDF-"):
                errors.append(f"{path}: file is not a PDF")
            else:
                print(f"PASS {path} HTTP 200 SHA-256 {got} bytes={len(actual)} Content-Type={content_type}")
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            errors.append(f"{path}: HTTPS request failed: {exc}")
    return errors


def main():
    for attempt in range(1, ATTEMPTS + 1):
        print(f"Verify deployed Pages against source checkout, pass {attempt}/{ATTEMPTS}", flush=True)
        try:
            errors = check_once()
        except FileNotFoundError as exc:
            print(f"FAIL source artifact missing: {exc}", file=sys.stderr)
            return 1
        if not errors:
            print(f"PASS: {len(FILES)}/{len(FILES)} real HTTPS resources match exact local SHA-256; not a device or PDF visual signoff")
            return 0
        print("Not yet identical:\n" + "\n".join(" - " + x for x in errors), flush=True)
        if attempt < ATTEMPTS:
            time.sleep(WAIT_SECONDS)
    print("FAIL: deployment is not byte-identical after all retries", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
