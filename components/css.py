"""Komponen CSS Kustom untuk Streamlit."""

import streamlit as st

def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1100px;
        }
        .hero-card {
            background: linear-gradient(135deg, rgba(37,99,235,0.18), rgba(59,130,246,0.12));
            border: 1px solid rgba(96,165,250,0.22);
            border-radius: 16px;
            padding: 1.75rem 2rem;
            margin-bottom: 1.5rem;
        }
        .hero-title {
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 0.35rem 0;
            letter-spacing: -0.02em;
        }
        .hero-subtitle {
            font-size: 1.02rem;
            color: rgba(226,232,240,0.82);
            margin: 0 0 1rem 0;
            line-height: 1.55;
        }
        .hero-badge {
            display: inline-block;
            background: rgba(37,99,235,0.22);
            color: #93c5fd;
            border: 1px solid rgba(96,165,250,0.35);
            border-radius: 999px;
            padding: 0.28rem 0.85rem;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        .section-card {
            background: rgba(30,41,59,0.55);
            border: 1px solid rgba(148,163,184,0.14);
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
        }
        .section-step {
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #60a5fa;
            margin-bottom: 0.35rem;
        }
        .section-title {
            font-size: 1.15rem;
            font-weight: 650;
            margin: 0 0 0.35rem 0;
        }
        .section-desc {
            font-size: 0.92rem;
            color: rgba(203,213,225,0.78);
            margin: 0 0 0.75rem 0;
        }
        .meta-label {
            font-size: 0.75rem;
            color: rgba(148,163,184,0.95);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.15rem;
        }
        .meta-value {
            font-size: 1rem;
            font-weight: 600;
            color: #f8fafc;
            word-break: break-word;
        }
        .empty-state {
            text-align: center;
            padding: 2.5rem 1.5rem;
            border: 1px dashed rgba(148,163,184,0.28);
            border-radius: 16px;
            background: rgba(15,23,42,0.35);
            margin: 1rem 0 1.5rem 0;
        }
        .empty-icon { font-size: 2.2rem; margin-bottom: 0.5rem; }
        .empty-title { font-size: 1.05rem; font-weight: 650; margin-bottom: 0.25rem; }
        .empty-desc { font-size: 0.92rem; color: rgba(203,213,225,0.72); }
        .result-card {
            background: linear-gradient(160deg, rgba(30,41,59,0.92), rgba(15,23,42,0.82));
            border: 1px solid rgba(96,165,250,0.32);
            border-radius: 20px;
            padding: 2.75rem 2rem;
            margin: 1rem 0 1.25rem 0;
            text-align: center;
            box-shadow: 0 12px 40px rgba(15,23,42,0.45);
        }
        .result-inner {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .result-emoji {
            font-size: 4.5rem;
            line-height: 1;
            margin-bottom: 0.65rem;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.25));
        }
        .result-label {
            font-size: 2.1rem;
            font-weight: 700;
            margin: 0 0 0.85rem 0;
            text-transform: capitalize;
            letter-spacing: -0.01em;
        }
        .result-conf-label {
            font-size: 0.78rem;
            font-weight: 650;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #94a3b8;
            margin-bottom: 0.35rem;
        }
        .result-confidence {
            font-size: 4.25rem;
            font-weight: 800;
            margin: 0;
            line-height: 1;
            background: linear-gradient(135deg, #93c5fd, #60a5fa, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .result-dominance {
            font-size: 0.82rem;
            color: #94a3b8;
            margin: 0 0 0.5rem 0;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 650;
        }
        .result-rank-note {
            font-size: 0.92rem;
            color: rgba(203,213,225,0.82);
            margin: 0.85rem 0 0 0;
            line-height: 1.45;
        }
        .result-margin {
            display: inline-block;
            margin-top: 0.55rem;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(37,99,235,0.18);
            border: 1px solid rgba(96,165,250,0.28);
            font-size: 0.82rem;
            color: #93c5fd;
            font-weight: 600;
        }
        .top3-card {
            background: rgba(15,23,42,0.55);
            border: 1px solid rgba(148,163,184,0.16);
            border-radius: 14px;
            padding: 0.9rem 1rem;
            text-align: center;
            min-height: 118px;
        }
        .top3-rank {
            font-size: 0.72rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .top3-emoji { font-size: 1.6rem; margin: 0.15rem 0; }
        .top3-label { font-size: 1rem; font-weight: 650; text-transform: capitalize; }
        .top3-pct {
            font-size: 1.15rem;
            font-weight: 700;
            color: #60a5fa;
            margin-top: 0.15rem;
        }
        .top3-conf-label {
            font-size: 0.68rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .transcript-card {
            background: linear-gradient(145deg, rgba(30,41,59,0.85), rgba(15,23,42,0.78));
            border: 1px solid rgba(96,165,250,0.28);
            border-left: 4px solid #3b82f6;
            border-radius: 14px;
            padding: 1.1rem 1.35rem;
            margin: 0.5rem 0 1rem 0;
        }
        .transcript-head {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #60a5fa;
            margin-bottom: 0.45rem;
        }
        .transcript-text {
            font-size: 1.05rem;
            color: #f1f5f9;
            line-height: 1.55;
            font-style: italic;
        }
        .transcript-empty {
            font-size: 0.95rem;
            color: rgba(148,163,184,0.85);
            font-style: italic;
        }
        .prob-row-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.92rem;
            margin-bottom: 0.2rem;
        }
        .prob-bar-wrap {
            background: rgba(51,65,85,0.65);
            border-radius: 999px;
            height: 10px;
            overflow: hidden;
            margin-bottom: 0.85rem;
        }
        .prob-bar-fill {
            height: 10px;
            border-radius: 999px;
        }
        .sidebar-pill {
            display: inline-block;
            background: rgba(51,65,85,0.75);
            border: 1px solid rgba(148,163,184,0.18);
            border-radius: 999px;
            padding: 0.18rem 0.62rem;
            margin: 0.12rem 0.18rem 0.12rem 0;
            font-size: 0.78rem;
            text-transform: capitalize;
        }
        .sidebar-header {
            background: linear-gradient(145deg, rgba(37,99,235,0.28), rgba(29,78,216,0.18));
            border: 1px solid rgba(96,165,250,0.22);
            border-radius: 14px;
            padding: 1rem 1rem 0.85rem 1rem;
            margin-bottom: 0.85rem;
            text-align: center;
        }
        .sidebar-header-icon {
            font-size: 1.75rem;
            margin-bottom: 0.25rem;
        }
        .sidebar-header-title {
            font-size: 1.05rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.01em;
        }
        .sidebar-header-sub {
            font-size: 0.78rem;
            color: rgba(203,213,225,0.72);
            margin: 0.25rem 0 0 0;
            line-height: 1.4;
        }
        .sidebar-stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.55rem;
            margin-bottom: 0.85rem;
        }
        .sidebar-stat-card {
            background: rgba(15,23,42,0.55);
            border: 1px solid rgba(148,163,184,0.14);
            border-radius: 12px;
            padding: 0.65rem 0.7rem;
        }
        .sidebar-stat-icon {
            font-size: 1rem;
            margin-bottom: 0.15rem;
        }
        .sidebar-stat-label {
            font-size: 0.68rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.1rem;
        }
        .sidebar-stat-value {
            font-size: 0.82rem;
            font-weight: 650;
            color: #f1f5f9;
            line-height: 1.25;
        }
        .sidebar-status-card {
            border-radius: 12px;
            padding: 0.7rem 0.85rem;
            margin-bottom: 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.65rem;
        }
        .sidebar-status-ok {
            background: rgba(37,99,235,0.12);
            border: 1px solid rgba(96,165,250,0.32);
        }
        .sidebar-status-fail {
            background: rgba(248,113,113,0.1);
            border: 1px solid rgba(248,113,113,0.28);
        }
        .sidebar-status-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        .sidebar-status-dot.ok {
            background: #3b82f6;
            box-shadow: 0 0 8px rgba(59,130,246,0.65);
        }
        .sidebar-status-dot.fail {
            background: #f87171;
            box-shadow: 0 0 8px rgba(248,113,113,0.55);
        }
        .sidebar-status-text {
            font-size: 0.84rem;
            font-weight: 650;
            color: #f8fafc;
        }
        .sidebar-status-sub {
            font-size: 0.72rem;
            color: rgba(203,213,225,0.65);
            margin-top: 0.05rem;
        }
        .sidebar-section-label {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: #60a5fa;
            margin: 0.15rem 0 0.55rem 0;
        }
        .sidebar-emotion-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.45rem;
            margin-bottom: 0.85rem;
        }
        .sidebar-emotion-item {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            background: rgba(15,23,42,0.45);
            border: 1px solid rgba(148,163,184,0.12);
            border-left: 3px solid var(--emotion-color, #2563eb);
            border-radius: 10px;
            padding: 0.42rem 0.55rem;
            font-size: 0.78rem;
            text-transform: capitalize;
        }
        .sidebar-emotion-emoji { font-size: 1rem; line-height: 1; }
        .sidebar-emotion-id {
            font-size: 0.65rem;
            color: #64748b;
            margin-left: auto;
        }
        .sidebar-howto {
            background: rgba(30,41,59,0.45);
            border: 1px solid rgba(148,163,184,0.12);
            border-radius: 12px;
            padding: 0.75rem 0.85rem;
            margin-bottom: 0.75rem;
        }
        .sidebar-howto-step {
            display: flex;
            align-items: flex-start;
            gap: 0.55rem;
            margin-bottom: 0.55rem;
        }
        .sidebar-howto-step:last-child { margin-bottom: 0; }
        .sidebar-howto-num {
            background: rgba(37,99,235,0.25);
            color: #93c5fd;
            border-radius: 999px;
            width: 1.35rem;
            height: 1.35rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.72rem;
            font-weight: 700;
            flex-shrink: 0;
        }
        .sidebar-howto-text {
            font-size: 0.78rem;
            color: rgba(226,232,240,0.85);
            line-height: 1.35;
            padding-top: 0.05rem;
        }
        .sidebar-divider {
            border: none;
            border-top: 1px solid rgba(148,163,184,0.12);
            margin: 0.65rem 0;
        }
        .status-ok { color: #60a5fa; font-weight: 650; }
        .status-fail { color: #f87171; font-weight: 650; }
        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(12,30,58,0.92));
        }
        div[data-testid="stSidebar"] .block-container { padding-top: 1rem; }
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
            border: none !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 0.72rem 1rem !important;
            font-weight: 650 !important;
            box-shadow: 0 8px 24px rgba(37,99,235,0.28) !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
            box-shadow: 0 10px 28px rgba(37,99,235,0.36) !important;
        }
        div.stButton > button:disabled {
            opacity: 0.55 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
