# Extract repo contents and generate chunks.jsonl

import os
import json
from pathlib import Path

DOC_EXTENSIONS = [".md", ".txt", ".rst"]
CODE_EXTENSIONS = [".py", ".js", ".ts", ".java", ".go"]
CONFIG_FILES = ["Dockerfile.ui", "Makefile", "requirements.txt", "pyproject.toml", "package.json"]

REPO_DIR =  Path("data/SyncWell")  # Update to actual repo path
SLACK_DIR = Path("data/slack")   # JSON exported messages
CONF_DIR = Path("data/confluence")  # Exported pages or API dump
ZOOM_DIR = Path("data/recordings")  # Transcribed .txt or .vtt files
OUTPUT_FILE = Path("data/chunks.jsonl")
OUTPUT_FILE.parent.mkdir(exist_ok=True)

chunks = []

# ─────────────────────────────────────────────────────────────
# Repo files (code + docs)
for root, dirs, files in os.walk(REPO_DIR):
    for fname in files:
        fpath = Path(root) / fname
        ext = fpath.suffix

        if ext in DOC_EXTENSIONS or fname in CONFIG_FILES:
            try:
                content = fpath.read_text(encoding="utf-8")
                chunks.append({"source": "repo", "file": str(fpath.relative_to(REPO_DIR)), "content": content})
            except Exception as e:
                print(f"[WARN] Could not read {fpath}: {e}")

        elif ext in CODE_EXTENSIONS:
            try:
                lines = fpath.read_text(encoding="utf-8").splitlines()
                comments = [line.strip() for line in lines if line.strip().startswith("#")]
                if comments:
                    chunks.append({
                        "source": "repo",
                        "file": str(fpath.relative_to(REPO_DIR)),
                        "content": "\n".join(comments)
                    })
            except Exception as e:
                print(f"[WARN] Could not read code from {fpath}: {e}")

# ─────────────────────────────────────────────────────────────
# Slack messages
if SLACK_DIR.exists():
    for file in SLACK_DIR.glob("*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            for msg in data:
                if "text" in msg and msg["text"].strip():
                    chunks.append({
                        "source": "slack",
                        "file": str(file.name),
                        "content": msg["text"]
                    })
        except Exception as e:
            print(f"[WARN] Could not parse Slack file {file}: {e}")

# ─────────────────────────────────────────────────────────────
# Confluence exports (text or HTML-stripped)
if CONF_DIR.exists():
    for file in CONF_DIR.glob("*.txt"):
        try:
            content = file.read_text(encoding="utf-8")
            chunks.append({"source": "confluence", "file": str(file.name), "content": content})
        except Exception as e:
            print(f"[WARN] Could not parse Confluence file {file}: {e}")

# ─────────────────────────────────────────────────────────────
# Zoom meeting transcripts (e.g., .txt or .vtt)
if ZOOM_DIR.exists():
    for file in ZOOM_DIR.glob("*.txt"):
        try:
            content = file.read_text(encoding="utf-8")
            chunks.append({"source": "zoom", "file": str(file.name), "content": content})
        except Exception as e:
            print(f"[WARN] Could not read Zoom file {file}: {e}")

# ─────────────────────────────────────────────────────────────
# Save to JSONL for RAG
with open(OUTPUT_FILE, "w") as out:
    for chunk in chunks:
        json.dump(chunk, out)
        out.write("\n")

print(f"Extracted {len(chunks)} chunks from all sources → {OUTPUT_FILE}")

# Then run: python ingest/embed_docs.py
# Your KT assistant will now use Slack, Confluence, Zoom, and repo content!

