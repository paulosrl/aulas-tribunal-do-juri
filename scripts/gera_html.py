#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import html
import mimetypes
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


MENU_START = "<!-- AUTO:MENU:AULA1:START -->"
MENU_END = "<!-- AUTO:MENU:AULA1:END -->"
CONTENT_START = "<!-- AUTO:CONTENT:START -->"
CONTENT_END = "<!-- AUTO:CONTENT:END -->"
TOPICS_START = "<!-- AUTO:MENU:TOPICOS:START -->"
TOPICS_END = "<!-- AUTO:MENU:TOPICOS:END -->"

ICON_RULES = [
    (("introdu", "funda", "base", "conceito"), "fa-book-open"),
    (("contexto", "memória", "memoria", "janela", "token"), "fa-window-maximize"),
    (("engenharia", "pilar", "método", "metodo", "protocolo"), "fa-pencil-ruler"),
    (("alucina", "risco", "erro", "falha", "ponto cego"), "fa-exclamation-triangle"),
    (("segurança", "seguranca", "lgpd", "sigilo", "compliance"), "fa-shield-halved"),
    (("promotor", "júri", "juri", "juríd", "jurid"), "fa-gavel"),
    (("dados", "prova", "laudo", "documento", "autos"), "fa-database"),
    (("análise", "analise", "investiga", "diagnóstico", "diagnostico"), "fa-search"),
    (("checklist", "validação", "validacao", "verificação", "verificacao"), "fa-check-circle"),
    (("estratégia", "estrategia", "plano", "tática", "tatica"), "fa-bullseye"),
    (("fluxo", "processo", "pipeline", "etapa"), "fa-sync"),
    (("conclus", "síntese", "sintese", "resumo"), "fa-star"),
    (("alerta", "atenção", "atencao"), "fa-exclamation-circle"),
]

ICON_POOL = [
    "fa-book-open",
    "fa-window-maximize",
    "fa-pencil-ruler",
    "fa-exclamation-triangle",
    "fa-shield-halved",
    "fa-gavel",
    "fa-database",
    "fa-search",
    "fa-check-circle",
    "fa-bullseye",
    "fa-sync",
    "fa-star",
    "fa-brain",
    "fa-microscope",
    "fa-balance-scale",
    "fa-chart-line",
    "fa-handshake",
    "fa-fingerprint",
    "fa-network-wired",
    "fa-rocket",
]

AGENT_HEADER_PAT = re.compile(
    r"^\*\*(\d+)\\?\.\*\*[\s\t]+\*\*([^*]+)\*\*"
)

TOPIC_NAV_ITEMS: list[tuple[str, str, str]] = [
    ("Abertura", "1.html", "fa-book-open"),
    ("Engenharia de Prompts", "2.html", "fa-window-maximize"),
    ("Agentes no Júri", "3.html", "fa-gavel"),
    ("Elementos Gráficos no Júri", "4.html", "fa-chart-line"),
    ("NotebookLM no Júri", "5.html", "fa-pencil-ruler"),
    ("Favoritos", "favoritos.html", "fa-star"),
    ("NotebookLM", "notebooklm.html", "fa-brain"),
]

NUMBERED_TOPIC_PAGES = {item[1] for item in TOPIC_NAV_ITEMS}


def safe_href(url: str) -> str:
    clean_url = re.sub(r"\\(.)", r"\1", url).strip()
    if re.match(r"^\s*javascript\s*:", clean_url, flags=re.IGNORECASE):
        return "#"
    return esc(clean_url)


def pick_agent_icon(name: str) -> str:
    name_lower = clean_md_title(name).lower()
    if any(k in name_lower for k in ("investiga", "analista")):
        return "fa-search"
    if any(k in name_lower for k in ("denúncia", "denuncia")):
        return "fa-gavel"
    if any(k in name_lower for k in ("diligência", "diligencia")):
        return "fa-tasks"
    if "arquivamento" in name_lower:
        return "fa-database"
    if any(k in name_lower for k in ("prisão", "prisao", "revogação", "revogacao")):
        return "fa-lock"
    if any(k in name_lower for k in ("laudo", "pericial")):
        return "fa-microscope"
    if any(k in name_lower for k in ("depoimento", "incoerência", "incoerencia")):
        return "fa-eye-slash"
    if any(k in name_lower for k in ("tese", "defensiva", "antecipação", "antecipacao")):
        return "fa-shield-halved"
    if any(k in name_lower for k in ("firac", "jurídica", "juridica")):
        return "fa-balance-scale"
    if any(k in name_lower for k in ("audiência", "audiencia", "perguntas")):
        return "fa-calendar-alt"
    if any(k in name_lower for k in ("cross", "interrogatório", "interrogatorio")):
        return "fa-user-tie"
    if any(k in name_lower for k in ("advogado", "diabo")):
        return "fa-user-secret"
    if any(k in name_lower for k in ("alegação", "alegacao", "memorial")):
        return "fa-tasks"
    if "embargo" in name_lower:
        return "fa-exclamation-circle"
    if any(k in name_lower for k in ("razões", "razoes", "recursal")):
        return "fa-level-up-alt"
    if any(k in name_lower for k in ("contrarrazões", "contrarrazoes")):
        return "fa-users-slash"
    if "roteiro" in name_lower:
        return "fa-list-ol"
    if any(k in name_lower for k in ("sustentação", "sustentacao", "oral")):
        return "fa-play-circle"
    if any(k in name_lower for k in ("quesitação", "quesitacao", "quesito")):
        return "fa-check-circle"
    if "dashboard" in name_lower:
        return "fa-chart-line"
    return "fa-bolt"


@dataclass
class Card:
    title: str
    level: int = 2
    blocks: List[str] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera página HTML a partir de Markdown usando template com marcadores AUTO."
    )
    parser.add_argument("input_md", help="Arquivo markdown de entrada")
    parser.add_argument("output_html", help="Arquivo html de saída")
    parser.add_argument(
        "--template",
        default="templates/topico.template.html",
        help="Template HTML com marcadores AUTO",
    )
    parser.add_argument(
        "--menu-icon",
        default="fa-list-ol",
        help="Ícone Font Awesome para itens de menu da Aula 1",
    )
    parser.add_argument(
        "--page-title",
        default="Defina o título da página",
        help='Título da página (tag <title>). Padrão: "Defina o título da página"',
    )
    parser.add_argument(
        "--menu-md",
        default="menu.md",
        help="Arquivo markdown com título e itens do menu lateral",
    )
    parser.add_argument(
        "--section-mode",
        choices=("semantic", "page"),
        default="semantic",
        help="Modo de seções: 'semantic' (padrão, estilo topico1) ou 'page' (1 seção por página marcada).",
    )
    return parser.parse_args()


def esc(text: str) -> str:
    return html.escape(text, quote=True)


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


