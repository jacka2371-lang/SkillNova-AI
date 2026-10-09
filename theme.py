
import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        @import url(
          'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
        );

        .stApp {
            background: #0b1020;
            color: #f4f5ff;
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stSidebar"] {
            background: #10172a;
            border-right: 1px solid #252d46;
        }

        [data-testid="stSidebar"] * {
            color: #edf0ff;
        }

        h1, h2, h3 {
            color: #f7f7ff !important;
            font-weight: 750 !important;
        }

        p, label, .stMarkdown {
            color: #d0d6ea;
        }

        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #171f38, #1d2040);
            border: 1px solid #303958;
            padding: 18px;
            border-radius: 16px;
        }

        [data-testid="stMetricValue"] {
            color: #a99bff;
        }

        div.stButton > button,
        div.stDownloadButton > button {
            background: linear-gradient(90deg, #7657ff, #477dff);
            color: white;
            border: 0;
            border-radius: 10px;
            min-height: 42px;
            font-weight: 650;
        }

        div.stButton > button:hover,
        div.stDownloadButton > button:hover {
            border: 1px solid #b8adff;
            color: white;
            filter: brightness(1.12);
        }

        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea {
            background: #131b30;
            color: white;
        }

        div[data-baseweb="select"] > div {
            background: #131b30;
        }

        .hero-card {
            padding: 28px;
            border-radius: 20px;
            background: linear-gradient(120deg, #29235c, #172f5d);
            border: 1px solid #45447c;
            margin-bottom: 22px;
        }

        .hero-card h2 {
            margin-bottom: 8px;
        }

        .hero-card p {
            color: #e1e5ff;
            margin-bottom: 0;
        }

        .feature-card {
            background: #141c31;
            border: 1px solid #2b3552;
            border-radius: 16px;
            padding: 20px;
            min-height: 145px;
        }

        .feature-card h3 {
            font-size: 18px;
            margin-top: 0;
        }

        .muted {
            color: #a7b0ca;
            font-size: 13px;
        }

        .badge-card {
            background: #1b2440;
            border: 1px solid #474c7d;
            border-radius: 14px;
            padding: 14px;
            text-align: center;
        }

        [data-testid="stProgressBar"] > div > div {
            background: linear-gradient(90deg, #8b5cf6, #4895ff);
        }

        hr {
            border-color: #29324d;
        }

        #MainMenu, footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_hero(name="Learner"):
    safe_name = str(name).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    st.markdown(
        f"""
        <div class="hero-card">
            <p class="muted">YOUR PERSONAL CAREER WORKSPACE</p>
            <h2>Welcome back, {safe_name} ✨</h2>
            <p>Build your skills. Improve your resume. Discover your next opportunity.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
