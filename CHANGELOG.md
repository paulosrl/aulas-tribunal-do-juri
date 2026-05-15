# CHANGELOG

Formato adotado:
- `Added`: novas funcionalidades/arquivos
- `Changed`: mudanças de comportamento/estilo
- `Fixed`: correções de bugs/regressões
- `Docs`: documentação e memória operacional
- `Validation`: testes e verificações executadas

## 2026-05-14

### Added
- Criação de `CHANGELOG.md` para rastrear mudanças de forma contínua.
- Implementação do `loggerador.md` com registro por página gerada (página, data/hora e SHA-256).

### Changed
- Padronização de cores no tema escuro com destaque em `#fbd246`.
- Ajustes de títulos e menu para consistência entre páginas.
- Ajuste do item "Página Principal" no menu lateral (texto e ícone).
- Renumeração dos itens de menu a partir de 1 em todas as páginas.
- Atualização dos links internos após renumeração e remoções.
- Remoção de referências/links não mais usados no código gerado.
- Remoção de negrito forte dos subitens.
- Cores dos subitens por tema:
  - claro: `#8A1F3A`
  - escuro: branco
- Padronização de links para `#fbd246` com negrito leve no tema escuro.
- Remoção de tabelas na área de sumário, mantendo estrutura em parágrafos com numeração e links.
- Ajuste de estilo do sumário para negrito leve e padronização com `1.html`.
- Sincronização de regras entre `templates/topico.template.html` e `scripts/html_gen/postprocessor.py`.
- Atualização da documentação operacional para incluir o fluxo de log de geração automática.

### Fixed
- Correção da cor do ícone da "Página Principal" conforme paleta definida.
- Correção para impedir que cor de texto dos subitens sobrescrevesse a cor dos ícones.
- Correção de regras de CSS para evitar regressões entre tema claro e escuro.
- Revisão do comportamento de lock/unlock para evitar duplicação visual de cadeados no fluxo testado.

### Docs
- Atualização de:
  - `README.md`
  - `CODEBASE_ANALYSIS.md`
  - `scripts/html_gen/README.md`
  - `CODEX.md`
  - `CLAUDE.md`
  - `GEMINI.md`

### Validation
- Build completo executado em `index` e `1..7` com `python3 scripts/build_all.py`.
- Testes de `lock`/`unlock` com `dry-run` no `scripts/lock_menu_items.py`.
- Verificação de consistência por hash entre saídas HTML antes/depois de rebuild quando aplicável.
- Revisão de pente-fino executada com `py_compile` + build + lock/unlock dry-run, sem falhas bloqueantes.