def strip_source_references(text: str) -> str:
    # Remove APENAS referências automáticas de ferramentas (SharePoint, Copilot Chat)
    # Preserva links úteis como m365.cloud.microsoft (agentes) e claude.ai

    # Regra 1: Remove referências para SharePoint/Copilot Chat (truncadas)
    text = re.sub(
        r"\s*\[[^\]]*mppabr-my.*?epoint\.com[^\]]*\]\(https?://[^\)]*sharepoint\.com[^\)]*\)",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Regra 2: Remove referências para Microsoft Copilot Chat path específico
    text = re.sub(
        r"\s*\[[^\]]*\]\(https?://[^\)]*sharepoint\.com/personal/paulolima_mppa_mp_br/Documents/Arquivos%20de%20Microsoft%20Copilot%20Chat/[^\)]*\)",
        "",
        text,
        flags=re.IGNORECASE,
    )

    return text


def extract_h1_title(markdown: str) -> str:
    for raw in markdown.splitlines():
        line = raw.strip()
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            return clean_md_title(m.group(1))
    return ""


def parse_authors_line(text: str) -> tuple[str, str, str] | None:
    # Ex: "Autores: Rodrigo Aquino e Paulo Lima | MPPA - CIIA | 14 e 15 de maio de 2026"
    m = re.match(r"^\s*\*{0,2}\s*Autores:\s*(.+?)\s*\*{0,2}\s*$", text, flags=re.IGNORECASE)
    if not m:
        return None
    payload = m.group(1).strip()
    payload = re.sub(r"^\*+\s*", "", payload)
    payload = re.sub(r"\s*\*+$", "", payload)
    parts = [p.strip() for p in payload.split("|")]
    if not parts:
        return None
    authors = clean_md_title(parts[0])
    org = clean_md_title(parts[1]) if len(parts) > 1 else ""
    date = clean_md_title(parts[2]) if len(parts) > 2 else ""
    return (authors, org, date)


def parse_agent_block(lines: List[str], start_i: int, agent_num: str, agent_name: str) -> tuple[str, int]:
    i = start_i
    desc_parts = []
    pillars = []
    agent_url = None

    while i < len(lines):
        raw = lines[i].strip()
        if not raw:
            i += 1
            continue

        if AGENT_HEADER_PAT.match(raw) or re.match(r"^##\s+", raw):
            break

        if raw.lower() == "link:":
            i += 1
            while i < len(lines):
                url_line = lines[i].strip()
                if not url_line:
                    i += 1
                    continue
                lm = re.match(r"^\[([^\]]+)\]\(([^)]+)\)$", url_line)
                if lm:
                    agent_url = re.sub(r"\\(.)", r"\1", lm.group(2))
                elif re.match(r"^https?://", url_line):
                    agent_url = re.sub(r"\\(.)", r"\1", url_line)
                i += 1
                break
            break

        if re.match(r"^\\\*\s+", raw):
            item = re.sub(r"^\\\*\s+", "", raw)
            pillars.append(f"<li>{inline_md(item)}</li>")
            i += 1
            continue

        if re.match(r"^(principais\s+)?pilares:?$", raw, re.IGNORECASE):
            i += 1
            continue

        desc_line = re.sub(r"^Descrição:\s*", "", raw, flags=re.IGNORECASE)
        desc_parts.append(desc_line)
        i += 1

    icon = pick_agent_icon(agent_name)
    desc_html_parts = []
    if desc_parts:
        desc_text = " ".join(desc_parts)
        desc_html_parts.append(f'<p class="agent-desc">{inline_md(desc_text)}</p>')
    if pillars:
        desc_html_parts.append(f'<ul class="agent-pillars">{"".join(pillars)}</ul>')

    desc_block = "\n".join(desc_html_parts)
    link_html = (
        f'<div class="agent-card-footer">'
        f'<a href="{safe_href(agent_url)}" class="agent-link-btn" target="_blank">'
        f'<i class="fas fa-external-link-alt"></i> Acessar Agente</a>'
        f'<!-- AGENT_LOGO -->'
        f'</div>'
        if agent_url
        else ""
    )

    html_block = (
        f'<div class="agent-card">\n'
        f'  <div class="agent-card-header">'
        f'<span class="agent-num-badge">{esc(agent_num)}</span>'
        f'<div class="agent-card-title"><i class="fas {icon}"></i> {inline_md(agent_name)}</div>'
        f'</div>\n'
        f'  <div class="agent-card-body">{desc_block}</div>\n'
        f'  {link_html}\n'
        f'</div>'
    )

    return html_block, i


def split_key_value_item(text: str) -> tuple[str, str] | None:
    # Aceita padrões como:
    # ⚖️ **Atividade-Fim:** Conteúdo...
    # **Atividade-Fim:** Conteúdo...
    raw = text.strip()
    m = re.match(
        r"^(?:(?P<icon>\S+)\s+)?\*\*(?P<label>[^*]{2,80}?:)\*\*\s*(?P<body>.+)$",
        raw,
    )
    if not m:
        return None
    icon = (m.group("icon") or "").strip()
    label = m.group("label").strip()
    body = m.group("body").strip()
    if icon:
        label = f"{icon} {label}"
    return label, body


def extract_agent_access_url(text: str) -> str | None:
    raw = text.strip()
    raw = re.sub(r"^\*{0,2}\s*Acesse o agente:\s*\*{0,2}\s*", "", raw, flags=re.IGNORECASE)
    if raw == text.strip():
        return None

    m_md = re.match(r"^\[([^\]]+)\]\((https?://[^)]+)\)\s*$", raw, flags=re.IGNORECASE)
    if m_md:
        return re.sub(r"\\(.)", r"\1", m_md.group(2).strip())

    m_url = re.match(r"^(https?://\S+)\s*$", raw, flags=re.IGNORECASE)
    if m_url:
        return re.sub(r"\\(.)", r"\1", m_url.group(1).strip())

    return None


def render_copilot_agent_cta(url: str) -> str:
    safe_url = safe_href(url)
    return (
        f'<a href="{safe_url}" class="copilot-agent-cta" target="_blank">'
        '<span class="copilot-agent-cta-icon" aria-hidden="true"></span>'
        '<span class="copilot-agent-cta-label">Acessar Agente Copilot</span>'
        '<i class="fas fa-external-link-alt" aria-hidden="true"></i>'
        "</a>"
    )


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


def derive_page_card_title(lines: List[str], start_idx: int) -> str:
    bold_candidate: str | None = None
    h3_candidate: str | None = None
    quote_candidate: str | None = None
    plain_candidate: str | None = None

    for j in range(start_idx, min(start_idx + 30, len(lines))):
        s = lines[j].strip()
        if not s:
            continue
        if is_page_comment_line(s) or is_page_marker_line(s):
            if j > start_idx:
                break
            continue
        if is_ocr_comment_line(s):
            continue
        if is_separator_line(s):
            if j > start_idx:
                break
            continue

        # Para título de página, segue lógica mais próxima do topico1:
        # prioriza apenas headings principais (# e ##), ignorando ###.
        mh = re.match(r"^(#{1,2})\s+(.+)$", s)
        if mh:
            return clean_md_title(mh.group(2))

        mh3 = re.match(r"^#{3}\s+(.+)$", s)
        if mh3 and h3_candidate is None:
            h3_candidate = clean_md_title(mh3.group(1))
            continue

        mb = re.match(r"^\*\*([^*]+)\*\*$", s)
        if mb and len(clean_md_title(mb.group(1))) <= 140:
            if bold_candidate is None:
                bold_candidate = clean_md_title(mb.group(1))
            continue

        if s.startswith(">") and quote_candidate is None:
            q = clean_md_title(re.sub(r"^>\s*", "", s))
            if q:
                quote_candidate = q
            continue

        if not s.startswith(">") and plain_candidate is None:
            plain_candidate = clean_md_title(s)

    return bold_candidate or h3_candidate or plain_candidate or quote_candidate or "Tópico"


def pick_icon(title: str, fallback: str = "fa-list-ol") -> str:
    t = clean_md_title(title).lower()
    for keywords, icon in ICON_RULES:
        if any(k in t for k in keywords):
            return icon
    return fallback


def pick_item_icon(text: str) -> str:
    # Se o item contém uma URL, usa ícone de link externo
    if "http" in text.lower() or "claude.ai" in text.lower():
        return "fa-link"

    t = clean_md_title(text).lower()
    rules = [
        (("promotor", "juiz", "decid"), "fa-gavel"),
        (("performance", "desempenho", "velocidade"), "fa-rocket"),
        (("curadoria", "seleção", "selecao"), "fa-bolt"),
        (("segurança", "seguranca", "lgpd", "sigilo"), "fa-shield-halved"),
        (("risco", "erro", "falha", "alucina"), "fa-exclamation-triangle"),
        (("verificar", "validar", "chec", "auditoria"), "fa-check-circle"),
        (("dados", "prova", "laudo", "autos"), "fa-database"),
        (("estratégia", "estrategia", "plano", "tática", "tatica"), "fa-bullseye"),
        (("contexto", "janela", "memória", "memoria", "token"), "fa-window-maximize"),
        (("processamento", "operacional", "organização", "organizacao"), "fa-cog"),
    ]
    for keywords, icon in rules:
        if any(k in t for k in keywords):
            return icon
    return "fa-check-circle"


def assign_unique_icons(cards: List[Card], fallback: str) -> List[str]:
    used: set[str] = set()
    assigned: List[str] = []
    for card in cards:
        preferred = pick_icon(card.title, fallback)
        if preferred not in used:
            selected = preferred
        else:
            selected = next((icon for icon in ICON_POOL if icon not in used), fallback)
        assigned.append(selected)
        used.add(selected)
    return assigned


def file_to_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    safe_mime = mime or "application/octet-stream"
    content_b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{safe_mime};base64,{content_b64}"


def parse_markdown(markdown: str, md_dir: Path, section_mode: str = "semantic") -> List[Card]:
    markdown = strip_source_references(markdown)
    lines = markdown.splitlines()
    cards: List[Card] = []
    raw_has_page_markers = any(is_page_comment_line(l) or is_page_marker_line(l) for l in lines)
    has_page_markers = (
        section_mode == "page"
        and raw_has_page_markers
    )
    strict_h2_mode = section_mode == "semantic" and raw_has_page_markers
    current: Card | None = None
    pending_page_start = False
    seen_first_page_marker = False
    seen_first_h2 = False
    current_agent_numbered_h3_idx: int | None = None
    current_agent_features_h3_idx: int | None = None
    prompt_counter = 0

    if not has_page_markers:
        # H1 global vira primeiro card de abertura (mantém título + autores no topo).
        h1 = None
        for line in lines:
            m = re.match(r"^#\s+(.+)$", line.strip())
            if m:
                h1 = m.group(1).strip()
                break
        intro = Card(title=h1 or "", level=1)
        cards.append(intro)
        current = intro

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip("\n")
        line = raw.strip()

        if not line:
            i += 1
            continue

        # Descarta comentários HTML do markdown (ex.: <!-- Página 20 -->)
        # e marcadores de paginação exportados do material fonte.
        if is_page_comment_line(line) or is_page_marker_line(line):
            if has_page_markers:
                seen_first_page_marker = True
                pending_page_start = True
            i += 1
            continue

        # Descarta comentários de OCR inseridos por extração automática.
        if is_ocr_comment_line(line):
            i += 1
            continue

        if has_page_markers and not seen_first_page_marker:
            i += 1
            continue

        if strict_h2_mode and not seen_first_h2 and not re.match(r"^##\s+(.+)$", line):
            i += 1
            continue

        # Separadores de markdown (***, ---, ___) são descartados.
        if is_separator_line(line):
            i += 1
            continue

        if has_page_markers and (pending_page_start or current is None):
            title = derive_page_card_title(lines, i)
            consumed_title_line = False

            mh = re.match(r"^(#{1,3})\s+(.+)$", line)
            if mh and clean_md_title(mh.group(2)) == title:
                consumed_title_line = True
            else:
                mb_card = re.match(r"^\*\*([^*]+)\*\*$", line)
                if mb_card and len(clean_md_title(mb_card.group(1))) <= 120 and clean_md_title(mb_card.group(1)) == title:
                    consumed_title_line = True

            current = Card(title=title or "", level=2)
            cards.append(current)
            pending_page_start = False
            if consumed_title_line:
                i += 1
                continue

        # agent ficha: **N\.** **NOME** ou N\. **NOME**
        m_agent = AGENT_HEADER_PAT.match(line)
        if m_agent and current is not None:
            num = m_agent.group(1)
            name = clean_md_title(m_agent.group(2))
            block_html, i = parse_agent_block(lines, i + 1, num, name)
            current.blocks.append(block_html)
            continue

        # headings
        m2 = re.match(r"^##\s+(.+)$", line)
        if m2:
            seen_first_h2 = True
            if has_page_markers:
                h_title = clean_md_title(m2.group(1))
                h_icon = pick_icon(h_title, "fa-star")
                current.blocks.append(f'<h3><i class="fas {h_icon}"></i> {inline_md(h_title)}</h3>')
            else:
                current = Card(title=clean_md_title(m2.group(1)), level=2)
                cards.append(current)
            i += 1
            continue

        # linha inteira em negrito vira novo tópico (padrão comum do curso)
        mb = re.match(r"^\*\*([^*]+)\*\*$", line)
        if mb:
            candidate = clean_md_title(mb.group(1))
            # Só promove negrito puro a título quando é texto curto (evita transformar parágrafos em menu)
            # EXCETO linhas que parecem ser labels ou chamadas de ação (Acesse, Link, Nota, etc)
            is_label = any(k in candidate.lower() for k in ("acesse", "link:", "nota:", "atenção:", "dica:", "estratégia:"))
            if len(candidate) <= 120 and not has_page_markers and not strict_h2_mode and not is_label:
                current = Card(title=candidate, level=2)
                cards.append(current)
                i += 1
                continue

        m3 = re.match(r"^###\s+(.+)$", line)
        if m3:
            h3_title = clean_md_title(m3.group(1))
            h3_icon = pick_icon(h3_title, "fa-star")
            current.blocks.append(f'<h3><i class="fas {h3_icon}"></i> {inline_md(h3_title)}</h3>')
            if re.match(r"^\d+[\.\)]\s+", h3_title):
                current_agent_numbered_h3_idx = len(current.blocks) - 1
                current_agent_features_h3_idx = None
            elif "funcionalidades principais" in h3_title.lower():
                current_agent_features_h3_idx = len(current.blocks) - 1
            i += 1
            continue

        # imagem markdown: ![alt](caminho)
        mimg = re.match(r"^!\[(.*?)\]\((.+?)\)$", line)
        if mimg:
            alt_text = mimg.group(1).strip()
            src_raw = mimg.group(2).strip()
            if re.match(r"^https?://", src_raw, flags=re.IGNORECASE):
                raise ValueError(
                    f"Imagem remota detectada no markdown: {src_raw}\n"
                    "Para saída 100% offline, use apenas arquivos locais."
                )
            image_path = (md_dir / src_raw).resolve()
            if not image_path.exists():
                raise FileNotFoundError(
                    f"Imagem referenciada não encontrada: {image_path}\n"
                    "Use um caminho local válido relativo ao markdown de entrada."
                )
            data_uri = file_to_data_uri(image_path)
            alt_html = inline_md(alt_text) if alt_text else ""
            current.blocks.append(
                '<figure class="media-figure">\n'
                f'<img src="{data_uri}" alt="{esc(alt_text)}" loading="lazy" />\n'
                + (f"<figcaption>{alt_html}</figcaption>\n" if alt_html else "")
                + "</figure>"
            )
            i += 1
            continue

        # H1 já foi capturado como título global, então não deve virar parágrafo
        m1 = re.match(r"^#\s+(.+)$", line)
        if m1:
            if has_page_markers:
                h1_title = clean_md_title(m1.group(1))
                h1_icon = pick_icon(h1_title, "fa-star")
                current.blocks.append(f'<h3><i class="fas {h1_icon}"></i> {inline_md(h1_title)}</h3>')
            i += 1
            continue

        # alert blockquote (obsidian/github-like): > [!WARNING] Titulo
        if line.startswith("> [!"):
            alert_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                alert_lines.append(lines[i].strip()[1:].strip())
                i += 1

            first = alert_lines[0] if alert_lines else ""
            mt = re.match(r"^\[!([A-Z]+)\]\s*(.*)$", first)
            if mt:
                kind = mt.group(1).strip().upper()
                title = mt.group(2).strip() or kind.title()
                body_lines = alert_lines[1:]
                body_text = " ".join(x for x in body_lines if x).strip()
                if body_text:
                    current.blocks.append(
                        '<div class="alert-box">\n'
                        f'<span class="badge">{inline_md(title)}</span>\n'
                        f'<p>{inline_md(body_text)}</p>\n'
                        "</div>"
                    )
                else:
                    current.blocks.append(
                        '<div class="alert-box">\n'
                        f'<span class="badge">{inline_md(title)}</span>\n'
                        "</div>"
                    )
                continue

        # blockquote
        if line.startswith(">"):
            bq = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                bq.append(lines[i].strip()[1:].strip())
                i += 1
            current.blocks.append(f"<blockquote>{inline_md(' '.join(bq))}</blockquote>")
            continue

        # ul
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i].strip())
                kv = split_key_value_item(item)
                if kv:
                    label, body = kv
                    items.append(
                        '<li class="li-kv">'
                        f'<div class="li-kv-label">{inline_md(label)}</div>'
                        f'<div class="li-kv-body">{inline_md(body)}</div>'
                        "</li>"
                    )
                    i += 1
                    continue
                has_leading_icon = bool(
                    re.match(
                        r"^\s*([⚖⚙✅✔️⭐🔒🔍📌📍📎🧠🛡️🧪📚🎯⚠️❗]|[\U0001F300-\U0001FAFF])",
                        item,
                    )
                )
                if has_leading_icon:
                    items.append(f'<li class="li-has-icon"><span class="li-topic-text">{inline_md(item)}</span></li>')
                else:
                    item_icon = pick_item_icon(item)
                    icon_mod = item_icon.replace("fa-", "")
                    items.append(
                        '<li class="li-topic">'
                        f'<span class="li-topic-icon icon-{icon_mod}"><i class="fas {item_icon}"></i></span>'
                        f'<span class="li-topic-text">{inline_md(item)}</span>'
                        "</li>"
                    )
                i += 1
            current.blocks.append("<ul>\n" + "\n".join(items) + "\n</ul>")
            continue

        # ol
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[i].strip())
                item = strip_leading_number(item)
                item_icon = pick_item_icon(item)
                icon_mod = item_icon.replace("fa-", "")
                items.append(
                    '<li class="li-topic">'
                    f'<span class="li-topic-icon icon-{icon_mod}"><i class="fas {item_icon}"></i></span>'
                    f'<span class="li-topic-text">{inline_md(item)}</span>'
                    "</li>"
                )
                i += 1
            current.blocks.append('<ol class="icon-ol">\n' + "\n".join(items) + "\n</ol>")
            continue

        # markdown table (pipe format)
        if line.startswith("|"):
            prompt_lines: List[str] = []
            j = i
            while j < len(lines):
                cand = lines[j].strip()
                if not cand.startswith("|"):
                    break
                prompt_lines.append(cand)
                j += 1

            first_cell = prompt_lines[0].strip().strip("|").strip().upper() if prompt_lines else ""
            first_cell = re.sub(r"^[^\w]+", "", first_cell)
            is_prompt_block = bool(
                re.match(r"^PROMPT\b", first_cell)
            )
            if prompt_lines and is_prompt_block:
                cleaned_lines: List[str] = []
                for pl in prompt_lines:
                    cell = pl.strip().strip("|").strip()
                    if not cell:
                        continue
                    if re.match(r"^[:\-\s|]+$", cell):
                        continue
                    cleaned_lines.append(cell)

                prompt_text = "\n".join(cleaned_lines).strip()
                if prompt_text:
                    prompt_counter += 1
                    prompt_id = f"prompt-{prompt_counter}"
                    current.blocks.append(
                        '<div class="prompt-lab">\n'
                        '  <div class="prompt-lab-title">Prompt</div>\n'
                        f'  <pre id="{prompt_id}" class="prompt-lab-text">{esc(prompt_text)}</pre>\n'
                        '  <div class="prompt-lab-actions">\n'
                        f'    <button type="button" class="prompt-lab-btn" onclick="copyPromptText(\'{prompt_id}\', this)">Copiar prompt</button>\n'
                        '    <a class="prompt-lab-btn prompt-lab-btn-link" href="https://notebooklm.google.com/" target="_blank">Testar no NotebookLM</a>\n'
                        "  </div>\n"
                        "</div>"
                    )
                    i = j
                    continue

            # Tabela de coluna única (| texto | + separador) vira callout textual,
            # evitando exibir barras "|" cruas no HTML.
            if (
                len(prompt_lines) >= 2
                and re.match(r"^\|?[\s:\-|\t]+\|?$", prompt_lines[1])
            ):
                parsed_rows: List[str] = []
                for pl in prompt_lines:
                    cell = pl.strip().strip("|").strip()
                    if not cell or re.match(r"^[:\-\s|]+$", cell):
                        continue
                    parsed_rows.append(cell)

                if parsed_rows and all(len([c for c in r.split("|") if c.strip()]) <= 1 for r in parsed_rows):
                    title_row = parsed_rows[0]
                    body_rows = parsed_rows[1:]
                    is_tip = clean_md_title(title_row).lower().startswith("💡 dica") or clean_md_title(title_row).lower().startswith("dica:")
                    if is_tip:
                        title_html = "Dica"
                        tip_text = title_row
                        tip_text = re.sub(r"^(💡\s*)?dica:\s*", "", tip_text, flags=re.IGNORECASE).strip()
                        body_html = [f"<p>{inline_md(tip_text)}</p>"] if tip_text else []
                        body_html += [f"<p>{inline_md(r)}</p>" for r in body_rows]
                        current.blocks.append(
                            '<div class="alert-box">\n'
                            f'  <div class="alert-box-title"><i class="fas fa-lightbulb"></i> {title_html}</div>\n'
                            f'  {"".join(body_html)}\n'
                            "</div>"
                        )
                    else:
                        content_rows = [f"<p>{inline_md(r)}</p>" for r in parsed_rows]
                        current.blocks.append(
                            '<div class="alert-box">\n'
                            f'  {"".join(content_rows)}\n'
                            "</div>"
                        )
                    i = j
                    continue

        if "|" in line and i + 1 < len(lines):
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            sep_line = lines[i + 1].strip()
            if (
                "|" in sep_line
                and re.match(r"^\|?[\s:\-|\t]+\|?$", sep_line)
                and len(header_cells) >= 2
            ):
                i += 2
                rows: List[List[str]] = []
                while i < len(lines):
                    row_line = lines[i].strip()
                    if not row_line or "|" not in row_line:
                        break
                    row_cells = [c.strip() for c in row_line.strip("|").split("|")]
                    rows.append(row_cells)
                    i += 1

                # normaliza tamanhos de linha
                col_count = len(header_cells)
                norm_rows = []
                for r in rows:
                    if len(r) < col_count:
                        r = r + [""] * (col_count - len(r))
                    elif len(r) > col_count:
                        r = r[:col_count]
                    norm_rows.append(r)

                # Ajuste específico para o Sumário: remove coluna "Páginas de origem".
                lower_headers = [clean_md_title(h).lower() for h in header_cells]
                drop_idx = None
                for idx_h, hh in enumerate(lower_headers):
                    if "páginas de origem" in hh or "paginas de origem" in hh:
                        drop_idx = idx_h
                        break
                if drop_idx is not None:
                    header_cells = [h for j, h in enumerate(header_cells) if j != drop_idx]
                    norm_rows = [
                        [c for j, c in enumerate(r) if j != drop_idx]
                        for r in norm_rows
                    ]

                table_html = []
                table_html.append('<div class="table-wrapper">')
                table_html.append('<table class="caor-table">')
                table_html.append("<thead>")
                table_html.append("<tr>")
                for h in header_cells:
                    header_label = clean_md_title(h)
                    th_class = ' class="col-index"' if header_label == "#" else ""
                    table_html.append(f"<th{th_class}>{inline_md(h)}</th>")
                table_html.append("</tr>")
                table_html.append("</thead>")
                table_html.append("<tbody>")
                for r in norm_rows:
                    table_html.append("<tr>")
                    for col_idx, c in enumerate(r):
                        if col_idx == 0 and header_cells and clean_md_title(header_cells[0]) == "#":
                            num_text = clean_md_title(c)
                            if re.match(r"^\d+$", num_text):
                                table_html.append(
                                    '<td class="col-index"><span class="num-badge">'
                                    f"{esc(num_text)}"
                                    "</span></td>"
                                )
                                continue
                        td_class = ' class="col-index"' if col_idx == 0 and header_cells and clean_md_title(header_cells[0]) == "#" else ""
                        table_html.append(f"<td{td_class}>{inline_md(c)}</td>")
                    table_html.append("</tr>")
                table_html.append("</tbody>")
                table_html.append("</table>")
                table_html.append("</div>")
                current.blocks.append("\n".join(table_html))
                continue

        # paragraph (agrupa linhas corridas)
        para = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt:
                break
            if is_page_comment_line(nxt) or is_page_marker_line(nxt):
                break
            if is_ocr_comment_line(nxt):
                break
            if is_separator_line(nxt):
                break
            if re.match(r"^(#|##|###)\s+", nxt):
                break
            if nxt.startswith(">"):
                break
            if re.match(r"^[-*]\s+", nxt) or re.match(r"^\d+\.\s+", nxt):
                break
            para.append(nxt)
            i += 1
        paragraph_text = " ".join(para)
        agent_access_url = extract_agent_access_url(paragraph_text)
        if agent_access_url:
            if current_agent_features_h3_idx is not None and 0 <= current_agent_features_h3_idx < len(current.blocks):
                cta_block = (
                    '<div class="copilot-agent-cta-wrap">\n'
                    f"  {render_copilot_agent_cta(agent_access_url)}\n"
                    "</div>"
                )
                current.blocks.insert(current_agent_features_h3_idx, cta_block)
                current_agent_features_h3_idx += 1
            elif current_agent_numbered_h3_idx is not None:
                # Fallback para casos sem "Funcionalidades principais" no agente
                current.blocks.append(
                    '<div class="copilot-agent-cta-wrap">\n'
                    f"  {render_copilot_agent_cta(agent_access_url)}\n"
                    "</div>"
                )
            else:
                current.blocks.append(
                    '<div class="copilot-agent-cta-wrap">\n'
                    f"  {render_copilot_agent_cta(agent_access_url)}\n"
                    "</div>"
                )
            continue
        authors_meta = parse_authors_line(paragraph_text)
        if authors_meta:
            authors, org, date = authors_meta
            author_names = [x.strip() for x in re.split(r"\s+e\s+", authors, flags=re.IGNORECASE) if x.strip()]
            author_badges = []
            for name in author_names[:2]:
                author_badges.append(f'<span class="author-badge">🏅 {inline_md(name)}</span>')
            if not author_badges:
                author_badges.append(f'<span class="author-badge">🏅 {inline_md(authors)}</span>')
            safe_org = inline_md(org) if org else "MPPA - CIIA"
            safe_date = inline_md(date) if date else ""
            date_html = f'  <div class="authors-date">{safe_date}</div>\n' if safe_date else ""
            current.blocks.append(
                '<div class="authors-meta">\n'
                f'  <div class="authors-badges">{"".join(author_badges)}</div>\n'
                f'  <div class="authors-org">{safe_org}</div>\n'
                f"{date_html}"
                '  <div class="authors-note">Material produzido com apoio de ferramentas de IA</div>\n'
                "</div>"
            )
            continue
        critical = classify_critical_paragraph(paragraph_text)
        if critical:
            _label, icon = critical
            current.blocks.append(
                '<div class="alert-box alert-critical">\n'
                f'<span class="badge"><i class="fas {icon}"></i></span>\n'
                f'<p>{inline_md(paragraph_text)}</p>\n'
                "</div>"
            )
        elif is_strategic_paragraph(paragraph_text):
            current.blocks.append(
                '<div class="text-discreet">\n'
                f'<p>{inline_md(paragraph_text)}</p>\n'
                "</div>"
            )
        else:
            current.blocks.append(f"<p>{inline_md(paragraph_text)}</p>")

    # Remove intro vazio quando há outros cards
    if len(cards) > 1 and not cards[0].blocks:
        cards = cards[1:]

    return cards


