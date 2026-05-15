# Graph Report - aulas-tribunal-do-juri  (2026-05-15)

## Corpus Check
- 32 files · ~93,607 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 550 nodes · 843 edges · 27 communities (24 shown, 3 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 53 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1d018250`
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
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]

## God Nodes (most connected - your core abstractions)
1. `3. Agentes/Assistentes Copilot para o Júri` - 43 edges
2. `build_topico.py` - 30 edges
3. `parse_markdown()` - 25 edges
4. `main()` - 23 edges
5. `parse_markdown()` - 23 edges
6. `parse_markdown()` - 21 edges
7. `**MÓDULO 2 — KIT DE PROMPTS**` - 16 edges
8. `clean_md_title()` - 16 edges
9. `generate_index_page()` - 16 edges
10. `clean_md_title()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Imprime cabeçalho visual` --rationale_for--> `print_header()`  [EXTRACTED]
  build_all.py → scripts/build_all.py
- `Imprime sumário final` --rationale_for--> `print_summary()`  [EXTRACTED]
  build_all.py → scripts/build_all.py
- `render_topics_menu()` --calls--> `esc()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py
- `Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v` --rationale_for--> `validate_content_preservation()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py
- `Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v` --rationale_for--> `validate_content_preservation()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py

## Communities (27 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (48): classify_critical_paragraph(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line(), is_strategic_paragraph(), assign_unique_icons(), pick_agent_icon() (+40 more)

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (42): apply_global_page_rules(), assign_unique_icons(), Card, classify_critical_paragraph(), clean_md_title(), derive_page_card_title(), esc(), extract_agent_access_url() (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.23
Nodes (31): build_topico.py, apply_global_page_rules(), assign_unique_icons(), Card, classify_critical_paragraph(), clean_md_title(), derive_page_card_title(), esc() (+23 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (29): append_generation_log(), _card_has_meaningful_content(), generate_index_page(), main(), parse_args(), Main entry point: orchestrates parsing, rendering, and validation., Main entry point: orchestrates parsing, rendering, and validation., Main entry point: orchestrates parsing, rendering, and validation. (+21 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (32): build_html(), build_page_title(), discover_markdown_files(), extract_h1_from_markdown(), get_project_root(), main(), parse_args(), print_header() (+24 more)

### Community 5 - "Community 5"
Cohesion: 0.32
Nodes (14): add_class(), apply_pattern(), get_topic_num(), has_class(), insert_lock_icon_in_card_title(), lock_attrs(), main(), parse_args() (+6 more)

### Community 6 - "Community 6"
Cohesion: 0.14
Nodes (14): generate_index_page(), Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html (+6 more)

### Community 7 - "Community 7"
Cohesion: 0.23
Nodes (11): generate_cards_html(), main(), parse_index_md(), Gera HTML dos cards a partir dos tópicos, Replace conteúdo entre dois marcadores, Replace conteúdo entre dois marcadores, Parse index.md e extrai: título, metadados, tópicos, Parse index.md e extrai: título, metadados, tópicos (+3 more)

### Community 8 - "Community 8"
Cohesion: 0.04
Nodes (47): 10. Júri Perguntas em AIJ Crim, 11. Júri Cross Examination, 12. Júri Advogado do Diabo, 13. Júri Análise de Audiência Degravada, 14. Júri Alegações Finais MP, 15. Júri Embargos de Declaração, 16. Júri Razões Recursais, 17. Júri Contrarrazões Recursais (+39 more)

### Community 9 - "Community 9"
Cohesion: 0.04
Nodes (47): **1.1 Aplicações Estratégicas Fundamentais**, **1.2 O Prompt Mestre: "Raio-X de Plenário"**, **3.1 Relatório Analítico de Julgamento (Trial Memo)**, **3.2 Análise FIRAC+ (Metodologia Avançada)**, **4.1 O "Transcritor Forense"**, **5.1 O "Simulador de Embate" — O Mais Recomendado**, **5.2 O "Briefing de Missão" — Visão da Equipe do MP**, **5.3 O "Simulador de Jurado Leigo"** (+39 more)

### Community 10 - "Community 10"
Cohesion: 0.07
Nodes (29): 10. O Retorno Real e a Fórmula da Alta Performance no Júri, 1. O Papel da IA no Ministério Público, 2. Contexto: A Base de Tudo, 3. A Janela de Contexto: Entrada, Saída e Limites, 4. Memória da IA: O Agora e O Sempre, 5. Os 5 Pilares da Engenharia de Contexto, 6. Os 5 Erros Críticos no Uso da IA, 7. Boas Práticas Institucionais e LGPD (+21 more)

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (27): 10. Síntese Estratégica e Boas Práticas, 11. Prompts para o Tribunal do Júri, 1. O que é Engenharia de Prompts, 2. Teoria e Prática da Engenharia de Prompts, 3. Os 4 Pilares de um Bom Prompt, 4. Exemplo Prático de Prompt Estruturado, 5. Metaprompting: Usando a IA para Criar Comandos, 6. Evolução do Usuário na Interação com IA (+19 more)

### Community 12 - "Community 12"
Cohesion: 0.09
Nodes (20): Arquitetura do Pipeline, code:bash (python3 scripts/build_all.py), code:bash (python3 scripts/gera_html.py conteudo/N.md html/N.html \), code:bash (# Travar tópicos 4, 5, 7), code:bash (# Primeiras 40 linhas), code:bash (python3 -m py_compile scripts/build_all.py scripts/gera_html), code:text (Inteligência Artificial Aplicada ao Tribunal do Júri — <Tópi), code:python (PAGE_TOPICS = {) (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.11
Nodes (18): Aulas: IA Aplicada ao Tribunal do Júri, Checklist de Revisão (Pente-fino), code:text (.), code:bash (python3 scripts/build_all.py), code:bash (python3 scripts/gera_html.py conteudo/3.md html/3.html \), code:bash (python3 -m py_compile scripts/build_all.py scripts/gera_html), code:bash (python3 scripts/lock_menu_items.py --items 4 5 6), code:bash (graphify update .) (+10 more)

### Community 14 - "Community 14"
Cohesion: 0.13
Nodes (14): Caso Feminicídio Tenente-Coronel SP, Clareza, Clareza, Persuasão e Precisão, Elementos Gráficos no Tribunal do Júri: Da investigação ao plenário: Visualizar para convencer, Fase Investigativa / Plenário: Homicídio - linha do tempo, Feminicídio: Linha do Tempo Cronológica das Ameaças, Homicídio Mercenário: Mapeamento do Pagamento pelo Crime, Linha do tempo — Caso Isabella Nardoni (+6 more)

### Community 15 - "Community 15"
Cohesion: 0.15
Nodes (12): Análise do Codebase - 2026-05-14 (pente-fino), Arquitetura de Geração, code:text (aulas-tribunal-do-juri/), Estado Visual Relevante, Estrutura Atual, Graphify (estado atual), Métricas de Código (linhas), Pente-fino Executado (2026-05-14) (+4 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (12): A extensão da mente do Promotor e o fim do caos documental, A revolução da escuta: extração inteligente de depoimentos, Engenharia de áudio como simulador cognitivo e estratégico, Extração seletiva e organização estratégica dos autos, NotebookLM - O Gabinete como Centro de Inteligência Analítica, O desafio da escala e os limites da IA em áudio e vídeo, O poder das fontes: internet versus autos, O protagonismo inegociável do Promotor de Justiça (+4 more)

### Community 17 - "Community 17"
Cohesion: 0.17
Nodes (10): code:bash (python3 scripts/build_all.py), code:bash (python3 scripts/gera_html.py conteudo/N.md html/N.html --tem), code:bash (python3 scripts/lock_menu_items.py --items 4 5 7), code:bash (sed -n '1,40p' loggerador.md), code:bash (python3 -m py_compile scripts/build_all.py scripts/gera_html), Comandos de Trabalho, Estado Atual, Pente-fino Rápido (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.17
Nodes (10): code:bash (python3 scripts/build_all.py), code:bash (python3 scripts/gera_html.py conteudo/N.md html/N.html --tem), code:bash (python3 scripts/lock_menu_items.py --items 4 5 7), code:bash (sed -n '1,40p' loggerador.md), code:bash (python3 -m py_compile scripts/build_all.py scripts/gera_html), Comandos de Trabalho, Estado Atual, Pente-fino Rápido (+2 more)

### Community 19 - "Community 19"
Cohesion: 0.22
Nodes (8): 🔒 Assistentes de IA, 🔒 Banco de Prompts, CIIA, 🔒 Dhiana, Guia NotebookLM, 🔒 Marias, Sites Abertos, Sites Fechados (acesso com login institucional)

### Community 20 - "Community 20"
Cohesion: 0.22
Nodes (8): Inteligência Artificial Aplicada ao Tribunal do Júri, [Tópico 1 | Abertura](1.html), [Tópico 2 | Engenharia de Prompts](2.html), [Tópico 3 | Agentes no Júri - Fluxo](3.html), [Tópico 4 | Elementos Gráficos no Júri](4.html), [Tópico 5 | NotebookLM no Júri](5.html), [Tópico 6 | Favoritos](6.html), [Tópico 7 | Guia NotebookLM](7.html)

### Community 21 - "Community 21"
Cohesion: 0.25
Nodes (7): 2026-05-14, Added, Changed, CHANGELOG, Docs, Fixed, Validation

### Community 22 - "Community 22"
Cohesion: 0.4
Nodes (4): Fluxo, html_gen, Módulos, Observações

## Knowledge Gaps
- **305 isolated node(s):** `allow`, `Extrai o primeiro H1 do arquivo markdown.     Retorna texto sem '#' e espaços ex`, `Constrói o título completo da página.     Padrão: "Inteligência Artificial Aplic`, `Retorna a raiz do projeto (onde está conteudo/ e html/)`, `Descobre todos os .md em conteudo/ e ordena logicamente` (+300 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `parse_markdown()` connect `Community 0` to `Community 3`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `parse_markdown()` (e.g. with `main()` and `is_page_comment_line()`) actually correct?**
  _`parse_markdown()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `main()` (e.g. with `parse_markdown()` and `assign_unique_icons()`) actually correct?**
  _`main()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `allow`, `Extrai o primeiro H1 do arquivo markdown.     Retorna texto sem '#' e espaços ex`, `Constrói o título completo da página.     Padrão: "Inteligência Artificial Aplic` to the rest of the system?**
  _305 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._