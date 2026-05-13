from __future__ import annotations

import base64
import html
import mimetypes
import re
from pathlib import Path


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def safe_href(url: str) -> str:
    clean_url = re.sub(r"\\(.)", r"\1", url).strip()
    if re.match(r"^\s*javascript\s*:", clean_url, flags=re.IGNORECASE):
        return "#"
    return esc(clean_url)


def inline_md(text: str) -> str:
    placeholders: dict[str, str] = {}

    def _store(fragment: str) -> str:
        key = f"\x02{len(placeholders)}\x03"
        placeholders[key] = fragment
        return key

    def _make_link(url: str, label: str) -> str:
        return _store(f'<a href="{safe_href(url)}" target="_blank">{esc(label)}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: _make_link(m.group(2), m.group(1)), text)
    text = re.sub(r'(?<!["\'/])(https?://[^\s<>"{}^\[\]]+?)(?=[\s\[\]()]|$)', lambda m: _make_link(m.group(1), m.group(1)), text)

    text = esc(text)

    for key, fragment in placeholders.items():
        text = text.replace(key, fragment)

    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!])", r"\1", text)
    text = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", lambda m: f"<strong>{m.group(1)}</strong>", text)
    text = re.sub(r"\*([^*]+)\*", lambda m: f"<em>{m.group(1)}</em>", text)
    return text


def clean_md_title(text: str) -> str:
    text = text.strip()
    # remove wrapper de negrito completo
    m = re.match(r"^\*\*(.+)\*\*$", text)
    if m:
        text = m.group(1).strip()
    # converte escapes de markdown: 1\. -> 1.
    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!])", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def strip_leading_number(text: str) -> str:
    t = clean_md_title(text)
    t = re.sub(r"^\d+[\.\-\)]?\s*", "", t)
    return t.strip()


def file_to_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    safe_mime = mime or "application/octet-stream"
    content_b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{safe_mime};base64,{content_b64}"


def normalize_data_uri(raw_logo: str) -> str:
    cleaned = re.sub(r"\s+", "", raw_logo.strip())
    if cleaned.startswith("data:image"):
        return cleaned
    return f"data:image/png;base64,{cleaned}"


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker, start + len(start_marker))
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"Marcadores não encontrados: {start_marker} ... {end_marker}")
    start_insert = start + len(start_marker)
    return text[:start_insert] + "\n" + replacement + text[end:]
