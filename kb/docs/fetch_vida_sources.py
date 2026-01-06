import json
import os
from pathlib import Path
import io
import pdfplumber
import requests
from bs4 import BeautifulSoup


# Base directory = directory where THIS script resides
BASE_DIR = Path(__file__).resolve().parent

RAW_DIR = BASE_DIR / "raw"
CONFIG_PATH = BASE_DIR / "vida_sources.json"

RAW_DIR.mkdir(parents=True, exist_ok=True)

def fetch_url(url: str) -> bytes:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content

def extract_html_text(html_bytes: bytes) -> str:
    soup = BeautifulSoup(html_bytes, "html.parser")

    # Very cheap heuristic: drop nav/footer, focus on main content.
    # You can refine this later.
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # If there's an obvious <main> or article, focus on that.
    main = soup.find("main") or soup.find("article") or soup.body
    text = main.get_text(separator="\n", strip=True)
    return text

def extract_pdf_text(pdf_bytes: bytes) -> str:


    text_parts = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)

def main():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        sources = json.load(f)

    for src in sources:
        doc_id = src["doc_id"]
        raw_path = RAW_DIR / f"{doc_id}.raw.json"
        if raw_path.exists():
            print(f"[skip] {doc_id} already exists")
            continue

        print(f"[fetch] {doc_id} -> {src['url']}")
        content = fetch_url(src["url"])
        Path("debug_raw.html").write_bytes(content)

        if src["format"] == "html":
            text = extract_html_text(content)
        elif src["format"] == "pdf":
            text = extract_pdf_text(content)
        else:
            raise ValueError(f"Unknown format {src['format']} for {doc_id}")

        raw_record = {
            "doc_id": doc_id,
            "title": src["title"],
            "url": src["url"],
            "source_type": src["source_type"],
            "pillar": src["pillar"],
            "language": src["language"],
            "format": src["format"],
            "text": text,
            # You can add a timestamp here if you like:
            # "downloaded_at": datetime.utcnow().isoformat()
        }

        with raw_path.open("w", encoding="utf-8") as f:
            json.dump(raw_record, f, ensure_ascii=False, indent=2)

        print(f"[saved] {raw_path}")

if __name__ == "__main__":
    main()
