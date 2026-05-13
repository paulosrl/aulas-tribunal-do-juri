# Graph Report - aulas-tribunal-do-juri  (2026-05-12)

## Corpus Check
- 1 files · ~37,931 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 32 nodes · 116 edges · 6 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fa2505b1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]

## God Nodes (most connected - your core abstractions)
1. `build_topico.py` - 30 edges
2. `parse_markdown()` - 21 edges
3. `clean_md_title()` - 15 edges
4. `main()` - 13 edges
5. `derive_page_card_title()` - 8 edges
6. `render_cards()` - 8 edges
7. `esc()` - 7 edges
8. `strip_leading_number()` - 7 edges
9. `pick_icon()` - 7 edges
10. `render_menu_from_labels()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `parse_markdown()` --calls--> `esc()`  [EXTRACTED]
  scripts/gera_html.py → scripts/gera_html.py  _Bridges community 2 → community 0_
- `render_menu_from_labels()` --calls--> `esc()`  [EXTRACTED]
  scripts/gera_html.py → scripts/gera_html.py  _Bridges community 2 → community 5_
- `render_cards()` --calls--> `inline_md()`  [EXTRACTED]
  scripts/gera_html.py → scripts/gera_html.py  _Bridges community 2 → community 1_
- `extract_h1_title()` --calls--> `clean_md_title()`  [EXTRACTED]
  scripts/gera_html.py → scripts/gera_html.py  _Bridges community 3 → community 1_
- `parse_markdown()` --calls--> `parse_authors_line()`  [EXTRACTED]
  scripts/gera_html.py → scripts/gera_html.py  _Bridges community 1 → community 0_

## Communities (6 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.43
Nodes (8): build_topico.py, Card, file_to_data_uri(), is_page_marker_line(), normalize_data_uri(), parse_markdown(), split_key_value_item(), strip_source_references()

### Community 1 - "Community 1"
Cohesion: 0.36
Nodes (8): classify_critical_paragraph(), clean_md_title(), is_strategic_paragraph(), parse_authors_line(), parse_menu_md(), pick_item_icon(), render_cards(), strip_leading_number()

### Community 2 - "Community 2"
Cohesion: 0.7
Nodes (4): apply_global_page_rules(), esc(), inline_md(), render_topics_menu()

### Community 3 - "Community 3"
Cohesion: 0.5
Nodes (4): extract_h1_title(), main(), parse_args(), replace_between()

### Community 4 - "Community 4"
Cohesion: 0.5
Nodes (4): derive_page_card_title(), is_ocr_comment_line(), is_page_comment_line(), is_separator_line()

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (3): assign_unique_icons(), pick_icon(), render_menu_from_labels()

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_topico.py` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.310) - this node is a cross-community bridge._
- **Why does `parse_markdown()` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `clean_md_title()` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._