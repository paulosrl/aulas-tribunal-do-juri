#!/usr/bin/env python3
"""
Gerador de index.html a partir de conteudo/index.md
Arquivo de entrada deve conter:
- H1 (título da página)
- Linha vazia
- Bloco de metadados (site, subtítulo, rodapé)
- Linha vazia (separador ***)
- H2 tópicos com formato: "## Tópico N | Nome | link.html"
  Seguido por descrição em um parágrafo
"""

import argparse
import html
import re
from pathlib import Path


def safe_href(url: str) -> str:
    clean_url = re.sub(r"\\(.)", r"\1", url).strip()
    if re.match(r"^\s*javascript\s*:", clean_url, flags=re.IGNORECASE):
        return "#"
    return html.escape(clean_url, quote=True)


def parse_index_md(markdown: str) -> dict:
    """Parse index.md e extrai: título, metadados, tópicos"""
    lines = markdown.split('\n')
    data = {
        'title': '',
        'site': '',
        'subtitle': '',
        'footer': '',
        'topics': []
    }

    i = 0

    # Extrair H1
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('# '):
            data['title'] = line[2:].strip()
            i += 1
            break
        i += 1

    # Pular linhas vazias
    while i < len(lines) and not lines[i].strip():
        i += 1

    # Extrair metadados até encontrar ***
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('***') or line.startswith('---'):
            i += 1
            break
        if line.startswith('**site:**'):
            data['site'] = line.replace('**site:**', '').strip()
        elif line.startswith('**subtítulo:**'):
            data['subtitle'] = line.replace('**subtítulo:**', '').strip()
        elif line.startswith('**rodapé:**'):
            data['footer'] = line.replace('**rodapé:**', '').strip()
        i += 1

    # Pular linhas vazias
    while i < len(lines) and not lines[i].strip():
        i += 1

    # Extrair tópicos (H2)
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('## '):
            # Parse: "## Tópico 1 | Nome | link.html"
            header = line[3:].strip()
            parts = [p.strip() for p in header.split('|')]
            if len(parts) >= 3:
                tag = parts[0]
                title = parts[1]
                href = parts[2]

                # Próxima linha pode ser vazia, então pula
                i += 1
                desc = ''
                # Procura a descrição (primeira linha não-vazia depois do H2)
                while i < len(lines):
                    candidate = lines[i].strip()
                    if candidate and not candidate.startswith('##') and not candidate.startswith('***'):
                        desc = candidate
                        break
                    elif candidate.startswith('***') or candidate.startswith('##'):
                        break
                    i += 1

                data['topics'].append({
                    'tag': tag,
                    'title': title,
                    'href': href,
                    'desc': desc
                })
        i += 1

    return data


def generate_cards_html(topics: list) -> str:
    """Gera HTML dos cards a partir dos tópicos"""
    icons = [
        '<svg class="topic-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M10 17.5L4.5 12 6 10.5l4 4 8-8L19.5 8z"/></svg>',
        '<svg class="topic-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 17.25V21h3.75L17.8 9.94l-3.75-3.75L3 17.25zm18-11.5a1 1 0 0 0 0-1.41l-1.34-1.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75L21 5.75z"/></svg>',
        '<svg class="topic-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M1 21h12v2H1v-2zm2-3h10v2H3v-2zm5-16l8 8-6 6-8-8 6-6zm6.59 8L8 3.41 4.41 7 11 13.59 14.59 10z"/></svg>',
        '<svg class="topic-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 3h18v4H3V3zm0 7h8v11H3V10zm10 0h8v11h-8V10z"/></svg>',
        '<svg class="topic-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 5h16a2 2 0 0 1 2 2v12l-4-3-4 3-4-3-4 3V7a2 2 0 0 1 2-2z"/></svg>',
        '<svg class="topic-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 17.27 6.18 3.73-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>'
    ]

    cards = []
    for idx, topic in enumerate(topics):
        icon = icons[idx % len(icons)]
        card = f'''      <a class="card" href="{safe_href(topic['href'])}">
        <span class="tag">{topic['tag']}</span>
        <div class="title-row">
          {icon}
          <p class="title">{topic['title']}</p>
        </div>
        <p class="desc">{topic['desc']}</p>
      </a>'''
        cards.append(card)

    return '\n'.join(cards)


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    """Replace conteúdo entre dois marcadores"""
    pattern = f'{re.escape(start_marker)}.*?{re.escape(end_marker)}'
    new_content = f'{start_marker}\n{replacement}\n      {end_marker}'
    return re.sub(pattern, new_content, text, flags=re.DOTALL)


def main():
    parser = argparse.ArgumentParser(description='Gera index.html a partir de conteudo/index.md')
    parser.add_argument('input_md', help='Arquivo markdown de entrada (conteudo/index.md)')
    parser.add_argument('output_html', help='Arquivo html de saída (html/index.html)')
    parser.add_argument('--template', default='templates/index.template.html', help='Template HTML')

    args = parser.parse_args()

    md_path = Path(args.input_md)
    html_path = Path(args.output_html)
    tpl_path = Path(args.template)

    # Validações
    if not md_path.exists():
        raise FileNotFoundError(f'Arquivo Markdown não encontrado: {md_path}')
    if not tpl_path.exists():
        raise FileNotFoundError(f'Template não encontrado: {tpl_path}')

    # Ler e parsear Markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        markdown = f.read()

    data = parse_index_md(markdown)

    # Gerar HTML dos cards
    cards_html = generate_cards_html(data['topics'])

    # Ler template
    with open(tpl_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Substituir marcadores
    html_out = template.replace('<!-- AUTO:TITLE -->', data['title'])
    html_out = html_out.replace('<!-- AUTO:SUBTITLE -->', data['subtitle'])
    html_out = html_out.replace('<!-- AUTO:FOOTER -->', data['footer'])
    html_out = replace_between(html_out, '<!-- AUTO:CARDS:START -->', '<!-- AUTO:CARDS:END -->', cards_html)

    # Gravar HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_out)

    print(f'✅ OK: {html_path} gerado a partir de {md_path}')


if __name__ == '__main__':
    main()