def render_cards(cards: List[Card], card_icons: List[str]) -> str:
    def _is_summary_title(title: str) -> bool:
        t = clean_md_title(title).lower()
        return ("sumário" in t) or ("sumario" in t)

    def _extract_text_lines_from_blocks(blocks: List[str]) -> List[str]:
        lines: List[str] = []
        for block in blocks:
            for raw in block.splitlines():
                txt = re.sub(r"<[^>]+>", "", raw).strip()
                txt = html.unescape(txt)
                txt = re.sub(r"\s+", " ", txt).strip()
                if txt:
                    lines.append(txt)
        return lines

    def _build_main_summary_table(current_idx: int, card: Card) -> str | None:
        # O sumário deve espelhar o submenu esquerdo: mesmos itens e mesmas âncoras.
        entries: List[tuple[int, str]] = []
        for target_idx, target_card in enumerate(cards, start=1):
            if target_idx == 1 and target_card.level == 1:
                continue
            short = strip_leading_number(target_card.title)
            short = re.sub(r"^\d+(?:\.\d+)*[\.\-\)]?\s*", "", short).strip()
            if not short:
                short = f"Seção {target_idx}"
            entries.append((target_idx, short))

        if len(entries) < 1:
            return None

        rows: List[str] = []
        for i, (tgt, label) in enumerate(entries, start=1):
            rows.append(
                "<tr>"
                f'<td class="col-index"><a href="#p{tgt}"><span class="num-badge">{i}</span></a></td>'
                f'<td><a href="#p{tgt}">{inline_md(label)}</a></td>'
                "</tr>"
            )
        return (
            '<div class="table-wrap">\n'
            '<table class="caor-table">\n'
            "<thead><tr><th class=\"col-index\">#</th><th>Nome da Seção</th></tr></thead>\n"
            "<tbody>\n"
            + "\n".join(rows)
            + "\n</tbody>\n</table>\n</div>"
        )

    def _linkify_summary_table(block_html: str, current_section_idx: int) -> str:
        # Em tabelas de "Sumário", liga cada linha numerada ao card correspondente.
        # Ex.: estando no card p2, a linha "1" aponta para #p3.
        if 'class="caor-table"' not in block_html:
            return block_html
        if "<span class=\"num-badge\">" not in block_html:
            return block_html

        def _row_repl(match: re.Match[str]) -> str:
            num_text = match.group(1).strip()
            label_html = match.group(2)
            if not re.match(r"^\d+$", num_text):
                return match.group(0)
            target = f"p{current_section_idx + int(num_text)}"
            return (
                "<tr>"
                f'<td class="col-index"><a href="#{target}"><span class="num-badge">{num_text}</span></a></td>'
                f'<td><a href="#{target}">{label_html}</a></td>'
                "</tr>"
            )

        pattern = (
            r"<tr>\s*"
            r'<td class="col-index"><span class="num-badge">(\d+)</span></td>\s*'
            r"<td>(.*?)</td>\s*"
            r"</tr>"
        )
        return re.sub(pattern, _row_repl, block_html, flags=re.DOTALL)

    out = []
    for idx, card in enumerate(cards, start=1):
        section_id = f"p{idx}"
        htag = "h1" if card.level == 1 else "h2"
        icon = card_icons[idx - 1] if idx - 1 < len(card_icons) else pick_icon(card.title, "fa-book-open")
        title = clean_md_title(card.title)
        if htag == "h2":
            title = strip_leading_number(title)
            title = re.sub(r"^\d+(?:\.\d+)*[\.\-\)]?\s*", "", title).strip()
        if not title:
            title = f"Seção {idx}"
        out.append(f'            <section id="{section_id}" class="caor-card">')
        out.append(f'                <{htag}><i class="fas {icon}"></i> {inline_md(title)}</{htag}>')
        auto_summary = _build_main_summary_table(idx, card) if _is_summary_title(card.title) else None
        is_single_plain_paragraph = (
            len(card.blocks) == 1
            and card.blocks[0].strip().startswith("<p>")
            and card.blocks[0].strip().endswith("</p>")
        )

        if auto_summary:
            for bl in auto_summary.splitlines():
                out.append(f"                {bl}")
        elif is_single_plain_paragraph:
            paragraph_html = card.blocks[0].strip()
            paragraph_text = re.sub(r"<[^>]+>", "", paragraph_html)
            single_icon = pick_item_icon(paragraph_text)
            icon_mod = single_icon.replace("fa-", "")
            out.append('                <div class="single-spot">')
            out.append(
                f'                    <div class="single-spot-head"><span class="li-topic-icon icon-{icon_mod}"><i class="fas {single_icon}"></i></span></div>'
            )
            out.append(f"                    {paragraph_html}")
            out.append("                </div>")
        else:
            for block in card.blocks:
                if _is_summary_title(card.title):
                    block = _linkify_summary_table(block, idx)
                for bl in block.splitlines():
                    out.append(f"                {bl}")
        out.append("            </section>")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_menu_from_labels(cards: List[Card], card_icons: List[str], menu_icon: str) -> str:
    def _submenu_entries() -> list[tuple[int, str, str]]:
        entries: list[tuple[int, str, str]] = []
        for idx, card in enumerate(cards, start=1):
            if idx == 1 and card.level == 1:
                continue
            short = strip_leading_number(card.title)
            short = re.sub(r"^\d+(?:\.\d+)*[\.\-\)]?\s*", "", short).strip()
            if not short:
                short = f"Seção {idx}"
            icon = card_icons[idx - 1] if idx - 1 < len(card_icons) else pick_icon(short, menu_icon)
            entries.append((idx, short, icon))
        return entries

    links = []
    for sub_num, (idx, short, icon) in enumerate(_submenu_entries(), start=1):
        links.append(
            f'            <a href="#p{idx}" class="nav-l"><i class="fas {icon}"></i> <span class="nav-topic-num">{sub_num}.</span> {esc(short)}</a>'
        )
    return "\n".join(links) + "\n"


