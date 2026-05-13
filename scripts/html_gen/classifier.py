from __future__ import annotations

import re
from .utils import clean_md_title


def is_page_marker_line(text: str) -> bool:
    line = text.strip()
    if not line:
        return False

    # Remove emoji comum de paginação em materiais OCR/exportados.
    line_no_emoji = re.sub(r"^[\U0001F300-\U0001FAFF]+\s*", "", line)
    normalized = clean_md_title(line_no_emoji)

    patterns = [
        r"^<!--\s*p[áa]gina\s+\d+\s*-->$",
        r"^\*\*p[áa]gina\s+\d+\*\*$",
        r"^p[áa]gina\s+\d+$",
    ]
    return any(re.match(p, normalized, flags=re.IGNORECASE) for p in patterns)


def is_page_comment_line(text: str) -> bool:
    return bool(
        re.match(
            r"^<!--\s*(?:p[áa]gina|page)\s*[: ]\s*\d+\s*-->$",
            text.strip(),
            flags=re.IGNORECASE,
        )
    )


def is_separator_line(text: str) -> bool:
    line = text.strip()
    return bool(re.match(r"^(\*{3,}|-{3,}|_{3,})$", line))


def is_ocr_comment_line(text: str) -> bool:
    line = text.strip()
    return bool(re.match(r"^<!--\s*/?\s*ocr:image_[^>]*-->$", line, flags=re.IGNORECASE))


def classify_critical_paragraph(text: str) -> tuple[str, str] | None:
    t = clean_md_title(text).lower()
    if len(t) < 90:
        return None

    severe_keywords = (
        "terminantemente proibido",
        "proibido",
        "sigilo judicial",
        "dados sensíveis",
        "dados sensiveis",
        "lgpd",
        "sem autorização institucional",
        "sem autorizacao institucional",
        "domínio público",
        "dominio publico",
        "versões gratuitas",
        "versoes gratuitas",
        "treinamento futuro",
    )
    if any(k in t for k in severe_keywords):
        return ("Alerta Crítico", "fa-shield-halved")
    return None


def is_strategic_paragraph(text: str) -> bool:
    t = clean_md_title(text).lower()
    strategic_keywords = (
        "estratégia",
        "estrategia",
        "mitigação",
        "mitigacao",
        "fluxo",
        "diretriz",
        "validação",
        "validacao",
        "boas práticas",
        "boas praticas",
        "protocolo",
    )
    return any(k in t for k in strategic_keywords) and len(t) >= 70
