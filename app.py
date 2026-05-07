import os
import re
import json
from pathlib import Path

import streamlit as st
import yaml

# ── Paths ─────────────────────────────────────────────────────────────────────

CONFIG_PATH = Path(__file__).parent / "config.yaml"
PREFS_PATH  = Path(__file__).parent / "prefs.json"

# ── Config + prefs ────────────────────────────────────────────────────────────

def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        raw = f.read()
    raw = re.sub(r"\$\{(\w+)\}", lambda m: os.environ.get(m.group(1), ""), raw)
    return yaml.safe_load(raw)


def load_prefs(config: dict) -> dict:
    """Merge saved prefs.json over config.yaml defaults. prefs.json wins."""
    app_cfg = config.get("app", {})
    ui_cfg  = config.get("ui", {})
    defaults = {
        "title":             app_cfg.get("title",    "CDP Launchpad"),
        "subtitle":          app_cfg.get("subtitle", ""),
        "theme":             ui_cfg.get("theme",             "light"),
        "font_size":         ui_cfg.get("font_size",         "medium"),
        "font_family":       ui_cfg.get("font_family",       "system"),
        "accent_color":      ui_cfg.get("accent_color",      "#FF6D2A"),
        "compact":           ui_cfg.get("compact",           False),
        "show_descriptions": ui_cfg.get("show_descriptions", True),
    }
    if PREFS_PATH.exists():
        try:
            saved = json.loads(PREFS_PATH.read_text())
            defaults.update({k: v for k, v in saved.items() if k in defaults})
        except Exception:
            pass
    return defaults


def save_prefs(prefs: dict):
    PREFS_PATH.write_text(json.dumps(prefs, indent=2))


def reset_prefs():
    PREFS_PATH.unlink(missing_ok=True)

# ── Theme tokens ──────────────────────────────────────────────────────────────

_FONT_SIZES = {
    "small":  ("0.78rem", "0.67rem", "0.88rem"),   # name, desc, search
    "medium": ("0.85rem", "0.73rem", "0.92rem"),
    "large":  ("0.96rem", "0.82rem", "1.02rem"),
}

_FONT_STACKS = {
    "system": '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
    "mono":   '"JetBrains Mono", "SF Mono", "Fira Code", "Cascadia Code", monospace',
    "serif":  'Georgia, "Times New Roman", Times, serif',
}

def build_tokens(p: dict) -> dict:
    accent  = p["accent_color"]
    fs      = _FONT_SIZES.get(p["font_size"], _FONT_SIZES["medium"])
    ff      = _FONT_STACKS.get(p["font_family"], _FONT_STACKS["system"])
    compact = p["compact"]

    if p["theme"] == "dark":
        t = dict(
            bg="#0D0E1C", card_bg="#1A1D2E", card_border="#2E3352",
            text_primary="#E8EAF6", text_secondary="#9AA3C2", text_muted="#5C6490",
            input_bg="#1A1D2E", input_border="#2E3352", input_text="#E8EAF6",
            divider="#2E3352",
            tab_active=accent, tab_inactive="#5C6490", tab_border="#2E3352",
            icon_bg=f"{accent}22", icon_border=f"{accent}44",
            hover_shadow=f"{accent}25",
        )
    else:
        t = dict(
            bg="#F4F6F9", card_bg="#FFFFFF", card_border="#E2E8F0",
            text_primary="#1E293B", text_secondary="#64748B", text_muted="#94A3B8",
            input_bg="#FFFFFF", input_border="#CBD5E1", input_text="#1E293B",
            divider="#E2E8F0",
            tab_active=accent, tab_inactive="#94A3B8", tab_border="#E2E8F0",
            icon_bg="#FFF3EC", icon_border="#FFD5BF",
            hover_shadow=f"{accent}22",
        )

    t.update(
        accent=accent,
        name_sz=fs[0], desc_sz=fs[1], search_sz=fs[2],
        font_family=ff,
        card_pad="9px 12px" if compact else "12px 14px",
        card_gap="7px"      if compact else "10px",
    )
    return t