def render_topics_accordion(out_path: Path, cards: List[Card], card_icons: List[str], menu_icon: str) -> str:
    # Menu lateral com acordeão para o tópico atual e links de navegação para os demais
    # Sub-itens da página atual (seções internas do acordeão)
    sub_html = render_menu_from_labels(cards, card_icons, menu_icon)

    items = []
    num = 0
    for label, filename, icon in TOPIC_NAV_ITEMS:
        is_numbered = filename in NUMBERED_TOPIC_PAGES
        if is_numbered:
            num += 1
        current_name = out_path.name.lower()
        is_current = current_name == filename.lower()

        if is_current:
            # Tópico atual: renderizar como cabeçalho clicável com sub-itens expandidos
            num_span = f'<span class="nav-topic-num">{num}.</span> ' if is_numbered else ''
            header = (
                f'<span class="nav-l nav-topic-header nav-aula current">'
                f'<i class="fas {icon}"></i> {num_span}{esc(label)}'
                f' <i class="fas fa-chevron-down nav-topic-chevron"></i></span>'
            )
            items.append(
                f'            <div class="nav-topic-group nav-topic-open">\n'
                f'                {header}\n'
                f'                <div class="nav-topic-subitems">\n'
                f'{sub_html}'
                f'                </div>\n'
                f'            </div>'
            )
        elif filename in NUMBERED_TOPIC_PAGES:
            # Outros tópicos numerados: links colapsáveis
            num_span = f'<span class="nav-topic-num">{num}.</span> '
            header = (
                f'<a href="{filename}" class="nav-l nav-topic-header">'
                f'<i class="fas {icon}"></i> {num_span}{esc(label)}</a>'
            )
            items.append(
                f'            <div class="nav-topic-group">\n'
                f'                {header}\n'
                f'            </div>'
            )
        else:
            # Itens extras (ex.: Favoritos) sem numeração
            topic_file = out_path.parent / filename
            if topic_file.exists():
                items.append(
                    f'            <a href="{filename}" class="nav-l">'
                    f'<i class="fas {icon}"></i> {esc(label)}</a>'
                )
            else:
                items.append(
                    f'            <span class="nav-l nav-locked">'
                    f'<i class="fas {icon}"></i> {esc(label)} <i class="fas fa-lock"></i></span>'
                )

    return "\n".join(items) + ("\n" if items else "")


