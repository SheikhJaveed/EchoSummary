import os
import math
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set. Export it before running.")

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "You are an expert note-taker for university lectures. "
    "Summarize the provided transcript into: 1) Title, 2) Key Concepts, 3) "
    "Definitions, 4) Examples, 5) Important Formulas or Code, 6) "
    "Actionable Study Notes. Keep it concise and well-structured."
)

def chunk_text(text: str, chunk_size: int = 12000) -> list[str]:
    # Rough chunking by characters; Gemini 1.5 can handle large inputs, but we stay safe.
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks

def summarize_chunk(chunk: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
{SYSTEM_PROMPT}

Transcript Chunk:
{chunk}

Return a clean, readable markdown summary for just this chunk.
"""
    resp = model.generate_content(prompt)
    return resp.text or ""

def summarize_long_text(full_text: str, title_hint: str = "Lecture Summary") -> str:
    chunks = chunk_text(full_text)
    if len(chunks) == 1:
        body = summarize_chunk(chunks[0])
        return f"# {title_hint}\n\n{body}"

    partials = []
    for i, ch in enumerate(chunks, 1):
        part = summarize_chunk(ch)
        partials.append(f"## Part {i}\n\n{part}")

    # Final merge
    model = genai.GenerativeModel("gemini-1.5-flash")
    merge_prompt = f"""
{SYSTEM_PROMPT}

We have multiple partial summaries of a single lecture. Merge them into one coherent, deduplicated, well-structured study note.

Partial Summaries:
{ "\n\n".join(partials) }

Return one final markdown document with sections:
- Title
- Key Concepts
- Definitions
- Examples
- Important Formulas or Code
- Actionable Study Notes
"""
    final = model.generate_content(merge_prompt).text or ""
    return f"# {title_hint}\n\n{final}"
