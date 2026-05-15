import re
import html
from typing import List
from pathlib import Path

from html_gen.utils import esc, safe_href, clean_md_title, strip_leading_number
from html_gen.icons import pick_icon, pick_item_icon
from html_gen.constants import TOPIC_NAV_ITEMS, NUMBERED_TOPIC_PAGES
from html_gen.models import Card


def _default_authors_meta_html() -> str:
    return (
        '<div class="authors-meta">\n'
        '  <div class="authors-org authors-org-first">Ministério Público do Estado do Pará - MPPA</div>\n'
        '  <div class="authors-org">Comitê de Governança da Inovação e Inteligência Artificial - CIIA</div>\n'
        '  <div class="authors-org">Grupo de Atuação Especial do Júri – GAEJÚRI</div>\n'
        '  <div class="authors-date">Inteligência Artificial Aplicada ao Tribunal do Júri - 14 e 15 de maio de 2025</div>\n'
        '  <div class="authors-note-row">\n'
        '    <div class="authors-note">Material produzido com apoio de ferramentas de IA por:</div>\n'
        '    <div class="authors-badges"><span class="author-badge"><span class="author-icon"><i class="fas fa-user-tie"></i></span> Rodrigo Aquino</span><span class="author-badge"><span class="author-icon"><i class="fas fa-user-tie"></i></span> Paulo Lima</span></div>\n'
        "  </div>\n"
        "</div>"
    )


def render_copilot_agent_cta(url: str) -> str:
    safe_url = safe_href(url)
    return (
        f'<a href="{safe_url}" class="copilot-agent-cta" target="_blank">'
        '<span class="copilot-agent-cta-icon" aria-hidden="true"></span>'
        '<span class="copilot-agent-cta-label">Acessar Agente Copilot</span>'
        '<i class="fas fa-external-link-alt" aria-hidden="true"></i>'
        "</a>"
    )


def inline_md(text: str) -> str:
    """Convert markdown inline formatting to HTML."""
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


def render_cards(cards: List[Card], card_icons: List[str]) -> str:
    def _is_summary_title(title: str) -> bool:
        t = clean_md_title(title).lower()
        return ("sumário" in t) or ("sumario" in t)

    def _is_main_summary_title(title: str) -> bool:
        t = clean_md_title(title)
        t = strip_leading_number(t).strip().lower()
        t = re.sub(r"[^a-zà-ÿ0-9]+", "", t)
        return t == "sumario"

    has_summary_card = any(_is_main_summary_title(c.title) for c in cards)

    if cards:
        first_card = cards[0]
        authors_block = None
        kept_blocks: List[str] = []
        for block in first_card.blocks:
            if authors_block is None and 'class="authors-meta"' in (block or ""):
                authors_block = block
                continue
            kept_blocks.append(block)
        first_card.blocks = kept_blocks
        if authors_block is None:
            authors_block = _default_authors_meta_html()
        header_title = first_card.title.strip()
        cards.insert(0, Card(level=1, title=header_title, blocks=[authors_block]))
        if not first_card.blocks:
            cards.pop(1)

    def _include_in_navigation(idx: int, card: Card) -> bool:
        if idx == 1 and card.level == 1:
            return False
        if _is_summary_title(card.title):
            return False
        return True

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
        # O sumário deve espelhar o submenu esquerdo: sem o item "Sumário".
        entries: List[tuple[int, str]] = []
        for target_idx, target_card in enumerate(cards, start=1):
            if not _include_in_navigation(target_idx, target_card):
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
                f'<p><a class="summary-link" href="#p{tgt}"><span class="num-badge">{i}</span> '
                f"<strong>{inline_md(label)}</strong></a></p>"
            )
        return "\n".join(rows)

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
        if _is_summary_title(card.title):
            title = "Sumário"
            icon = "fa-book-open"
        if htag == "h2":
            title = strip_leading_number(title)
            title = re.sub(r"^\d+(?:\.\d+)*[\.\-\)]?\s*", "", title).strip()
        if not title:
            title = f"Seção {idx}"
        out.append(f'            <section id="{section_id}" class="caor-card">')
        is_first_header_card = idx == 1 and any('class="authors-meta"' in (b or "") for b in card.blocks)
        if not is_first_header_card:
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
        if is_first_header_card and has_summary_card:
            out.append(f'                <{htag}><i class="fas {icon}"></i> {inline_md(title)}</{htag}>')
        out.append("            </section>")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_menu_from_labels(cards: List[Card], card_icons: List[str], menu_icon: str) -> str:
    def _is_summary_title(title: str) -> bool:
        t = clean_md_title(title).lower()
        return ("sumário" in t) or ("sumario" in t)

    def _submenu_entries() -> list[tuple[int, str, str]]:
        entries: list[tuple[int, str, str]] = []
        for idx, card in enumerate(cards, start=1):
            if idx == 1 and card.level == 1:
                continue
            if _is_summary_title(card.title):
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
