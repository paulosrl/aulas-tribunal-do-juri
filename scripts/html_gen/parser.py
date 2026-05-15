"""
Parser module: Markdown → List[Card] conversion.

Core parsing logic for converting markdown source documents into structured
Card objects with HTML blocks for rendering.
"""

import re
from pathlib import Path
from typing import List

from html_gen.constants import AGENT_HEADER_PAT, COURSE_DATE_LABEL
from html_gen.models import Card
from html_gen.utils import (
    esc,
    safe_href,
    inline_md,
    clean_md_title,
    strip_leading_number,
)
from html_gen.icons import pick_icon, pick_item_icon
from html_gen.classifier import (
    is_page_marker_line,
    is_page_comment_line,
    is_separator_line,
    is_ocr_comment_line,
    classify_critical_paragraph,
    is_strategic_paragraph,
)


def strip_source_references(text: str) -> str:
    """
    Remove APENAS referências automáticas de ferramentas (SharePoint, Copilot Chat).
    Preserva links úteis como m365.cloud.microsoft (agentes) e claude.ai.
    """
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
    """Extract the H1 title from markdown source."""
    for raw in markdown.splitlines():
        line = raw.strip()
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            return clean_md_title(m.group(1))
    return ""


def parse_authors_line(text: str) -> tuple[str, str, str] | None:
    """
    Parse authors metadata line.

    Example: "Autores: Rodrigo Aquino e Paulo Lima | Ministério Público do Pará - MPPA | 14 e 15 de maio de 2026"
    Returns: (authors, org, date) tuple.
    """
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
    """
    Parse agent block: description, pillars, and access link.

    Returns: (html_block, next_line_index) tuple.
    """
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

    # Import here to avoid circular dependency
    from html_gen.icons import pick_agent_icon

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
    """
    Split key-value item from markdown.

    Acepta padrões como:
    - ⚖️ **Atividade-Fim:** Conteúdo...
    - **Atividade-Fim:** Conteúdo...
    """
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
    """
    Extract agent access URL from paragraph text.

    Matches:
    - "Acesse o agente: [Label](https://...)"
    - "Acesse o agente: https://..."
    """
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
    """Render CTA (Call-to-Action) button for Copilot agent access."""
    safe_url = safe_href(url)
    return (
        f'<a href="{safe_url}" class="copilot-agent-cta" target="_blank">'
        '<span class="copilot-agent-cta-icon" aria-hidden="true"></span>'
        '<span class="copilot-agent-cta-label">Acessar Agente Copilot</span>'
        '<i class="fas fa-external-link-alt" aria-hidden="true"></i>'
        "</a>"
    )


def derive_page_card_title(lines: List[str], start_idx: int) -> str:
    """
    Derive card title from lines, prioritizing headings and bold text.

    Used in page mode to infer section title from context.
    """
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


def file_to_data_uri(path: Path) -> str:
    """Convert image file to data URI for embedding."""
    import base64
    import mimetypes

    mime, _ = mimetypes.guess_type(path.name)
    safe_mime = mime or "application/octet-stream"
    content_b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{safe_mime};base64,{content_b64}"


def parse_markdown(markdown: str, md_dir: Path, section_mode: str = "semantic") -> List[Card]:
    """
    MAIN PARSER: Convert markdown to List[Card].

    This is the core parsing engine that:
    1. Strips source references
    2. Detects page markers and section mode
    3. Iterates through lines parsing:
       - Headings (H1, H2, H3)
       - Agent blocks
       - Lists (unordered, ordered, key-value)
       - Tables (markdown pipe format)
       - Blockquotes and alerts
       - Images (embedded as data URI)
       - Paragraphs (with inline markdown)
    4. Applies semantic classification (strategic, critical)
    5. Returns ordered list of Card objects
    """
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

        # Padrão «pergunta + link»: parágrafo que abre com aspas seguido de URL pura
        # → emite bloco practice-card destacado
        _starts_with_quote = re.match(r'^[\u201c\u201d"]', paragraph_text)
        if _starts_with_quote:
            # Avança por linhas vazias até encontrar o próximo parágrafo não-vazio
            _j = i
            while _j < len(lines) and not lines[_j].strip():
                _j += 1
            _next_line = lines[_j].strip() if _j < len(lines) else ""
            _url_match = re.match(r'^(https?://\S+)$', _next_line)
            if _url_match:
                _practice_url = _url_match.group(1)
                _safe_url = safe_href(_practice_url)
                # Texto da pergunta: remove aspas envolventes se existirem
                _question = paragraph_text.strip().strip('\u201c\u201d"').strip().rstrip('\u201d"').strip()
                current.blocks.append(
                    '<div class="practice-card">\n'
                    '  <div class="practice-card-header">\n'
                    '    <span class="practice-card-icon"><i class="fas fa-flask"></i></span>\n'
                    '    <span class="practice-card-label">Experimente</span>\n'
                    '  </div>\n'
                    f'  <p class="practice-card-question">\u201c{esc(_question)}\u201d</p>\n'
                    f'  <a href="{_safe_url}" class="practice-card-btn" target="_blank" rel="noopener noreferrer">'
                    '<i class="fas fa-external-link-alt"></i> Testar agente</a>\n'
                    '</div>'
                )
                i = _j + 1  # consome a linha da URL
                continue
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
                author_badges.append(
                    f'<span class="author-badge"><span class="author-icon"><i class="fas fa-user-tie"></i></span> {inline_md(name)}</span>'
                )
            if not author_badges:
                author_badges.append(
                    f'<span class="author-badge"><span class="author-icon"><i class="fas fa-user-tie"></i></span> {inline_md(authors)}</span>'
                )
            # Padrão institucional fixo definido para o bloco de autores.
            # Mantemos estrutura padrão em todas as páginas.
            org_html = (
                "  <div class=\"authors-org authors-org-first\">Ministério Público do Estado do Pará - MPPA</div>\n"
                "  <div class=\"authors-org\">Comitê de Governança da Inovação e Inteligência Artificial - CIIA</div>\n"
                "  <div class=\"authors-org\">Grupo de Atuação Especial do Júri – GAEJÚRI</div>\n"
            )
            date_html = f'    <div class="authors-date">{COURSE_DATE_LABEL}</div>'
            current.blocks.append(
                '<div class="authors-meta">\n'
                f"{org_html}"
                '  <div class="authors-date-row">\n'
                f"{date_html}\n"
                f'    <div class="authors-badges">{"".join(author_badges)}</div>\n'
                "  </div>\n"
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

    # Remove intro apenas quando realmente vazio (sem blocos e sem título).
    # Isso preserva H1s de abertura como "Sites Abertos" em páginas como Favoritos.
    if len(cards) > 1 and not cards[0].blocks and not cards[0].title.strip():
        cards = cards[1:]

    return cards
