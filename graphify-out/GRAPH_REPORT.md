# Graph Report - aulas-tribunal-do-juri  (2026-05-13)

## Corpus Check
- 2 files · ~116,726 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 92 nodes · 251 edges · 11 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `eec9c6dc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]

## God Nodes (most connected - your core abstractions)
1. `build_topico.py` - 30 edges
2. `parse_markdown()` - 23 edges
3. `parse_markdown()` - 21 edges
4. `clean_md_title()` - 16 edges
5. `clean_md_title()` - 15 edges
6. `main()` - 14 edges
7. `main()` - 13 edges
8. `generate_index_page()` - 12 edges
9. `validate_content_preservation()` - 10 edges
10. `esc()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `pick_agent_icon()` --calls--> `clean_md_title()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 1 → community 3_
- `parse_markdown()` --calls--> `esc()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 1 → community 8_
- `extract_h1_title()` --calls--> `clean_md_title()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 9 → community 3_
- `parse_markdown()` --calls--> `parse_authors_line()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 3 → community 8_
- `is_page_marker_line()` --calls--> `clean_md_title()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 3 → community 4_

## Communities (11 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.27
Nodes (13): apply_global_page_rules(), assign_unique_icons(), esc(), extract_h1_title(), file_to_data_uri(), main(), normalize_data_uri(), parse_args() (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (10): apply_global_page_rules(), esc(), file_to_data_uri(), inline_md(), parse_agent_block(), pick_agent_icon(), render_copilot_agent_cta(), render_menu_from_labels() (+2 more)

### Community 2 - "Community 2"
Cohesion: 0.18
Nodes (11): generate_index_page(), Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.29
Nodes (10): assign_unique_icons(), classify_critical_paragraph(), clean_md_title(), is_strategic_paragraph(), parse_authors_line(), parse_menu_md(), pick_icon(), pick_item_icon() (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.31
Nodes (9): derive_page_card_title(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line(), Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v, Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v, Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.53
Nodes (9): build_topico.py, Card, derive_page_card_title(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line(), parse_markdown() (+1 more)

### Community 6 - "Community 6"
Cohesion: 0.36
Nodes (7): generate_cards_html(), main(), parse_index_md(), Replace conteúdo entre dois marcadores, Parse index.md e extrai: título, metadados, tópicos, Gera HTML dos cards a partir dos tópicos, replace_between()

### Community 7 - "Community 7"
Cohesion: 0.4
Nodes (6): classify_critical_paragraph(), clean_md_title(), is_strategic_paragraph(), parse_authors_line(), parse_menu_md(), strip_leading_number()

### Community 8 - "Community 8"
Cohesion: 0.4
Nodes (5): Card, extract_agent_access_url(), parse_markdown(), split_key_value_item(), strip_source_references()

### Community 9 - "Community 9"
Cohesion: 0.4
Nodes (5): extract_h1_title(), main(), parse_args(), replace_between(), validate_completeness()

### Community 10 - "Community 10"
Cohesion: 0.67
Nodes (3): inline_md(), pick_item_icon(), render_cards()

## Knowledge Gaps
- **16 isolated node(s):** `Parse index.md e extrai: título, metadados, tópicos`, `Gera HTML dos cards a partir dos tópicos`, `Replace conteúdo entre dois marcadores`, `Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v`, `Generate landing page with index.template.html` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `generate_index_page()` connect `Community 2` to `Community 1`, `Community 9`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `validate_content_preservation()` connect `Community 4` to `Community 1`, `Community 3`, `Community 9`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `build_topico.py` connect `Community 5` to `Community 0`, `Community 10`, `Community 7`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **What connects `Parse index.md e extrai: título, metadados, tópicos`, `Gera HTML dos cards a partir dos tópicos`, `Replace conteúdo entre dois marcadores` to the rest of the system?**
  _16 weakly-connected nodes found - possible documentation gaps or missing edges._