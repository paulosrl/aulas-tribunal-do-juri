# Aulas: IA Aplicada ao Tribunal do Júri

Repositório do material em HTML da trilha **Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário**.

## Objetivo

Este projeto converte conteúdos em Markdown (`conteudo/*.md`) para páginas HTML com layout padronizado, menu lateral consistente, tema claro/escuro e navegação entre tópicos.

## Acesso ao Site (GitHub Pages)

- URL pública: **https://paulosrl.github.io/aulas-tribunal-do-juri/**

## Estrutura do Projeto

- `conteudo/`
: fontes em Markdown (tópicos 1 a 5 e materiais base)
- `templates/topico.template.html`
: template visual oficial das páginas de tópico
- `scripts/gera_html.py`
: gerador principal Markdown -> HTML
- `html/`
: saída final das páginas prontas para publicação
  - `index.html` (landing page)
  - `1.html` a `5.html` (tópicos)
  - `logo.png` (logo usada no layout)

## Páginas Geradas

- `html/index.html`: landing page com acesso aos tópicos
- `html/1.html`: Abertura
- `html/2.html`: Engenharia de Prompts
- `html/3.html`: Agentes no Juri
- `html/4.html`: Elementos Gráficos no Juri
- `html/5.html`: NotebookLM no Júri

## Como Gerar as Páginas

Execute no diretório raiz do projeto:

```bash
python3 scripts/gera_html.py conteudo/1.md html/1.html --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário"
python3 scripts/gera_html.py conteudo/2.md html/2.html --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário"
python3 scripts/gera_html.py conteudo/3.md html/3.html --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário"
python3 scripts/gera_html.py conteudo/4.md html/4.html --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário"
python3 scripts/gera_html.py conteudo/5.md html/5.html --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário"
```

## Regras Implementadas no Gerador

- Remove referências do tipo SharePoint/Copilot no HTML final.
- Mantém menu fixo de tópicos com 6 opções:
  1. Abertura
  2. Engenharia de Prompts
  3. Agentes no Juri
  4. Elementos Gráficos no Juri
  5. NotebookLM no Júri
  6. Favoritos
- Evita duplicação do título principal no menu interno da página.
- Mantém título principal da página no conteúdo (`h1`).
- Remove coluna "Páginas de origem" do sumário quando existir em tabelas.
- Usa badges numéricos no sumário com padrão visual uniforme.
- Ajusta tabelas para evitar rolagem horizontal no uso padrão do template.

## Padrões de Design Aplicados

- Tema padrão inicial: **claro**.
- Paleta principal com destaque em `#8A1F3A`.
- Botão de alternância de tema (`🌓 TEMA`) com persistência via `localStorage`.
- Logo e endereço `ciia.mppa.mp.br` em destaque no menu.
- Bloco de autores com medalhas e nota de IA:
  - `MPPA — CIIA`
  - `14 e 15 de maio de 2025`
  - `Material produzido com apoio de ferramentas de IA`

## Landing Page (`html/index.html`)

A landing foi construída com a mesma linguagem visual dos tópicos e contém:

- Logo central em destaque
- Link para `ciia.mppa.mp.br`
- Navegação por cards para os tópicos 1 a 6
- Ícones profissionais por tópico
- Compatibilidade com modo claro/escuro

## Publicação no GitHub

### 1) Commit e push

```bash
git add .
git commit -m "Atualiza landing, template e páginas do curso"
git push origin main
```

### 2) GitHub Pages (sugestão)

Se desejar publicar diretamente o conteúdo de `html/`, configure o GitHub Pages para servir a pasta correta (via workflow ou configuração do repositório).

## Observações

- O projeto já está pronto para navegação local abrindo `html/index.html`.
- Para publicação web, mantenha sempre `index.html`, `logo.png` e `1.html` a `5.html` atualizados em `html/`.