def validate_completeness(markdown: str, html_out: str, cards: List[Card]) -> None:
    md_md_links = len(re.findall(r"\[[^\]]+\]\(https?://[^)]+\)", markdown))
    md_bare_urls = len(re.findall(r'(?<!\[)(?<!\]\()https?://[^\s<>"{}^\[\]]+?(?=[\s\[\]()]|$)', markdown))
    total_md_links = md_md_links + md_bare_urls

    html_links = len(re.findall(r'<a\s+href="https?://', html_out))
    empty_cards = [c for c in cards if not c.blocks]

    issues = []
    if html_links < total_md_links:
        issues.append(f"  ⚠️  {total_md_links - html_links} link(s) perdido(s): MD={total_md_links} → HTML={html_links}")
    if empty_cards:
        issues.append(f"  ⚠️  {len(empty_cards)} card(s) sem conteúdo")
    if issues:
        print("ALERTAS DE COMPLETUDE:")
        for msg in issues:
            print(msg)
    else:
        print(f"  ✓ Completude: {len(cards)} seções, {html_links}/{total_md_links} links OK")


def validate_content_preservation(markdown: str, html_out: str) -> None:
    """
    Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.
    Faz verificação por linhas normalizadas (texto) contra o texto final do HTML.
    """
    def _normalize_text(s: str) -> str:
        s = html.unescape(s)
        s = re.sub(r"\\([\\`*_{}\[\]()#+\-.!])", r"\1", s)
        s = s.replace("\\", " ")
        s = re.sub(r"[^\w\sÀ-ÿ]", " ", s, flags=re.UNICODE)
        s = re.sub(r"\s+", " ", s).strip().lower()
        return s

    html_text = re.sub(r"<[^>]+>", " ", html_out)
    html_text_norm = _normalize_text(html_text)
    html_source_norm = _normalize_text(html_out)

    missing: list[str] = []
    checked = 0

    def _line_variants_for_match(raw_line: str, normalized_line: str) -> list[str]:
        variants = [normalized_line]
        stripped = raw_line.strip()

        # Headings podem perder prefixo numérico no render (ex.: 1.1, 5.2).
        if re.match(r"^#+\s+", stripped):
            no_hash = re.sub(r"^#+\s*", "", stripped)
            no_md = re.sub(r"[*_`]", "", no_hash).strip()
            no_num = re.sub(r"^\d+(?:\.\d+)*[\.\-\)]?\s*", "", no_md).strip()
            no_num_norm = _normalize_text(no_num)
            if no_num_norm and no_num_norm not in variants:
                variants.append(no_num_norm)

        # Linhas de listas numeradas podem perder o prefixo no render com ícones/menu.
        no_ord = re.sub(r"^\d+(?:\.\d+)*[\.\-\)]?\s*", "", stripped).strip()
        if no_ord and no_ord != stripped:
            no_ord_norm = _normalize_text(no_ord)
            if no_ord_norm and no_ord_norm not in variants:
                variants.append(no_ord_norm)

        # Linhas com links markdown podem aparecer no HTML sem a URL visível no texto.
        no_urls = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", stripped)
        no_urls = re.sub(r"https?://\S+", " ", no_urls).strip()
        no_urls_norm = _normalize_text(no_urls)
        if no_urls_norm and no_urls_norm not in variants:
            variants.append(no_urls_norm)

        no_ord_no_urls = re.sub(r"^\d+(?:\.\d+)*[\.\-\)]?\s*", "", no_urls).strip()
        no_ord_no_urls_norm = _normalize_text(no_ord_no_urls)
        if no_ord_no_urls_norm and no_ord_no_urls_norm not in variants:
            variants.append(no_ord_no_urls_norm)

        return [v for v in variants if v]

    in_summary_block = False
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            continue
        low_line = clean_md_title(line).lower()
        if re.match(r"^#+\s+", line):
            # Qualquer novo heading encerra bloco de sumário.
            if in_summary_block and "sumário" not in low_line and "sumario" not in low_line:
                in_summary_block = False
        if "sumário" in low_line or "sumario" in low_line:
            in_summary_block = True
            continue
        if in_summary_block:
            # Permite sumário simplificado (apenas tópicos principais) sem acusar perda.
            continue
        if is_separator_line(line) or is_page_comment_line(line) or is_page_marker_line(line) or is_ocr_comment_line(line):
            continue
        if re.match(r"^\|?\s*[:\-| ]+\|?\s*$", line):
            continue
        if re.match(r"^#\s+\*{0,2}\s*m[óo]dulo\s+\d+", line, flags=re.IGNORECASE):
            # Headings macro de módulo podem ser reestruturados em seções/cards.
            continue
        if re.match(r"^\*{0,2}\s*autores:\s*", line, flags=re.IGNORECASE):
            # Linha de metadados de autores é renderizada em bloco próprio.
            continue
        if re.match(r"^\*{0,2}\s*acesse o agente:\s*", line, flags=re.IGNORECASE):
            # Link de agente é renderizado como botão CTA.
            continue

        # Normalização de markdown para comparar texto puro.
        norm = line
        norm = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", norm)              # imagens
        norm = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 \2", norm)      # links markdown
        norm = re.sub(r"[*_`>#]", " ", norm)                            # sintaxe markdown
        norm = re.sub(r"\|", " ", norm)                                 # pipes em prompts/tabelas
        norm = re.sub(r"\\([\\`*_{}\[\]()#+\-.!])", r"\1", norm)
        norm = _normalize_text(norm)

        # Ignora linhas muito curtas/estruturais para reduzir falso positivo.
        if len(norm) < 12:
            continue

        checked += 1
        variants = _line_variants_for_match(line, norm)
        if not any((v in html_text_norm) or (v in html_source_norm) for v in variants):
            missing.append(line)

    if missing:
        preview = "\n".join(f"  - {m[:160]}" for m in missing[:12])
        raise ValueError(
            "Perda de conteúdo detectada na geração HTML. "
            f"{len(missing)} linha(s) relevantes não encontradas no HTML.\n"
            f"Exemplos:\n{preview}"
        )
    print(f"  ✓ Preservação: {checked} linhas verificadas, sem perda de conteúdo")


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker, start + len(start_marker))
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"Marcadores não encontrados: {start_marker} ... {end_marker}")
    start_insert = start + len(start_marker)
    return text[:start_insert] + "\n" + replacement + text[end:]


