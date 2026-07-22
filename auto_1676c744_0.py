"""
sample_pdf_setup.py

This script creates a `sample_pdfs` directory, downloads a few example PDF files
into it, and ensures that the required third‑party libraries (`httpx` and
`anthropic`) are installed. It is self‑contained and uses only the Python
standard library together with `httpx` and `anthropic`.

Usage:
    python sample_pdf_setup.py
"""

import sys
import subprocess
import os
from pathlib import Path

# ----------------------------------------------------------------------
# Helper: ensure a package is installed, installing it via pip if needed.
# ----------------------------------------------------------------------
def ensure_package(package: str) -> None:
    try:
        __import__(package)
    except ImportError:
        print(f"[INFO] Installing missing package: {package}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install {package}: {e}")
            sys.exit(1)

# Ensure required third‑party packages are available.
ensure_package("httpx")
ensure_package("anthropic")

import httpx  # noqa: E402  (import after dynamic install)

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
PDF_DIR = Path("sample_pdfs")
PDF_URLS = [
    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    "https://www.africau.edu/images/default/sample.pdf",
    "https://www.hq.nasa.gov/alsj/a17/A17_FlightPlan.pdf",
]

# ----------------------------------------------------------------------
# Main workflow
# ----------------------------------------------------------------------
def download_pdfs(target_dir: Path, urls: list[str]) -> None:
    """Download each PDF from `urls` into `target_dir`."""
    target_dir.mkdir(parents=True, exist_ok=True)
    client = httpx.Client(timeout=30.0)

    for idx, url in enumerate(urls, start=1):
        try:
            resp = client.get(url)
            resp.raise_for_status()
            filename = target_dir / f"sample_{idx}.pdf"
            with open(filename, "wb") as f:
                f.write(resp.content)
            print(f"[SUCCESS] Downloaded {url} -> {filename}")
        except httpx.HTTPError as exc:
            print(f"[ERROR] Failed to download {url}: {exc}")

    client.close()

def main() -> None:
    try:
        download_pdfs(PDF_DIR, PDF_URLS)
        print("[INFO] PDF setup complete.")
    except Exception as exc:
        print(f"[UNEXPECTED ERROR] {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()