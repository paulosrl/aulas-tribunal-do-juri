import argparse
import base64
import mimetypes
import re
from pathlib import Path
from typing import List
from html_gen.constants import MENU_START, MENU_END, CONTENT_START, CONTENT_END, TOPICS_START, TOPICS_END
from html_gen.utils import esc, safe_href, replace_between
from html_gen.parser import parse_markdown, extract_h1_title
from html_gen.renderer import render_cards, render_menu_from_labels, render_topics_accordion
from html_gen.postprocessor import apply_global_page_rules
from html_gen.icons import assign_unique_icons
from html_gen.validation import validate_completeness, validate_content_preservation


def _card_has_meaningful_content(card) -> bool:
    """Return True when card has at least one non-empty content block."""
    for block in card.blocks:
        if block and block.strip():
            return True
    return False


def _strip_removed_empty_headings(markdown: str, removed_titles: list[str]) -> str:
    """
    Remove heading lines from markdown validation input when those sections were
    intentionally dropped for being empty.
    """
    if not removed_titles:
        return markdown
    title_set = {t.strip().lower() for t in removed_titles if t and t.strip()}
    out_lines: list[str] = []
    for raw in markdown.splitlines():
        m = re.match(r"^\s*#{1,6}\s+(.*)$", raw)
        if not m:
            out_lines.append(raw)
            continue
        heading_text = re.sub(r"\s+", " ", m.group(1)).strip()
        if heading_text.lower() in title_set:
            continue
        out_lines.append(raw)
    return "\n".join(out_lines)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the HTML generator."""
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
        "--section-mode",
        choices=("semantic", "page"),
        default="semantic",
        help="Modo de seções: 'semantic' (padrão, estilo topico1) ou 'page' (1 seção por página marcada).",
    )
    return parser.parse_args()


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
        <h2 class="title">{esc(topic['title'])}</h2>
      </div>
      <p class="desc">{esc(topic['desc'])}</p>
    </a>\n'''

    # Replace markers
    html_out = template.replace("<!-- AUTO:TITLE -->", esc(title))
    html_out = html_out.replace("<!-- AUTO:SUBTITLE -->", esc(subtitle))
    html_out = html_out.replace("<!-- AUTO:FOOTER -->", esc(footer))
    html_out = html_out.replace("      <!-- AUTO:CARDS:START -->\n      <!-- AUTO:CARDS:END -->", f"      <!-- AUTO:CARDS:START -->\n{cards_html}      <!-- AUTO:CARDS:END -->")

    # Inject logo as data URI
    logo_path = out_path.parent / "logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
            mime_type, _ = mimetypes.guess_type(str(logo_path))
            logo_uri = f"data:{mime_type};base64,{logo_b64}"
            html_out = html_out.replace('src="logo.png"', f'src="{logo_uri}"')

    # Inject mppa symbol as data URI
    mppa_path = out_path.parent / "mppa.png"
    if mppa_path.exists():
        with open(mppa_path, "rb") as f:
            mppa_b64 = base64.b64encode(f.read()).decode("utf-8")
            mime_type, _ = mimetypes.guess_type(str(mppa_path))
            mppa_uri = f"data:{mime_type};base64,{mppa_b64}"
            html_out = html_out.replace('src="mppa.png"', f'src="{mppa_uri}"')

    return html_out


def main() -> None:
    """Main entry point: orchestrates parsing, rendering, and validation."""
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
    original_cards_count = len(cards)
    removed_empty_titles = [c.title for c in cards if not _card_has_meaningful_content(c)]
    cards = [c for c in cards if _card_has_meaningful_content(c)]
    removed_empty_cards = original_cards_count - len(cards)

    card_icons = assign_unique_icons(cards, args.menu_icon)
    content_html = render_cards(cards, card_icons)
    primary_h1 = extract_h1_title(markdown)
    menu_group_title = primary_h1 or args.page_title
    topics_html = render_topics_accordion(out_path, cards, card_icons, args.menu_icon)

    html_out = replace_between(template, CONTENT_START, CONTENT_END, content_html)
    html_out = replace_between(html_out, TOPICS_START, TOPICS_END, topics_html)
    html_out = apply_global_page_rules(html_out, out_path, md_path, args.page_title, menu_group_title)

    out_path.write_text(html_out, encoding="utf-8")
    print(f"OK: {out_path} gerado a partir de {md_path} com {len(cards)} seção(ões).")
    if removed_empty_cards:
        print(f"INFO: {removed_empty_cards} seção(ões) vazia(s) foram removidas automaticamente.")
    validate_completeness(markdown, html_out, cards)
    validation_markdown = _strip_removed_empty_headings(markdown, removed_empty_titles)
    validate_content_preservation(validation_markdown, html_out)


if __name__ == "__main__":
    main()
