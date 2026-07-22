"""
pdf_to_llm.py

A self‑contained script that extracts plain‑text content from a PDF file,
splits the text into manageable chunks, and sends each chunk to an Anthropic
LLM via its HTTP API.  The script uses only the Python standard library plus
`httpx` and `anthropic` (the official Anthropic client).  Errors are caught and
reported, and the LLM responses are printed to stdout.

Usage:
    python pdf_to_llm.py <path_to_pdf> <anthropic_api_key>
"""

import sys
import re
import os
from typing import List

import httpx
from anthropic import Anthropic, APIError  # type: ignore


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Very‑lightweight PDF text extractor.

    It scans the raw PDF for text operands that appear as
    `(some text) Tj` or `(some text) TJ` operators.  This works for
    simple PDFs that embed text directly; it will not handle complex
    layouts, fonts, or compressed streams.

    Returns the concatenated text or raises an exception on failure.
    """
    try:
        with open(pdf_path, "rb") as f:
            raw = f.read().decode("latin-1", errors="ignore")
    except Exception as e:
        raise RuntimeError(f"Failed to read PDF file: {e}")

    # Find all occurrences of text within parentheses followed by Tj/TJ
    pattern = re.compile(r"\((.*?)\)\s+[Tt][Jj]")
    matches = pattern.findall(raw)

    # Un‑escape common PDF escape sequences
    def unescape(s: str) -> str:
        s = s.replace(r"\)", ")")
        s = s.replace(r"\(", "(")
        s = s.replace(r"\\", "\\")
        return s

    text = " ".join(unescape(m) for m in matches)
    if not text:
        raise RuntimeError("No extractable text found in PDF.")
    return text


def chunk_text(text: str, max_chars: int = 2000) -> List[str]:
    """
    Split `text` into chunks no longer than `max_chars` characters,
    attempting to break on whitespace to avoid cutting words.
    """
    chunks = []
    while text:
        if len(text) <= max_chars:
            chunks.append(text.strip())
            break
        # Find last whitespace within the limit
        split_at = text.rfind(" ", 0, max_chars)
        if split_at == -1:
            split_at = max_chars
        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()
    return chunks


def send_to_anthropic(chunk: str, api_key: str) -> str:
    """
    Sends a single `chunk` to Anthropic's Claude model and returns the
    generated completion.  Uses the official `anthropic` client which
    internally relies on `httpx`.
    """
    client = Anthropic(api_key=api_key)
    try:
        response = client.completions.create(
            model="claude-2.1",
            max_tokens=1024,
            prompt=chunk,
        )
        return response.completion
    except APIError as e:
        raise RuntimeError(f"Anthropic API error: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while calling Anthropic: {e}")


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_llm.py <pdf_path> <anthropic_api_key>")
        sys.exit(1)

    pdf_path, api_key = sys.argv[1], sys.argv[2]

    if not os.path.isfile(pdf_path):
        print(f"Error: File not found – {pdf_path}")
        sys.exit(1)

    try:
        text = extract_text_from_pdf(pdf_path)
    except Exception as e:
        print(f"Error extracting text: {e}")
        sys.exit(1)

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks, 1):
        try:
            completion = send_to_anthropic(chunk, api_key)
            print(f"\n--- Chunk {i}/{len(chunks)} ---")
            print(completion)
        except Exception as e:
            print(f"\n--- Chunk {i}/{len(chunks)} ---")
            print(f"Error sending to LLM: {e}")


if __name__ == "__main__":
    main()