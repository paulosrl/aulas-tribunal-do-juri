# Análise do Codebase - 2026-05-13

## Resumo Executivo

**Estado**: ✅ Clean repository  
**Última análise**: 2026-05-13  
**Arquivos analisados**: 29 arquivos principais

### Estrutura

```
aulas-tribunal-do-juri/
├── scripts/           (2.039 linhas Python)
├── conteudo/          (1.782 linhas Markdown + metadados)
├── templates/         (2 templates HTML com Font Awesome 6)
├── html/              (Saídas geradas)
└── graphify-out/      (Análise arquitetural)
```

## Métricas Principais

| Métrica | Valor |
|---------|-------|
| **Tamanho código** | 1.854 linhas (gera_html.py) |
| **Tamanho conteúdo** | 1.782 linhas (8 arquivos .md) |
| **Proporção** | 1.14:1 (code:content) |
| **Nós (graphify)** | 102 |
| **Arestas** | 266 |
| **Comunidades** | 11 |
| **God nodes** | 2 (>20 edges) |
| **Coesão alta** | Comunidades 9-10 (0.53-0.67) |

## Componentes Críticos

### 1. Gerador Principal (`gera_html.py`)
- **Responsabilidade**: Markdown → HTML via templates
- **Linhas**: 1.854
- **God node**: `build_topico.py` (30 arestas)
- **Funções-chave**:
  - `parse_markdown()` - 23+ arestas (crítica)
  - `apply_global_page_rules()`
  - `assign_unique_icons()`
  - `generate_index_page()`

### 2. Conteúdo Educacional
- **5 tópicos**: 1.148 linhas (~5.6k palavras)
- **Especiais**: Favoritos (42 linhas), NotebookLM (659 linhas)
- **Landing**: index.md com 7 tópicos no menu

### 3. Sistema Visual
- **Font Awesome 6**: Embutido nos templates
- **Ícones**: Renderizados via CSS ::before + cor li-topic-icon
- **Copilot button**: Data URI embutido (copilot.png)

## Padrões Detectados

### Pontos Fortes
✅ **Segurança**: Comunidade 9 com alta coesão (0.53) - escaping centralizado  
✅ **Renderização**: Comunidade 10 com alta coesão (0.67) - menu/ícones bem integrados  
✅ **Qualidade**: 100% de extração graphify (sem ambiguidades)  
✅ **Simplicidade**: Maioria das funções < 50 linhas  

### Pontos de Atenção
⚠️ **gera_html.py**: 1.854 linhas (ideal: <800)  
⚠️ **Graphify desatualizado**: Último em c536700, HEAD é 618e953  
⚠️ **Hub central**: `esc()` conecta 5+ comunidades (refatorar com cuidado)  

## Histórico Recent

```
618e953  refactor: update document titles and realign icon categories
3cefff5  fix: update session metadata and session dates
c536700  refactor: update course metadata, reorganize curriculum
1b308b9  feat: add new site assets and update project infrastructure
eec9c6d  chore: relocate copilot.png to the html directory
```

**Padrão**: Refactors focados em metadados, nenhuma alteração destrutiva.

## Recomendações

1. **Manter graphify atualizado**: `graphify update .` após mudanças Python
2. **Atenção com refatorações**: Comunidades 9-10 têm alta coesão (testes necessários)
3. **Validação de conteúdo**: Função `validate_content_preservation()` é crítica
4. **Documentação**: Manter CLAUDE.md, AGENTS.md, CODEX.md sincronizados

## Próximas Ações

- [ ] Atualizar graphify: `graphify update .`
- [ ] Review de gera_html.py para possível split
- [ ] Verificar todos os 11 tópicos do menu lateral
- [ ] Testar rendering de ícones FA6 em todos os navegadores