def inject_css(t: dict, show_desc: bool):
    desc_display = "block" if show_desc else "none"
    st.markdown(f"""
    <style>
    /* ── Base ── */
    html, body, [class*="css"] {{ font-family: {t['font_family']} !important; }}
    .stApp {{ background: {t['bg']} !important; }}
    .block-container {{ padding-top: 1.4rem !important; padding-bottom: 2rem !important; max-width: 1600px; }}

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, .stDeployButton,
    [data-testid="stDeployButton"],
    [data-testid="stToolbar"],
    [data-testid="stHeader"] {{ display: none !important; }}

    /* ── Typography ── */
    .stApp p, .stApp span, .stApp div, .stApp label {{ color: {t['text_secondary']}; font-family: {t['font_family']} !important; }}
    .stMarkdown p {{ color: {t['text_secondary']} !important; }}
    .stCaption p  {{ color: {t['text_muted']} !important; font-size: 0.78rem !important; }}
    h1, h2, h3, h4 {{ color: {t['text_primary']} !important; font-family: {t['font_family']} !important; }}

    /* ── Divider ── */
    hr {{ border-color: {t['divider']} !important; margin: 0.5rem 0 !important; }}

    /* ── Search input ── */
    .stTextInput > div > div > input {{
        background: {t['input_bg']} !important;
        border: 1px solid {t['input_border']} !important;
        border-radius: 8px !important;
        color: {t['input_text']} !important;
        font-size: {t['search_sz']} !important;
        font-family: {t['font_family']} !important;
        padding: 0.5rem 0.9rem !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {t['accent']} !important;
        box-shadow: 0 0 0 2px {t['accent']}30 !important;
    }}
    .stTextInput > div > div > input::placeholder {{ color: {t['text_muted']} !important; opacity: 1; }}

    /* ── Tabs ── */
    [data-testid="stTabs"] [role="tablist"] {{ border-bottom: 1px solid {t['tab_border']} !important; gap: 4px; }}
    [data-testid="stTabs"] button[role="tab"] {{
        color: {t['tab_inactive']} !important;
        font-size: 0.85rem !important; font-weight: 500 !important;
        border-bottom: 2px solid transparent !important;
        font-family: {t['font_family']} !important;
        background: transparent !important;
    }}
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
        color: {t['tab_active']} !important;
        border-bottom-color: {t['tab_active']} !important;
        font-weight: 600 !important;
    }}

    /* ── Settings gear button ── */
    .stApp .stButton > button {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: {t['text_muted']} !important;
        font-size: 1.1rem !important;
        padding: 4px 8px !important;
        border-radius: 7px !important;
        min-height: unset !important;
        height: auto !important;
        width: 100% !important;
        line-height: 1.5 !important;
    }}
    .stApp .stButton > button:hover {{
        background: {t['icon_bg']} !important;
        color: {t['text_primary']} !important;
    }}
    /* Restore normal button styling inside the settings dialog */
    [data-testid="stDialog"] .stButton > button {{
        font-size: 0.88rem !important;
        padding: 8px 16px !important;
        min-height: 2.4rem !important;
        height: auto !important;
        border-radius: 8px !important;
        width: 100% !important;
    }}
    [data-testid="stDialog"] .stButton > button[kind="secondary"] {{
        background: {t['card_bg']} !important;
        border: 1px solid {t['card_border']} !important;
        color: {t['text_primary']} !important;
    }}
    [data-testid="stDialog"] .stButton > button[kind="primary"] {{
        background: {t['accent']} !important;
        border: none !important;
        color: #fff !important;
    }}
    /* Align button column with input — strip top padding Streamlit adds */
    .stTextInput {{ padding-top: 0 !important; }}
    .stButton    {{ padding-top: 0 !important; margin-top: 0 !important; }}

    /* ── Environment header ── */
    .env-header {{
        display: flex; align-items: center; gap: 8px;
        padding: 9px 13px; border-radius: 8px;
        margin-bottom: 12px; border: 1px solid;
    }}
    .env-dot   {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
    .env-badge {{ padding: 2px 8px; border-radius: 10px; font-size: 0.67rem; font-weight: 700; color: #FFF; text-transform: uppercase; letter-spacing: 0.5px; }}
    .env-title {{ font-size: 0.92rem; font-weight: 700; color: {t['text_primary']}; font-family: {t['font_family']}; }}
    .env-count {{ font-size: 0.70rem; color: {t['text_muted']}; margin-left: auto; }}

    /* ── Service card ── */
    .svc-card {{
        background: {t['card_bg']}; border: 1px solid {t['card_border']};
        border-radius: 10px; padding: {t['card_pad']}; margin-bottom: {t['card_gap']};
        display: flex; align-items: flex-start; gap: 11px;
        transition: box-shadow 0.15s, border-color 0.15s, transform 0.12s;
    }}
    .svc-card:hover {{
        box-shadow: 0 4px 14px {t['hover_shadow']};
        border-color: {t['accent']}; transform: translateY(-1px);
    }}
    .svc-card.unconfigured {{ opacity: 0.45; }}

    .svc-icon {{
        width: 34px; height: 34px; margin-top: 2px;
        background: {t['icon_bg']}; border: 1px solid {t['icon_border']};
        border-radius: 7px; display: flex; align-items: center;
        justify-content: center; font-size: 16px; flex-shrink: 0;
    }}
    .svc-info  {{ flex: 1; min-width: 0; }}
    .svc-name  {{ font-size: {t['name_sz']}; font-weight: 600; color: {t['text_primary']}; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-family: {t['font_family']}; }}
    .svc-desc  {{
        font-size: {t['desc_sz']}; color: {t['text_secondary']}; margin: 2px 0 0;
        font-family: {t['font_family']};
        {"display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; white-space: normal;" if show_desc else "display: none;"}
    }}

    .svc-link {{
        display: inline-block; padding: 5px 13px;
        background: {t['accent']}; color: #FFF !important;
        border-radius: 6px; font-size: 0.73rem; font-weight: 600;
        text-decoration: none !important; flex-shrink: 0;
        transition: opacity 0.12s; white-space: nowrap;
        font-family: {t['font_family']}; margin-top: 2px;
    }}
    .svc-link:hover {{ opacity: 0.85; }}

    .tag-nc {{ font-size: 0.62rem; font-weight: 700; text-transform: uppercase;
               letter-spacing: 0.4px; border-radius: 4px; padding: 2px 6px;
               background: {t['card_border']}; color: {t['text_muted']}; flex-shrink: 0; }}
    .empty-state {{ color: {t['text_muted']}; font-size: 0.82rem; padding: 10px 0; }}

    /* ── Dialog tweaks ── */
    [data-testid="stDialog"] > div > div {{
        background: {t['card_bg']} !important;
        border: 1px solid {t['card_border']} !important;
        border-radius: 14px !important;
    }}
    [data-testid="stDialog"] label,
    [data-testid="stDialog"] p {{ color: {t['text_secondary']} !important; }}
    [data-testid="stDialog"] h1,
    [data-testid="stDialog"] h2,
    [data-testid="stDialog"] h3 {{ color: {t['text_primary']} !important; }}
    </style>
    """, unsafe_allow_html=True)


