import subprocess
import sys
import os

# Step 1: Install dependencies
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

# Step 2: Application
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cloudera Platform Portal",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Branding / colour tokens ──────────────────────────────────────────────────
CLOUDERA_ORANGE   = "#FF6D2A"
CLOUDERA_DARK     = "#0D0E1C"
CLOUDERA_CHARCOAL = "#1A1D2E"
CLOUDERA_PANEL    = "#21253A"
CLOUDERA_BORDER   = "#2E3352"
CLOUDERA_MUTED    = "#8891B8"
CLOUDERA_TEXT     = "#E8EAF6"
CLOUDERA_WHITE    = "#FFFFFF"
PROD_ACCENT       = "#00C896"   # green
DEV_ACCENT        = "#3B9EFF"   # blue
DR_ACCENT         = "#F7B731"   # amber

# ── Service definitions ───────────────────────────────────────────────────────
# Each service: (display_name, icon_svg_path_or_emoji, description, {env: url})
SERVICES = [
    {
        "name": "Management Console",
        "icon": "🖥️",
        "description": "Central control plane for your CDP environment",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>""",
        "urls": {
            "prod": "https://console.prod.cloudera.example.com",
            "dev":  "https://console.dev.cloudera.example.com",
            "dr":   "https://console.dr.cloudera.example.com",
        },
    },
    {
        "name": "Data Catalog",
        "icon": "🗂️",
        "description": "Unified metadata management & data discovery",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>""",
        "urls": {
            "prod": "https://catalog.prod.cloudera.example.com",
            "dev":  "https://catalog.dev.cloudera.example.com",
            "dr":   "https://catalog.dr.cloudera.example.com",
        },
    },
    {
        "name": "Query Editor",
        "icon": "🔍",
        "description": "Interactive SQL editor powered by Apache Hue",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>""",
        "urls": {
            "prod": "https://hue.prod.cloudera.example.com",
            "dev":  "https://hue.dev.cloudera.example.com",
            "dr":   "https://hue.dr.cloudera.example.com",
        },
    },
    {
        "name": "Data Flow",
        "icon": "🌊",
        "description": "Apache NiFi based data ingestion & routing",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>""",
        "urls": {
            "prod": "https://dataflow.prod.cloudera.example.com",
            "dev":  "https://dataflow.dev.cloudera.example.com",
            "dr":   "https://dataflow.dr.cloudera.example.com",
        },
    },
    {
        "name": "Resource Monitoring",
        "icon": "📊",
        "description": "Cluster health, metrics & resource utilisation",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>""",
        "urls": {
            "prod": "https://monitoring.prod.cloudera.example.com",
            "dev":  "https://monitoring.dev.cloudera.example.com",
            "dr":   "https://monitoring.dr.cloudera.example.com",
        },
    },
    {
        "name": "Data Warehouse",
        "icon": "🏛️",
        "description": "Cloud-native analytical data warehouse (CDW)",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>""",
        "urls": {
            "prod": "https://cdw.prod.cloudera.example.com",
            "dev":  "https://cdw.dev.cloudera.example.com",
            "dr":   "https://cdw.dr.cloudera.example.com",
        },
    },
    {
        "name": "Machine Learning",
        "icon": "🤖",
        "description": "Cloudera AI Workbench for ML experiments",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>""",
        "urls": {
            "prod": "https://cml.prod.cloudera.example.com",
            "dev":  "https://cml.dev.cloudera.example.com",
            "dr":   "https://cml.dr.cloudera.example.com",
        },
    },
    {
        "name": "Data Engineering",
        "icon": "⚙️",
        "description": "Apache Spark pipelines & job orchestration",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/></svg>""",
        "urls": {
            "prod": "https://cde.prod.cloudera.example.com",
            "dev":  "https://cde.dev.cloudera.example.com",
            "dr":   "https://cde.dr.cloudera.example.com",
        },
    },
    {
        "name": "Streaming",
        "icon": "⚡",
        "description": "Apache Kafka real-time event streaming",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>""",
        "urls": {
            "prod": "https://kafka.prod.cloudera.example.com",
            "dev":  "https://kafka.dev.cloudera.example.com",
            "dr":   "https://kafka.dr.cloudera.example.com",
        },
    },
    {
        "name": "Data Visualisation",
        "icon": "📈",
        "description": "Interactive BI dashboards & visual analytics",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>""",
        "urls": {
            "prod": "https://dataviz.prod.cloudera.example.com",
            "dev":  "https://dataviz.dev.cloudera.example.com",
            "dr":   "https://dataviz.dr.cloudera.example.com",
        },
    },
    {
        "name": "Ranger Security",
        "icon": "🛡️",
        "description": "Centralised access control & audit policies",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>""",
        "urls": {
            "prod": "https://ranger.prod.cloudera.example.com",
            "dev":  "https://ranger.dev.cloudera.example.com",
            "dr":   "https://ranger.dr.cloudera.example.com",
        },
    },
    {
        "name": "Atlas Lineage",
        "icon": "🔗",
        "description": "Data lineage, classification & governance",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>""",
        "urls": {
            "prod": "https://atlas.prod.cloudera.example.com",
            "dev":  "https://atlas.dev.cloudera.example.com",
            "dr":   "https://atlas.dr.cloudera.example.com",
        },
    },
]

