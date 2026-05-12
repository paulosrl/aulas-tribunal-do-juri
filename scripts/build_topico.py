#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import html
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
    return parser.parse_args()


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def inline_md(text: str) -> str:
    text = esc(text)
    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!])", r"\1", text)
    text = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", lambda m: f"<strong>{m.group(1)}</strong>", text)
    text = re.sub(r"\*([^*]+)\*", lambda m: f"<em>{m.group(1)}</em>", text)
    return text


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
    t = re.sub(r"^\d+\s*[\.\-\)]\s*", "", t)
    return t.strip()


def pick_icon(title: str, fallback: str = "fa-list-ol") -> str:
    t = clean_md_title(title).lower()
    for keywords, icon in ICON_RULES:
        if any(k in t for k in keywords):
            return icon
    return fallback


def pick_item_icon(text: str) -> str:
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


def parse_markdown(markdown: str) -> List[Card]:
    lines = markdown.splitlines()
    cards: List[Card] = []

    # H1 global vira primeiro card de abertura
    h1 = None
    for line in lines:
        m = re.match(r"^#\s+(.+)$", line.strip())
        if m:
            h1 = m.group(1).strip()
            break

    intro = Card(title=h1 or "Tópico", level=1)
    cards.append(intro)
    current = intro

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip("\n")
        line = raw.strip()

        if not line:
            i += 1
            continue

        # headings
        m2 = re.match(r"^##\s+(.+)$", line)
        if m2:
            current = Card(title=clean_md_title(m2.group(1)), level=2)
            cards.append(current)
            i += 1
            continue

        # linha inteira em negrito vira novo tópico (padrão comum do curso)
        mb = re.match(r"^\*\*([^*]+)\*\*$", line)
        if mb:
            candidate = clean_md_title(mb.group(1))
            # Só promove negrito puro a título quando é texto curto (evita transformar parágrafos em menu)
            if len(candidate) <= 120:
                current = Card(title=candidate, level=2)
                cards.append(current)
                i += 1
                continue

        m3 = re.match(r"^###\s+(.+)$", line)
        if m3:
            h3_title = clean_md_title(m3.group(1))
            h3_icon = pick_icon(h3_title, "fa-star")
            current.blocks.append(f'<h3><i class="fas {h3_icon}"></i> {inline_md(h3_title)}</h3>')
            i += 1
            continue

        # H1 já foi capturado como título global, então não deve virar parágrafo
        m1 = re.match(r"^#\s+(.+)$", line)
        if m1:
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

                table_html = []
                table_html.append('<div class="table-wrapper">')
                table_html.append("<table>")
                table_html.append("<thead>")
                table_html.append("<tr>")
                for h in header_cells:
                    table_html.append(f"<th style=\"white-space: nowrap;\">{inline_md(h)}</th>")
                table_html.append("</tr>")
                table_html.append("</thead>")
                table_html.append("<tbody>")
                for r in norm_rows:
                    table_html.append("<tr>")
                    for c in r:
                        table_html.append(f"<td style=\"white-space: nowrap;\">{inline_md(c)}</td>")
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
            if re.match(r"^(#|##|###)\s+", nxt):
                break
            if nxt.startswith(">"):
                break
            if re.match(r"^[-*]\s+", nxt) or re.match(r"^\d+\.\s+", nxt):
                break
            para.append(nxt)
            i += 1
        paragraph_text = " ".join(para)
        critical = classify_critical_paragraph(paragraph_text)
        if critical:
            label, icon = critical
            current.blocks.append(
                '<div class="alert-box alert-critical">\n'
                f'<span class="badge"><i class="fas {icon}"></i> {inline_md(label)}</span>\n'
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
    out = []
    for idx, card in enumerate(cards, start=1):
        section_id = f"p{idx}"
        htag = "h1" if card.level == 1 else "h2"
        icon = card_icons[idx - 1] if idx - 1 < len(card_icons) else pick_icon(card.title, "fa-book-open")
        title = clean_md_title(card.title)
        if htag == "h2":
            title = f"{idx}. {strip_leading_number(title)}"
        out.append(f'            <section id="{section_id}" class="caor-card">')
        out.append(f'                <{htag}><i class="fas {icon}"></i> {inline_md(title)}</{htag}>')
        is_single_plain_paragraph = (
            len(card.blocks) == 1
            and card.blocks[0].strip().startswith("<p>")
            and card.blocks[0].strip().endswith("</p>")
        )

        if is_single_plain_paragraph:
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
                for bl in block.splitlines():
                    out.append(f"                {bl}")
        out.append("            </section>")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def parse_menu_md(menu_md_path: Path) -> tuple[str, list[str]]:
    if not menu_md_path.exists():
        return ("Introdução", [])

    title = "Introdução"
    items: list[str] = []
    for raw in menu_md_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        m1 = re.match(r"^#\s+(.+)$", line)
        if m1:
            title = clean_md_title(m1.group(1))
            continue
        m2 = re.match(r"^[-*]\s+(.+)$", line)
        if m2:
            items.append(strip_leading_number(m2.group(1)))
            continue
        m3 = re.match(r"^\d+\.\s+(.+)$", line)
        if m3:
            items.append(strip_leading_number(m3.group(1)))
            continue
    return (title or "Introdução", items)


def render_menu_from_labels(cards: List[Card], card_icons: List[str], menu_icon: str) -> str:
    links = []
    for idx, card in enumerate(cards, start=1):
        short = f"{idx}. {strip_leading_number(card.title)}"
        icon = card_icons[idx - 1] if idx - 1 < len(card_icons) else pick_icon(short, menu_icon)
        links.append(
            f'            <a href="#p{idx}" class="nav-l"><i class="fas {icon}"></i> {esc(short)}</a>'
        )
    return "\n".join(links) + "\n"


def render_topics_menu(out_path: Path, total_topics: int = 4) -> str:
    current_topic = None
    m = re.search(r"topico(\d+)\.html$", out_path.name, flags=re.IGNORECASE)
    if m:
        current_topic = int(m.group(1))

    links: list[str] = []
    topic_icons = [
        "fa-book-open",
        "fa-window-maximize",
        "fa-pencil-ruler",
        "fa-shield-halved",
        "fa-gavel",
        "fa-database",
        "fa-search",
        "fa-check-circle",
    ]
    for idx in range(1, total_topics + 1):
        if current_topic == idx:
            continue
        topic_icon = topic_icons[(idx - 1) % len(topic_icons)]
        topic_file = out_path.parent / f"topico{idx}.html"
        if topic_file.exists():
            links.append(
                f'            <a href="topico{idx}.html" class="nav-l"><i class="fas {topic_icon}"></i> Tópico {idx}</a>'
            )
        else:
            links.append(
                f'            <span class="nav-l nav-locked"><i class="fas {topic_icon}"></i> Tópico {idx} <i class="fas fa-lock"></i></span>'
            )
    return "\n".join(links) + ("\n" if links else "")


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"Marcadores não encontrados: {start_marker} ... {end_marker}")
    start_insert = start + len(start_marker)
    return text[:start_insert] + "\n" + replacement + text[end:]