# ── Settings dialog ───────────────────────────────────────────────────────────

@st.dialog("Settings", width="large")
def settings_dialog(prefs: dict):
    # ── Branding ──────────────────────────────────────────────────────────────
    st.markdown("**Branding**")
    new_title    = st.text_input("App title",  value=prefs["title"],    key="d_title")
    new_subtitle = st.text_input("Subtitle",   value=prefs["subtitle"], key="d_subtitle",
                                 help="Shown below the title. Leave blank to hide.")

    st.divider()

    # ── Theme & colors ────────────────────────────────────────────────────────
    st.markdown("**Theme & Colors**")
    ca, cb = st.columns(2)
    with ca:
        new_theme = st.radio(
            "Mode", ["light", "dark"],
            index=0 if prefs["theme"] == "light" else 1,
            horizontal=True, key="d_theme",
        )
    with cb:
        new_accent = st.color_picker("Accent color", value=prefs["accent_color"], key="d_accent")

    st.divider()

    # ── Typography ────────────────────────────────────────────────────────────
    st.markdown("**Typography**")
    ta, tb = st.columns(2)
    with ta:
        new_font_size = st.select_slider(
            "Font size", options=["small", "medium", "large"],
            value=prefs["font_size"], key="d_font_size",
        )
    with tb:
        new_font_family = st.radio(
            "Font style",
            options=["system", "mono", "serif"],
            format_func={"system": "Sans-serif (default)", "mono": "Monospace", "serif": "Serif"}.get,
            index=["system", "mono", "serif"].index(prefs.get("font_family", "system")),
            key="d_font_family",
        )

    st.divider()

    # ── Layout ────────────────────────────────────────────────────────────────
    st.markdown("**Layout**")
    la, lb = st.columns(2)
    with la:
        new_compact = st.toggle("Compact cards", value=prefs["compact"], key="d_compact")
    with lb:
        new_show_desc = st.toggle("Show service descriptions", value=prefs["show_descriptions"], key="d_show_desc")

    st.divider()

    # ── Actions ───────────────────────────────────────────────────────────────
    ba, bb = st.columns(2)
    with ba:
        if st.button("Save", type="primary", use_container_width=True):
            save_prefs({
                "title":             new_title,
                "subtitle":          new_subtitle,
                "theme":             new_theme,
                "accent_color":      new_accent,
                "font_size":         new_font_size,
                "font_family":       new_font_family,
                "compact":           new_compact,
                "show_descriptions": new_show_desc,
            })
            st.rerun()
    with bb:
        if st.button("Reset to defaults", use_container_width=True):
            reset_prefs()
            st.rerun()


