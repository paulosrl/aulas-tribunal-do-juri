import re
import html
from typing import List
from html_gen.utils import clean_md_title


def validate_completeness(markdown: str, html_out: str, cards: List) -> None:
    """
    Validação de completude: verifica se links e cards vazios foram preservados.
    """
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

    def _is_separator_line(text: str) -> bool:
        line = text.strip()
        return bool(re.match(r"^(\*{3,}|-{3,}|_{3,})$", line))

    def _is_page_comment_line(text: str) -> bool:
        return bool(
            re.match(
                r"^<!--\s*(?:p[áa]gina|page)\s*[: ]\s*\d+\s*-->$",
                text.strip(),
                flags=re.IGNORECASE,
            )
        )

    def _is_page_marker_line(text: str) -> bool:
        line = text.strip()
        if not line:
            return False
        line_no_emoji = re.sub(r"^[\U0001F300-\U0001FAFF]+\s*", "", line)
        normalized = clean_md_title(line_no_emoji)
        patterns = [
            r"^<!--\s*p[áa]gina\s+\d+\s*-->$",
            r"^\*\*p[áa]gina\s+\d+\*\*$",
            r"^p[áa]gina\s+\d+$",
        ]
        return any(re.match(p, normalized, flags=re.IGNORECASE) for p in patterns)

    def _is_ocr_comment_line(text: str) -> bool:
        line = text.strip()
        return bool(re.match(r"^<!--\s*/?\s*ocr:image_[^>]*-->$", line, flags=re.IGNORECASE))

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
        if _is_separator_line(line) or _is_page_comment_line(line) or _is_page_marker_line(line) or _is_ocr_comment_line(line):
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