def normalize_data_uri(raw_logo: str) -> str:
    cleaned = re.sub(r"\s+", "", raw_logo.strip())
    if cleaned.startswith("data:image"):
        return cleaned
    return f"data:image/png;base64,{cleaned}"


def apply_global_page_rules(html_out: str, out_path: Path, page_title: str, menu_group_title: str) -> str:
    # Regra 0: Título de página vindo de parâmetro de execução.
    safe_title = esc(page_title.strip() or "Defina o título da página")
    html_out = re.sub(r"<title>.*?</title>", f"<title>{safe_title}</title>", html_out, flags=re.IGNORECASE | re.DOTALL)

    safe_group_title = esc(menu_group_title.strip() or "Introdução")
    html_out = re.sub(
        r'(<span class="mobile-header-title">).*?(</span>)',
        rf"\1{safe_group_title}\2",
        html_out,
        flags=re.IGNORECASE | re.DOTALL,
    )
    html_out = re.sub(
        r'(<div class="nav-group-title">)\s*Aula 1\s*(</div>)',
        rf"\1{safe_group_title}\2",
        html_out,
        count=1,
        flags=re.IGNORECASE,
    )

    # Regra 1: Página inicial sempre aponta para index.html na mesma pasta.
    html_out = re.sub(r'href="\.\./index\.html"', 'href="index.html"', html_out, flags=re.IGNORECASE)

    # Regra 2: Logo vem de logo.png na pasta do arquivo de saída.
    logo_file = out_path.parent / "logo.png"
    if not logo_file.exists():
        raise FileNotFoundError(
            f"Arquivo obrigatório não encontrado: {logo_file}\n"
            f"Coloque logo.png no diretório {out_path.parent}"
        )
    logo_bytes = base64.b64encode(logo_file.read_bytes()).decode("ascii")
    logo_data_uri = f"data:image/png;base64,{logo_bytes}"

    html_out = re.sub(
        r'(<img[^>]*class="sidebar-logo"[^>]*src=")[^"]*(")',
        rf"\1{logo_data_uri}\2",
        html_out,
        flags=re.IGNORECASE,
    )
    return html_out


def main() -> None:
    args = parse_args()

    md_path = Path(args.input_md)
    tpl_path = Path(args.template)
    out_path = Path(args.output_html)
    menu_md_path = Path(args.menu_md)

    markdown = md_path.read_text(encoding="utf-8")
    template = tpl_path.read_text(encoding="utf-8")

    cards = parse_markdown(markdown)
    card_icons = assign_unique_icons(cards, args.menu_icon)
    content_html = render_cards(cards, card_icons)
    menu_group_title, _ = parse_menu_md(menu_md_path)
    menu_html = render_menu_from_labels(cards, card_icons, args.menu_icon)
    topics_html = render_topics_menu(out_path)

    html_out = replace_between(template, MENU_START, MENU_END, menu_html)
    html_out = replace_between(html_out, CONTENT_START, CONTENT_END, content_html)
    html_out = replace_between(html_out, TOPICS_START, TOPICS_END, topics_html)
    html_out = apply_global_page_rules(html_out, out_path, args.page_title, menu_group_title)

    out_path.write_text(html_out, encoding="utf-8")
    print(f"OK: {out_path} gerado a partir de {md_path} com {len(cards)} seção(ões).")


if __name__ == "__main__":
    main()