def normalize_data_uri(raw_logo: str) -> str:
    cleaned = re.sub(r"\s+", "", raw_logo.strip())
    if cleaned.startswith("data:image"):
        return cleaned
    return f"data:image/png;base64,{cleaned}"


def apply_global_page_rules(
    html_out: str,
    out_path: Path,
    md_path: Path,
    page_title: str,
    menu_group_title: str,
) -> str:
    # Regra 0: Título de página vindo de parâmetro de execução.
    safe_title = esc(page_title.strip() or "Defina o título da página")
    html_out = re.sub(r"<title>.*?</title>", f"<title>{safe_title}</title>", html_out, flags=re.IGNORECASE | re.DOTALL)

    safe_group_title = esc(menu_group_title.strip() or page_title.strip() or "Tópico")
    html_out = re.sub(
        r'(<span class="mobile-header-title">).*?(</span>)',
        rf"\1{safe_group_title}\2",
        html_out,
        flags=re.IGNORECASE | re.DOTALL,
    )
    # Remove rótulo legado "Curso" que aparece antes de "Início".
    html_out = re.sub(
        r'\s*<div class="nav-group-title">\s*Curso\s*</div>\s*',
        "\n",
        html_out,
        flags=re.IGNORECASE,
    )

    # Regra 1: Página inicial sempre aponta para index.html na mesma pasta.
    html_out = re.sub(r'href="\.\./index\.html"', 'href="index.html"', html_out, flags=re.IGNORECASE)

    # Regra 2: Logo preferencialmente na pasta de saída; fallback para pasta do markdown.
    logo_candidates = [
        out_path.parent / "logo.png",
        md_path.parent / "logo.png",
        Path("logo.png"),
    ]
    logo_file = next((p for p in logo_candidates if p.exists()), None)
    if logo_file is None:
        raise FileNotFoundError(
            f"Arquivo obrigatório não encontrado: logo.png\n"
            f"Procurei em: {', '.join(str(p) for p in logo_candidates)}"
        )
    logo_bytes = base64.b64encode(logo_file.read_bytes()).decode("ascii")
    logo_data_uri = f"data:image/png;base64,{logo_bytes}"

    html_out = re.sub(
        r'(<img[^>]*class="sidebar-logo"[^>]*src=")[^"]*(")',
        rf"\1{logo_data_uri}\2",
        html_out,
        flags=re.IGNORECASE,
    )

    agent_logo_html = f'<img src="{logo_data_uri}" class="agent-logo" alt="Logo" />'
    html_out = html_out.replace("<!-- AGENT_LOGO -->", agent_logo_html)

    # Ícone do botão Copilot: usa arquivo real para fidelidade visual.
    copilot_candidates = [
        out_path.parent / "copilot.png",
        md_path.parent / "copilot.png",
        Path("copilot.png"),
    ]
    copilot_icon_data_uri = None
    for candidate in copilot_candidates:
        if candidate.exists():
            copilot_icon_data_uri = file_to_data_uri(candidate)
            break

    # Regra 3: Injetar CSS para fichas de agente e aumentar tamanho do conteúdo em 20%
    agent_css = """<style>
.agent-card {
  background: linear-gradient(135deg, rgba(138,31,58,0.05), rgba(138,31,58,0.02));
  border: 1px solid rgba(138,31,58,0.2);
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transition: box-shadow 0.2s ease;
}
.agent-card:hover {
  box-shadow: 0 4px 20px rgba(138,31,58,0.15);
}
.agent-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.agent-num-badge {
  background: var(--accent);
  color: white;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.85rem;
  flex-shrink: 0;
}
.agent-card-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--accent);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.agent-card-title i {
  font-size: 1.1rem;
}
.agent-card-body {
  flex: 1;
}
.agent-desc {
  color: var(--text-main);
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0 0 0.5rem 0;
}
.agent-pillars {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}
.agent-pillars li {
  padding-left: 1rem;
  border-left: 3px solid var(--accent);
  font-size: 0.85rem;
  color: var(--text-main);
  margin: 0;
}
.agent-card-footer {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-top: 0.5rem;
}
.agent-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: var(--accent);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  text-decoration: none;
  transition: opacity 0.2s ease;
}
.agent-link-btn:hover {
  opacity: 0.85;
}
.agent-logo {
  width: 34px;
  height: 34px;
  object-fit: contain;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}
.agent-logo:hover {
  opacity: 1;
}
.caor-card h1,
.caor-card h2,
.caor-card h3 {
  font-size: 1.275em;
}
.caor-card p {
  font-size: 1.071em;
}
.caor-card li {
  font-size: 1.071em;
}
.nav-topic-subitems .nav-l {
  font-size: clamp(0.89rem, 1.035vw, 0.98rem) !important;
}
/* Clickable cards for index page */
.caor-card a {
  color: var(--accent);
  text-decoration: none;
  cursor: pointer;
  transition: opacity 0.2s ease;
}
.caor-card a:hover {
  opacity: 0.8;
}
.caor-card h2 a {
  display: inline;
  border-bottom: none;
}
.copilot-agent-cta-wrap {
  margin: 0.5rem 0 1rem 0;
}
.copilot-agent-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.62rem;
  background: linear-gradient(135deg, #8a1f3a 0%, #a72c55 40%, #c63d73 100%);
  color: #fff !important;
  border: 0;
  border-radius: 12px;
  padding: 0.7rem 1rem;
  font-weight: 700;
  font-size: 0.95rem;
  text-decoration: none !important;
  border-bottom: none !important;
  box-shadow: 0 6px 18px rgba(138, 31, 58, 0.28);
  transition: transform 0.15s ease, box-shadow 0.2s ease, opacity 0.2s ease;
}
.copilot-agent-cta:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 22px rgba(138, 31, 58, 0.34);
  opacity: 1;
}
.copilot-agent-cta .fa-external-link-alt {
  font-size: 0.82rem;
  opacity: 0.95;
}
.copilot-agent-cta-icon {
  width: 1.26rem;
  height: 1.26rem;
  background-image: url("__COPILOT_ICON_DATA_URI__");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 0.25rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  flex-shrink: 0;
}
.prompt-lab {
  margin: 0.9rem 0 1rem 0;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.14);
  background: linear-gradient(180deg, #121621 0%, #0d1119 100%);
  box-shadow: 0 8px 22px rgba(0,0,0,0.28);
  overflow: hidden;
}
.prompt-lab-title {
  color: #d7def0;
  font-weight: 700;
  font-size: 0.86rem;
  letter-spacing: 0.02em;
  padding: 0.55rem 0.8rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.03);
}
.prompt-lab-text {
  margin: 0;
  padding: 0.9rem 1rem;
  color: #f8fbff;
  background: transparent;
  font-size: 0.88rem;
  line-height: 1.55;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
.prompt-lab-actions {
  display: flex;
  gap: 0.55rem;
  padding: 0.75rem 0.9rem 0.9rem;
  border-top: 1px solid rgba(255,255,255,0.08);
}
.prompt-lab-btn {
  border: 1px solid #93c5fd;
  background: #dbeafe;
  color: #0f172a;
  border-radius: 8px;
  padding: 0.45rem 0.72rem;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none !important;
}
.prompt-lab-btn:hover {
  background: #bfdbfe;
  opacity: 1;
}
.prompt-lab-btn-link {
  display: inline-flex;
  align-items: center;
  border-color: #f59e0b;
  background: #fde68a;
  color: #111827;
}
.prompt-lab-btn-link:hover {
  background: #fcd34d;
}
</style>"""
    if copilot_icon_data_uri:
        agent_css = agent_css.replace("__COPILOT_ICON_DATA_URI__", copilot_icon_data_uri)
    else:
        agent_css = agent_css.replace("__COPILOT_ICON_DATA_URI__", "")
    html_out = html_out.replace("</head>", f"{agent_css}\n</head>", 1)
    prompt_js = """<script>
function copyPromptText(promptId, btnEl) {
  const node = document.getElementById(promptId);
  if (!node) return;
  const text = node.innerText || node.textContent || "";
  navigator.clipboard.writeText(text).then(() => {
    const prev = btnEl.textContent;
    btnEl.textContent = "Copiado";
    setTimeout(() => { btnEl.textContent = prev; }, 1200);
  });
}
</script>"""
    html_out = html_out.replace("</body>", f"{prompt_js}\n</body>", 1)

    return html_out


