# Graph Report - aulas-tribunal-do-juri  (2026-05-13)

## Corpus Check
- 2 files · ~71,313 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 102 nodes · 266 edges · 10 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `618e9535`
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

## God Nodes (most connected - your core abstractions)
1. `build_topico.py` - 30 edges
2. `parse_markdown()` - 23 edges
3. `parse_markdown()` - 21 edges
4. `clean_md_title()` - 16 edges
5. `generate_index_page()` - 16 edges
6. `clean_md_title()` - 15 edges
7. `main()` - 14 edges
8. `main()` - 13 edges
9. `validate_content_preservation()` - 12 edges
10. `esc()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `render_topics_menu()` --calls--> `esc()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py
- `Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v` --rationale_for--> `validate_content_preservation()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py
- `Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v` --rationale_for--> `validate_content_preservation()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py
- `Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v` --rationale_for--> `validate_content_preservation()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py
- `Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v` --rationale_for--> `validate_content_preservation()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py

## Communities (10 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (14): generate_index_page(), Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html (+6 more)

### Community 1 - "Community 1"
Cohesion: 0.21
Nodes (13): Card, classify_critical_paragraph(), derive_page_card_title(), extract_agent_access_url(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line() (+5 more)

### Community 2 - "Community 2"
Cohesion: 0.32
Nodes (12): apply_global_page_rules(), assign_unique_icons(), esc(), extract_h1_title(), inline_md(), main(), normalize_data_uri(), parse_args() (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.23
Nodes (11): generate_cards_html(), main(), parse_index_md(), Gera HTML dos cards a partir dos tópicos, Replace conteúdo entre dois marcadores, Replace conteúdo entre dois marcadores, Parse index.md e extrai: título, metadados, tópicos, Parse index.md e extrai: título, metadados, tópicos (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.42
Nodes (11): build_topico.py, Card, derive_page_card_title(), file_to_data_uri(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line() (+3 more)

### Community 5 - "Community 5"
Cohesion: 0.36
Nodes (8): apply_global_page_rules(), assign_unique_icons(), extract_h1_title(), file_to_data_uri(), main(), parse_args(), replace_between(), validate_completeness()

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (9): esc(), inline_md(), parse_agent_block(), pick_agent_icon(), render_copilot_agent_cta(), render_menu_from_labels(), render_topics_accordion(), render_topics_menu() (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.36
Nodes (8): classify_critical_paragraph(), clean_md_title(), is_strategic_paragraph(), parse_authors_line(), parse_menu_md(), pick_item_icon(), render_cards(), strip_leading_number()

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (6): Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v, Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v, Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v, Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v, Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v, validate_content_preservation()

### Community 9 - "Community 9"
Cohesion: 0.6
Nodes (6): clean_md_title(), parse_menu_md(), pick_icon(), pick_item_icon(), render_cards(), strip_leading_number()

## Knowledge Gaps
- **24 isolated node(s):** `Parse index.md e extrai: título, metadados, tópicos`, `Gera HTML dos cards a partir dos tópicos`, `Replace conteúdo entre dois marcadores`, `Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v`, `Generate landing page with index.template.html` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `generate_index_page()` connect `Community 0` to `Community 5`, `Community 6`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Why does `validate_content_preservation()` connect `Community 8` to `Community 9`, `Community 5`, `Community 1`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `main()` connect `Community 5` to `Community 0`, `Community 1`, `Community 6`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **What connects `Parse index.md e extrai: título, metadados, tópicos`, `Gera HTML dos cards a partir dos tópicos`, `Replace conteúdo entre dois marcadores` to the rest of the system?**
  _24 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._