# ── Global CSS injection ──────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        /* ── Reset & base ─────────────────────────────────────────── */
        html, body, [class*="css"] {{
            font-family: 'Sora', sans-serif;
            background-color: {CLOUDERA_DARK};
            color: {CLOUDERA_TEXT};
        }}

        .stApp {{
            background: radial-gradient(ellipse 120% 80% at 50% -10%,
                rgba(255,109,42,0.12) 0%,
                {CLOUDERA_DARK} 60%);
            min-height: 100vh;
        }}

        /* Hide Streamlit chrome */
        #MainMenu, footer, header {{ visibility: hidden; }}
        .block-container {{
            padding: 2rem 2.5rem 3rem;
            max-width: 1600px;
        }}

        /* ── Top header bar ──────────────────────────────────────── */
        .cdp-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.2rem 1.6rem;
            background: {CLOUDERA_CHARCOAL};
            border: 1px solid {CLOUDERA_BORDER};
            border-radius: 14px;
            margin-bottom: 1.8rem;
            box-shadow: 0 4px 32px rgba(0,0,0,0.4);
        }}
        .cdp-logo-wrap {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}
        .cdp-logo-icon {{
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, {CLOUDERA_ORANGE}, #FF9A62);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 0 20px rgba(255,109,42,0.45);
        }}
        .cdp-logo-text {{ line-height: 1.15; }}
        .cdp-logo-text .brand  {{ font-size: 1.25rem; font-weight: 700; color: {CLOUDERA_WHITE}; letter-spacing: -0.3px; }}
        .cdp-logo-text .sub    {{ font-size: 0.72rem; font-weight: 400; color: {CLOUDERA_MUTED}; letter-spacing: 1.2px; text-transform: uppercase; }}
        .cdp-header-right {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .cdp-pill {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.6px;
            text-transform: uppercase;
        }}
        .cdp-pill.live {{
            background: rgba(0,200,150,0.15);
            color: {PROD_ACCENT};
            border: 1px solid rgba(0,200,150,0.3);
        }}

        /* ── Section title (env columns) ────────────────────────── */
        .env-col-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 0.85rem 1.2rem;
            border-radius: 10px;
            margin-bottom: 1.2rem;
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        .env-col-header.prod {{
            background: rgba(0,200,150,0.10);
            border: 1px solid rgba(0,200,150,0.25);
            color: {PROD_ACCENT};
        }}
        .env-col-header.dev  {{
            background: rgba(59,158,255,0.10);
            border: 1px solid rgba(59,158,255,0.25);
            color: {DEV_ACCENT};
        }}
        .env-col-header.dr   {{
            background: rgba(247,183,49,0.10);
            border: 1px solid rgba(247,183,49,0.25);
            color: {DR_ACCENT};
        }}
        .env-dot {{
            width: 9px;
            height: 9px;
            border-radius: 50%;
            flex-shrink: 0;
        }}
        .env-dot.prod {{ background: {PROD_ACCENT}; box-shadow: 0 0 8px {PROD_ACCENT}; }}
        .env-dot.dev  {{ background: {DEV_ACCENT};  box-shadow: 0 0 8px {DEV_ACCENT};  }}
        .env-dot.dr   {{ background: {DR_ACCENT};   box-shadow: 0 0 8px {DR_ACCENT};   }}

        /* ── Service card ────────────────────────────────────────── */
        .svc-card {{
            background: {CLOUDERA_PANEL};
            border: 1px solid {CLOUDERA_BORDER};
            border-radius: 12px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.85rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
            position: relative;
            overflow: hidden;
        }}
        .svc-card::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(255,109,42,0.04) 0%, transparent 60%);
            pointer-events: none;
        }}
        .svc-card:hover {{
            border-color: rgba(255,109,42,0.45);
            box-shadow: 0 4px 24px rgba(255,109,42,0.15), 0 0 0 1px rgba(255,109,42,0.08);
            transform: translateY(-2px);
        }}

        .svc-icon {{
            width: 40px;
            height: 40px;
            border-radius: 9px;
            background: rgba(255,109,42,0.12);
            border: 1px solid rgba(255,109,42,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }}

        .svc-info {{
            flex: 1;
            min-width: 0;
        }}
        .svc-name {{
            font-size: 0.88rem;
            font-weight: 600;
            color: {CLOUDERA_WHITE};
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .svc-desc {{
            font-size: 0.72rem;
            color: {CLOUDERA_MUTED};
            margin-top: 1px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .svc-link {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 12px;
            border-radius: 7px;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.4px;
            text-decoration: none !important;
            white-space: nowrap;
            flex-shrink: 0;
            transition: opacity 0.15s, box-shadow 0.15s;
        }}
        .svc-link:hover {{ opacity: 0.85; box-shadow: 0 2px 12px rgba(0,0,0,0.3); }}
        .svc-link.prod {{
            background: linear-gradient(135deg, rgba(0,200,150,0.2), rgba(0,200,150,0.1));
            color: {PROD_ACCENT} !important;
            border: 1px solid rgba(0,200,150,0.35);
        }}
        .svc-link.dev {{
            background: linear-gradient(135deg, rgba(59,158,255,0.2), rgba(59,158,255,0.1));
            color: {DEV_ACCENT} !important;
            border: 1px solid rgba(59,158,255,0.35);
        }}
        .svc-link.dr {{
            background: linear-gradient(135deg, rgba(247,183,49,0.2), rgba(247,183,49,0.1));
            color: {DR_ACCENT} !important;
            border: 1px solid rgba(247,183,49,0.35);
        }}

        /* ── Search bar ──────────────────────────────────────────── */
        .stTextInput > div > div > input {{
            background: {CLOUDERA_CHARCOAL} !important;
            border: 1px solid {CLOUDERA_BORDER} !important;
            border-radius: 10px !important;
            color: {CLOUDERA_TEXT} !important;
            font-family: 'Sora', sans-serif !important;
            font-size: 0.88rem !important;
            padding: 0.65rem 1rem !important;
        }}
        .stTextInput > div > div > input:focus {{
            border-color: {CLOUDERA_ORANGE} !important;
            box-shadow: 0 0 0 2px rgba(255,109,42,0.2) !important;
        }}
        .stTextInput label {{
            color: {CLOUDERA_MUTED} !important;
            font-size: 0.8rem !important;
        }}

        /* ── Stats bar ───────────────────────────────────────────── */
        .stats-bar {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1.6rem;
            flex-wrap: wrap;
        }}
        .stat-chip {{
            background: {CLOUDERA_CHARCOAL};
            border: 1px solid {CLOUDERA_BORDER};
            border-radius: 8px;
            padding: 0.55rem 1rem;
            font-size: 0.78rem;
            color: {CLOUDERA_MUTED};
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .stat-chip b {{ color: {CLOUDERA_WHITE}; }}

        /* ── Footer ──────────────────────────────────────────────── */
        .cdp-footer {{
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid {CLOUDERA_BORDER};
            text-align: center;
            font-size: 0.72rem;
            color: {CLOUDERA_MUTED};
            letter-spacing: 0.5px;
        }}
        .cdp-footer span {{ color: {CLOUDERA_ORANGE}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Component helpers ─────────────────────────────────────────────────────────
def render_header():
    st.markdown(
        """
        <div class="cdp-header">
          <div class="cdp-logo-wrap">
            <div class="cdp-logo-icon">☁️</div>
            <div class="cdp-logo-text">
              <div class="brand">Cloudera Data Platform</div>
              <div class="sub">Internal Services Portal</div>
            </div>
          </div>
          <div class="cdp-header-right">
            <span class="cdp-pill live">● Live</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_env_header(label: str, env_class: str, count: int):
    icons = {"prod": "🟢", "dev": "🔵", "dr": "🟡"}
    st.markdown(
        f"""
        <div class="env-col-header {env_class}">
          <span class="env-dot {env_class}"></span>
          {label}
          &nbsp;&nbsp;
          <span style="font-size:0.68rem;opacity:0.7;">{count} services</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_service_card(service: dict, env: str):
    url  = service["urls"][env]
    icon = service["icon"]
    arrow = "↗"
    st.markdown(
        f"""
        <div class="svc-card">
          <div class="svc-icon">{icon}</div>
          <div class="svc-info">
            <div class="svc-name">{service['name']}</div>
            <div class="svc-desc">{service['description']}</div>
          </div>
          <a class="svc-link {env}" href="{url}" target="_blank" rel="noopener">
            Open {arrow}
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats(services, query):
    n_total   = len(services)
    n_showing = len([s for s in services if query.lower() in s["name"].lower() or query.lower() in s["description"].lower()]) if query else n_total
    st.markdown(
        f"""
        <div class="stats-bar">
          <div class="stat-chip">🔗 <b>{n_total}</b> total services</div>
          <div class="stat-chip">🟢 Production</div>
          <div class="stat-chip">🔵 Development</div>
          <div class="stat-chip">🟡 Disaster Recovery</div>
          {"<div class='stat-chip'>🔍 <b>" + str(n_showing) + "</b> matching</div>" if query else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="cdp-footer">
          Built with <span>♥</span> on Cloudera AI · Internal use only
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Main app ──────────────────────────────────────────────────────────────────
def main():
    inject_css()
    render_header()

    # Search / filter
    #search = st.text_input("", placeholder="🔍  Search services…", key="search", label_visibility="collapsed")
    # AFTER (proper label, hidden visually)
    search = st.text_input(
      "Search services",
      placeholder="🔍  Search services…",
      key="search",
      label_visibility="collapsed"   # hides the label but keeps it for accessibility
    )
    query  = search.strip()

    # Filter services
    filtered = [
        s for s in SERVICES
        if not query
        or query.lower() in s["name"].lower()
        or query.lower() in s["description"].lower()
    ]

    render_stats(SERVICES, query)

    if not filtered:
        st.markdown(
            f"<p style='color:{CLOUDERA_MUTED};text-align:center;padding:2rem;'>No services match <b style='color:{CLOUDERA_ORANGE};'>{query}</b></p>",
            unsafe_allow_html=True,
        )
        return

    # Three environment columns
    col_prod, col_dev, col_dr = st.columns(3, gap="large")

    with col_prod:
        render_env_header("PRODUCTION", "prod", len(filtered))
        for svc in filtered:
            render_service_card(svc, "prod")

    with col_dev:
        render_env_header("DEVELOPMENT", "dev", len(filtered))
        for svc in filtered:
            render_service_card(svc, "dev")

    with col_dr:
        render_env_header("DISASTER RECOVERY", "dr", len(filtered))
        for svc in filtered:
            render_service_card(svc, "dr")

    render_footer()


if __name__ == "__main__":
    main()
