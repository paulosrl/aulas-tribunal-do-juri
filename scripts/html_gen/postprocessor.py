import re
import base64
from pathlib import Path

from html_gen.utils import esc, file_to_data_uri, normalize_data_uri, replace_between


def apply_global_page_rules(
    html_out: str,
    out_path: Path,
    md_path: Path,
    page_title: str,
    menu_group_title: str,
) -> str:
    """Apply global post-processing rules to HTML output.

    Handles:
    - Title injection from parameters
    - Logo embedding as base64 data URI
    - CSS injection for agent cards and styling
    - JavaScript injection for prompt copying
    - Mobile header configuration
    - Copilot icon embedding
    """
    # Regra 0: Título de página vindo de parâmetro de execução.
    safe_title = esc(page_title.strip() or "Defina o título da página")
    html_out = re.sub(r"<title>.*?</title>", f"<title>{safe_title}</title>", html_out, flags=re.IGNORECASE | re.DOTALL)

    safe_group_title = esc(menu_group_title.strip() or page_title.strip() or "Tópico")
    html_out = re.sub(
        r'(<span class="mobile-header-title">).*?(</span>)',
        rf"\1{safe_group_title}\2",
        html_out,
        flags=re.IGNORECASE | re.DOTALL,
    )
    # Remove rótulo legado "Curso" que aparece antes de "Início".
    html_out = re.sub(
        r'\s*<div class="nav-group-title">\s*Curso\s*</div>\s*',
        "\n",
        html_out,
        flags=re.IGNORECASE,
    )

    # Regra 1: Página inicial sempre aponta para index.html na mesma pasta.
    html_out = re.sub(r'href="\.\./index\.html"', 'href="index.html"', html_out, flags=re.IGNORECASE)

    # Regra 2: Logo preferencialmente na pasta de saída; fallback para pasta do markdown.
    logo_candidates = [
        out_path.parent / "logo.png",
        md_path.parent / "logo.png",
        Path("logo.png"),
    ]
    logo_file = next((p for p in logo_candidates if p.exists()), None)
    if logo_file is None:
        raise FileNotFoundError(
            f"Arquivo obrigatório não encontrado: logo.png\n"
            f"Procurei em: {', '.join(str(p) for p in logo_candidates)}"
        )
    logo_bytes = base64.b64encode(logo_file.read_bytes()).decode("ascii")
    logo_data_uri = f"data:image/png;base64,{logo_bytes}"

    html_out = re.sub(
        r'(<img[^>]*class="sidebar-logo"[^>]*src=")[^"]*(")',
        rf"\1{logo_data_uri}\2",
        html_out,
        flags=re.IGNORECASE,
    )

    agent_logo_html = f'<img src="{logo_data_uri}" class="agent-logo" alt="Logo" />'
    html_out = html_out.replace("<!-- AGENT_LOGO -->", agent_logo_html)

    # Ícone do botão Copilot: usa arquivo real para fidelidade visual.
    copilot_candidates = [
        out_path.parent / "copilot.png",
        md_path.parent / "copilot.png",
        Path("copilot.png"),
    ]
    copilot_icon_data_uri = None
    for candidate in copilot_candidates:
        if candidate.exists():
            copilot_icon_data_uri = file_to_data_uri(candidate)
            break

    # Regra 3: Injetar CSS para fichas de agente e aumentar tamanho do conteúdo em 20%
    agent_css = """<style>
.agent-card {
  background: linear-gradient(135deg, rgba(138,31,58,0.05), rgba(138,31,58,0.02));
  border: 1px solid rgba(138,31,58,0.2);
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transition: box-shadow 0.2s ease;
}
.agent-card:hover {
  box-shadow: 0 4px 20px rgba(138,31,58,0.15);
}
.agent-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.agent-num-badge {
  background: var(--accent);
  color: white;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.85rem;
  flex-shrink: 0;
}
.agent-card-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--accent);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.agent-card-title i {
  font-size: 1.1rem;
}
.agent-card-body {
  flex: 1;
}
.agent-desc {
  color: var(--text-main);
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0 0 0.5rem 0;
}
.agent-pillars {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}
.agent-pillars li {
  padding-left: 1rem;
  border-left: 3px solid var(--accent);
  font-size: 0.85rem;
  color: var(--text-main);
  margin: 0;
}
.agent-card-footer {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-top: 0.5rem;
}
.agent-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: var(--accent);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  text-decoration: none;
  transition: opacity 0.2s ease;
}
.agent-link-btn:hover {
  opacity: 0.85;
}
.agent-logo {
  width: 34px;
  height: 34px;
  object-fit: contain;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}
.agent-logo:hover {
  opacity: 1;
}
.caor-card h1,
.caor-card h2,
.caor-card h3 {
  font-size: 1.275em;
}
.caor-card p {
  font-size: 1.071em;
}
.caor-card li {
  font-size: 1.071em;
}
.nav-topic-subitems .nav-l {
  font-size: clamp(0.89rem, 1.035vw, 0.98rem) !important;
}
/* Clickable cards for index page */
.caor-card a {
  color: var(--accent);
  text-decoration: none;
  cursor: pointer;
  transition: opacity 0.2s ease;
}
.caor-card a:hover {
  opacity: 0.8;
}
.caor-card h2 a {
  display: inline;
  border-bottom: none;
}
.copilot-agent-cta-wrap {
  margin: 0.5rem 0 1rem 0;
}
.copilot-agent-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.62rem;
  background: linear-gradient(135deg, #8a1f3a 0%, #a72c55 40%, #c63d73 100%);
  color: #fff !important;
  border: 0;
  border-radius: 12px;
  padding: 0.7rem 1rem;
  font-weight: 700;
  font-size: 0.95rem;
  text-decoration: none !important;
  border-bottom: none !important;
  box-shadow: 0 6px 18px rgba(138, 31, 58, 0.28);
  transition: transform 0.15s ease, box-shadow 0.2s ease, opacity 0.2s ease;
}
.copilot-agent-cta:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 22px rgba(138, 31, 58, 0.34);
  opacity: 1;
}
.copilot-agent-cta .fa-external-link-alt {
  font-size: 0.82rem;
  opacity: 0.95;
}
.copilot-agent-cta-icon {
  width: 1.26rem;
  height: 1.26rem;
  background-image: url("__COPILOT_ICON_DATA_URI__");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 0.25rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  flex-shrink: 0;
}
.prompt-lab {
  margin: 0.9rem 0 1rem 0;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.14);
  background: linear-gradient(180deg, #121621 0%, #0d1119 100%);
  box-shadow: 0 8px 22px rgba(0,0,0,0.28);
  overflow: hidden;
}
.prompt-lab-title {
  color: #d7def0;
  font-weight: 700;
  font-size: 0.86rem;
  letter-spacing: 0.02em;
  padding: 0.55rem 0.8rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.03);
}
.prompt-lab-text {
  margin: 0;
  padding: 0.9rem 1rem;
  color: #f8fbff;
  background: transparent;
  font-size: 0.88rem;
  line-height: 1.55;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
.prompt-lab-actions {
  display: flex;
  gap: 0.55rem;
  padding: 0.75rem 0.9rem 0.9rem;
  border-top: 1px solid rgba(255,255,255,0.08);
}
.prompt-lab-btn {
  border: 1px solid #93c5fd;
  background: #dbeafe;
  color: #0f172a;
  border-radius: 8px;
  padding: 0.45rem 0.72rem;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none !important;
}
.prompt-lab-btn:hover {
  background: #bfdbfe;
  opacity: 1;
}
.prompt-lab-btn-link {
  display: inline-flex;
  align-items: center;
  border-color: #f59e0b;
  background: #fde68a;
  color: #111827;
}
.prompt-lab-btn-link:hover {
  background: #fcd34d;
}
</style>"""
    if copilot_icon_data_uri:
        agent_css = agent_css.replace("__COPILOT_ICON_DATA_URI__", copilot_icon_data_uri)
    else:
        agent_css = agent_css.replace("__COPILOT_ICON_DATA_URI__", "")
    html_out = html_out.replace("</head>", f"{agent_css}\n</head>", 1)
    prompt_js = """<script>
function copyPromptText(promptId, btnEl) {
  const node = document.getElementById(promptId);
  if (!node) return;
  const text = node.innerText || node.textContent || "";
  navigator.clipboard.writeText(text).then(() => {
    const prev = btnEl.textContent;
    btnEl.textContent = "Copiado";
    setTimeout(() => { btnEl.textContent = prev; }, 1200);
  });
}
</script>"""
    html_out = html_out.replace("</body>", f"{prompt_js}\n</body>", 1)

    return html_out