def generate_index_page(md_path: Path, out_path: Path) -> str:
    """Generate landing page with index.template.html"""
    markdown = md_path.read_text(encoding="utf-8")
    tpl_path = md_path.parent.parent / "templates" / "index.template.html"
    template = tpl_path.read_text(encoding="utf-8")

    # Extract title (H1)
    h1_match = re.search(r"^# (.+)$", markdown, re.MULTILINE)
    title = h1_match.group(1) if h1_match else ""

    # Extract metadata
    subtitle = ""
    footer = ""
    subtitle_match = re.search(r"^\*\*subtítulo:\*\*\s+(.+)$", markdown, re.MULTILINE)
    footer_match = re.search(r"^\*\*rodapé:\*\*\s+(.+)$", markdown, re.MULTILINE)

    if subtitle_match:
        subtitle = subtitle_match.group(1)
    if footer_match:
        footer = footer_match.group(1)

    # Extract topics (H2 with links)
    topic_pattern = r"^## \[([^\]]+)\]\(([^)]+)\)\s*\n\n(.+?)(?=\n\n\*\*\*|$)"
    topics = []
    for match in re.finditer(topic_pattern, markdown, re.MULTILINE | re.DOTALL):
        title_text = match.group(1)
        link = match.group(2)
        desc = match.group(3).strip()

        # Extract icon from menu_icon or use fa-landmark default
        icon = "fa-landmark"
        topics.append({"title": title_text, "link": link, "desc": desc, "icon": icon})

    # Generate cards HTML
    cards_html = ""
    for topic in topics:
        cards_html += f'''    <a href="{safe_href(topic['link'])}" class="card">
      <div class="title-row">
        <i class="fas {topic['icon']}"></i>
        <h2 class="title">{html.escape(topic['title'])}</h2>
      </div>
      <p class="desc">{html.escape(topic['desc'])}</p>
    </a>\n'''

    # Replace markers
    html_out = template.replace("<!-- AUTO:TITLE -->", html.escape(title))
    html_out = html_out.replace("<!-- AUTO:SUBTITLE -->", html.escape(subtitle))
    html_out = html_out.replace("<!-- AUTO:FOOTER -->", html.escape(footer))
    html_out = html_out.replace("      <!-- AUTO:CARDS:START -->\n      <!-- AUTO:CARDS:END -->", f"      <!-- AUTO:CARDS:START -->\n{cards_html}      <!-- AUTO:CARDS:END -->")

    # Inject logo as data URI
    logo_path = out_path.parent / "logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
            mime_type, _ = mimetypes.guess_type(str(logo_path))
            logo_uri = f"data:{mime_type};base64,{logo_b64}"
            html_out = html_out.replace('src="logo.png"', f'src="{logo_uri}"')

    return html_out


