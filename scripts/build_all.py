#!/usr/bin/env python3
"""
Build automatizado: descobre todos os .md em conteudo/ e gera respectivos .html
"""

import subprocess
import sys
import argparse
import os
from pathlib import Path
from datetime import datetime


# Prefixo padrão para todos os títulos de página
TITLE_PREFIX = 'Inteligência Artificial Aplicada ao Tribunal do Júri'

# Mapeamento de tópicos principais (extraído do H1 de cada arquivo)
# Se o tópico for None, é extraído automaticamente do H1 do arquivo
PAGE_TOPICS = {
    'index.md': None,  # Landing page, não precisa --page-title
    '1.md': 'Abertura',
    '2.md': 'Engenharia de Prompts',
    '3.md': 'Agentes no Júri',
    '4.md': 'Elementos Gráficos no Júri',
    '5.md': 'NotebookLM no Júri',
    '6.md': 'Favoritos',
    '7.md': 'Notebooklm - Guia e Dicas',
}


def extract_h1_from_markdown(md_path: Path) -> str:
    """
    Extrai o primeiro H1 do arquivo markdown.
    Retorna texto sem '#' e espaços extras.
    """
    try:
        content = md_path.read_text(encoding='utf-8')
        for line in content.split('\n'):
            if line.startswith('# '):
                return line[2:].strip()
    except Exception:
        pass
    return 'Sem Título'


def build_page_title(md_name: str, md_path: Path) -> str | None:
    """
    Constrói o título completo da página.
    Padrão: "Inteligência Artificial Aplicada ao Tribunal do Júri — <Tópico>"
    """
    if md_name == 'index.md':
        return None  # Landing page não precisa

    # Usar tópico predefinido ou extrair do arquivo
    topic = PAGE_TOPICS.get(md_name)
    if topic is None:
        topic = extract_h1_from_markdown(md_path)

    # Montar título final
    return f'{TITLE_PREFIX} — {topic}'


def get_project_root() -> Path:
    """Retorna a raiz do projeto (onde está conteudo/ e html/)"""
    current = Path(__file__).parent.parent
    if (current / 'conteudo').exists() and (current / 'html').exists():
        return current
    raise RuntimeError('Não conseguiu encontrar conteudo/ e html/ a partir do script')


def discover_markdown_files(conteudo_dir: Path) -> list[Path]:
    """Descobre todos os .md em conteudo/ e ordena logicamente"""
    md_files = sorted(conteudo_dir.glob('*.md'))

    # Ordena: index.md primeiro, depois tópicos numéricos (1, 2, 10...), depois extras.
    def sort_key(p: Path) -> tuple:
        name = p.name
        stem = p.stem
        if name == 'index.md':
            return (0, '')
        elif stem.isdigit():
            return (1, int(stem))
        else:
            return (2, name)

    return sorted(md_files, key=sort_key)


def build_html(script_dir: Path, project_root: Path, md_file: Path, timeout_seconds: int = 30) -> bool:
    """
    Executa gera_html.py para um arquivo markdown
    Retorna True se bem-sucedido, False caso contrário
    """
    md_name = md_file.name
    html_name = md_file.stem + '.html'
    output_path = project_root / 'html' / html_name

    # Construir comando
    cmd = [
        sys.executable,
        str(script_dir / 'gera_html.py'),
        str(md_file),
        str(output_path),
    ]

    # Adicionar argumentos específicos se não for index.md
    if md_name != 'index.md':
        cmd.extend([
            '--template', str(project_root / 'templates' / 'topico.template.html'),
            '--section-mode', 'semantic',
        ])

        page_title = build_page_title(md_name, md_file)
        if page_title:
            cmd.extend(['--page-title', page_title])

    try:
        env = os.environ.copy()
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_seconds, env=env)
        if result.returncode != 0:
            print(f'  ❌ ERRO: {result.stderr or result.stdout}')
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f'  ❌ TIMEOUT após {timeout_seconds} segundos')
        return False
    except Exception as e:
        print(f'  ❌ EXCEÇÃO: {e}')
        return False


def print_header():
    """Imprime cabeçalho visual"""
    print()
    print('╔' + '═' * 70 + '╗')
    print('║' + ' ' * 20 + '🏗️  BUILD AUTOMÁTICO DO SITE' + ' ' * 22 + '║')
    print('║' + ' ' * 22 + f'Iniciado em {datetime.now().strftime("%H:%M:%S")}' + ' ' * 24 + '║')
    print('╚' + '═' * 70 + '╝')
    print()


def print_summary(results: dict):
    """Imprime sumário final"""
    total = len(results)
    successful = sum(1 for v in results.values() if v)
    failed = total - successful

    print()
    print('╔' + '═' * 70 + '╗')
    print('║' + ' ' * 25 + '📊 SUMÁRIO FINAL' + ' ' * 29 + '║')
    print('╠' + '═' * 70 + '╣')
    print(f'║  Total de arquivos processados: {total:<40} ║')
    print(f'║  ✅ Sucesso:                    {successful:<40} ║')
    if failed > 0:
        print(f'║  ❌ Falhas:                     {failed:<40} ║')
    print('╠' + '═' * 70 + '╣')

    # Listar resultados
    for md_file, success in sorted(results.items()):
        status = '✅' if success else '❌'
        html_file = md_file.replace('.md', '.html')
        print(f'║  {status}  {html_file:<60} ║')

    print('╚' + '═' * 70 + '╝')
    print()

    if failed == 0:
        print('🎉 Todos os arquivos foram gerados com sucesso!')
        return 0
    else:
        print(f'⚠️  {failed} arquivo(s) falharam. Verifique os erros acima.')
        return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Build automatizado: descobre todos os .md em conteudo/ e gera respectivos .html.'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Timeout em segundos por arquivo durante a geração (padrão: 30).',
    )
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        project_root = get_project_root()
        script_dir = project_root / 'scripts'
        conteudo_dir = project_root / 'conteudo'

        print_header()

        # Descobrir arquivos
        md_files = discover_markdown_files(conteudo_dir)
        if not md_files:
            print('❌ Nenhum arquivo .md encontrado em conteudo/')
            return 1

        print(f'📂 Encontrados {len(md_files)} arquivo(s) markdown:\n')
        for i, md_file in enumerate(md_files, 1):
            print(f'   {i}. {md_file.name}')
        print()

        # Processar cada arquivo
        results = {}
        print('🔨 Processando...\n')

        for i, md_file in enumerate(md_files, 1):
            md_name = md_file.name
            html_name = md_file.stem + '.html'

            print(f'[{i}/{len(md_files)}] {md_name:<20} → {html_name:<20}', end=' ', flush=True)

            success = build_html(script_dir, project_root, md_file, timeout_seconds=args.timeout)
            results[md_name] = success

            if success:
                print('✅')
            else:
                print('❌')

        # Sumário
        exit_code = print_summary(results)
        return exit_code

    except KeyboardInterrupt:
        print('\n\n⚠️  Build interrompido pelo usuário')
        return 130
    except Exception as e:
        print(f'\n❌ Erro fatal: {e}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