# ── Render helpers ────────────────────────────────────────────────────────────

def render_env_header(env: dict, count: int):
    color = env.get("color", "#6B7280")
    name  = env.get("name",  env.get("id", "Unknown"))
    badge = env.get("badge", name[:3].upper())
    st.markdown(f"""
    <div class="env-header" style="background:{color}18;border-color:{color}44;">
      <span class="env-dot" style="background:{color};box-shadow:0 0 6px {color}88;"></span>
      <span class="env-badge" style="background:{color};">{badge}</span>
      <span class="env-title">{name}</span>
      <span class="env-count">{count} service{"s" if count != 1 else ""}</span>
    </div>
    """, unsafe_allow_html=True)


def render_service_card(svc: dict):
    url  = svc.get("url", "").strip()
    icon = svc.get("icon", "🔧")
    name = svc.get("name", "Unknown")
    desc = svc.get("description", "")

    if url:
        action   = f'<a class="svc-link" href="{url}" target="_blank" rel="noopener">Open ↗</a>'
        card_cls = "svc-card"
    else:
        action   = '<span class="tag-nc">Not configured</span>'
        card_cls = "svc-card unconfigured"

    st.markdown(f"""
    <div class="{card_cls}">
      <div class="svc-icon">{icon}</div>
      <div class="svc-info">
        <p class="svc-name">{name}</p>
        <p class="svc-desc">{desc}</p>
      </div>
      {action}
    </div>
    """, unsafe_allow_html=True)


def render_env_block(env: dict, services: list, search: str):
    q = search.lower()
    visible = [
        s for s in services
        if not q or q in s.get("name", "").lower() or q in s.get("description", "").lower()
    ]
    render_env_header(env, len(visible))
    if visible:
        for svc in visible:
            render_service_card(svc)
    else:
        st.markdown('<p class="empty-state">No matching services.</p>', unsafe_allow_html=True)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="CDP Launchpad",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Load config + persisted prefs
    try:
        config = load_config()
    except FileNotFoundError:
        st.error(f"Config file not found: `{CONFIG_PATH}`")
        st.stop()
    except yaml.YAMLError as exc:
        st.error(f"Invalid YAML in config.yaml: {exc}")
        st.stop()

    prefs = load_prefs(config)
    envs  = config.get("environments", [])

    tokens    = build_tokens(prefs)
    show_desc = prefs["show_descriptions"]
    inject_css(tokens, show_desc)

    # ── Header row ────────────────────────────────────────────────────────────
    h_title, h_right = st.columns([3, 1.6])

    with h_title:
        st.markdown(f"## 🚀 {prefs['title']}")
        if prefs.get("subtitle"):
            st.caption(prefs["subtitle"])

    with h_right:
        sc, bc = st.columns([9, 1])
        with sc:
            search = st.text_input(
                "Search", placeholder="Search services…",
                label_visibility="collapsed", key="search",
            )
        with bc:
            if st.button("⚙️", help="Open settings", use_container_width=True):
                settings_dialog(prefs)

    st.divider()

    if not envs:
        st.warning("No environments defined in `config.yaml`.")
        st.stop()

    # Resolve services (filter disabled)
    env_services: dict[str, list] = {
        env["id"]: [s for s in env.get("services", []) if s.get("enabled", True)]
        for env in envs
    }

    # Layout: columns ≤3, tabs 4+
    n = len(envs)
    q = search.strip()
    if n <= 3:
        cols = st.columns(n, gap="large")
        for col, env in zip(cols, envs):
            with col:
                render_env_block(env, env_services[env["id"]], q)
    else:
        tabs = st.tabs([e.get("name", e["id"]) for e in envs])
        for tab, env in zip(tabs, envs):
            with tab:
                render_env_block(env, env_services[env["id"]], q)

    st.divider()
    st.caption("CDP Launchpad · Edit config.yaml to manage environments and service URLs")


if __name__ == "__main__":
    main()