def main() -> None:
    args = parse_args()

    md_path = Path(args.input_md)
    tpl_path = Path(args.template)
    out_path = Path(args.output_html)

    # Special handling for index page
    if out_path.name == "index.html":
        html_out = generate_index_page(md_path, out_path)
        out_path.write_text(html_out, encoding="utf-8")
        print(f"OK: {out_path} gerado como landing page.")
        return

    markdown = md_path.read_text(encoding="utf-8")
    template = tpl_path.read_text(encoding="utf-8")

    cards = parse_markdown(markdown, md_path.parent, section_mode=args.section_mode)
    card_icons = assign_unique_icons(cards, args.menu_icon)
    content_html = render_cards(cards, card_icons)
    primary_h1 = extract_h1_title(markdown)
    menu_group_title = clean_md_title(primary_h1) or clean_md_title(args.page_title)
    topics_html = render_topics_accordion(out_path, cards, card_icons, args.menu_icon)

    html_out = replace_between(template, CONTENT_START, CONTENT_END, content_html)
    html_out = replace_between(html_out, TOPICS_START, TOPICS_END, topics_html)
    html_out = apply_global_page_rules(html_out, out_path, md_path, args.page_title, menu_group_title)

    out_path.write_text(html_out, encoding="utf-8")
    print(f"OK: {out_path} gerado a partir de {md_path} com {len(cards)} seção(ões).")
    validate_completeness(markdown, html_out, cards)
    validate_content_preservation(markdown, html_out)


if __name__ == "__main__":
    main()
