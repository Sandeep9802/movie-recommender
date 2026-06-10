import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_data
def load_data():
    meta = pd.read_pickle("meta_data.pkl")
    csv  = pd.read_csv("movies_metadata.csv")[["id", "title"]]
    csv["id"] = pd.to_numeric(csv["id"], errors="coerce")
    csv  = csv.dropna(subset=["id"])
    csv["id"] = csv["id"].astype(int)
    csv  = csv.drop_duplicates(subset=["title"], keep="first")
    meta = meta.drop(columns=["poster_path", "id"], errors="ignore")
    meta = meta.merge(csv, on="title", how="left")
    return meta

@st.cache_data
def load_poster_map():
    try:
        return pd.read_pickle("poster_map.pkl")
    except FileNotFoundError:
        return None

def recommend_cluster(movie_title, n=10):
    idx     = meta_data[meta_data["title"] == movie_title].index[0]
    cluster = meta_data.loc[idx, "cluster"]
    return meta_data[
        (meta_data["cluster"] == cluster) & (meta_data.index != idx)
    ][["title", "genres", "vote_average", "release_date"]].head(n)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Netflix+Sans:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    background-color: #141414;
    color: #e5e5e5;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── Netflix-style Top Nav ── */
.nf-nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: linear-gradient(to bottom, #000 0%, transparent 100%);
    padding: 18px 4%;
    display: flex;
    align-items: center;
    gap: 40px;
}
.nf-logo {
    font-size: 2rem;
    font-weight: 900;
    color: #e50914;
    letter-spacing: -2px;
    font-family: 'Inter', sans-serif;
    text-transform: uppercase;
}

/* ── Hero Banner ── */
.nf-hero {
    position: relative;
    width: 100%;
    height: 520px;
    background: linear-gradient(
        to right,
        #000 0%, #000 20%,
        rgba(0,0,0,0.8) 40%,
        rgba(0,0,0,0.4) 70%,
        transparent 100%
    ),
    linear-gradient(
        to top,
        #141414 0%,
        transparent 30%
    ),
    radial-gradient(ellipse at 70% 50%, #1a0a0a 0%, #0a0a1a 40%, #000 100%);
    display: flex;
    align-items: center;
    padding: 0 4%;
    margin-top: -80px;
}
.nf-hero-content {
    max-width: 600px;
    padding-top: 80px;
}
.nf-hero-eyebrow {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #e50914;
    margin-bottom: 16px;
}
.nf-hero-title {
    font-size: 3.8rem;
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -2px;
    color: #fff;
    margin-bottom: 16px;
}
.nf-hero-title span { color: #e50914; }
.nf-hero-desc {
    font-size: 1.05rem;
    color: #aaa;
    line-height: 1.6;
    font-weight: 300;
    max-width: 480px;
}

/* ── Search Row ── */
.nf-search-row {
    padding: 0 4% 32px;
    background: linear-gradient(to bottom, transparent, #141414 40%);
    margin-top: -60px;
    position: relative;
    z-index: 10;
}

/* ── Section Label ── */
.nf-section-label {
    font-size: 1.35rem;
    font-weight: 700;
    color: #e5e5e5;
    padding: 8px 4% 16px;
    letter-spacing: -0.3px;
}
.nf-section-label span {
    color: #e50914;
    font-style: italic;
}

/* ── Movie Row ── */
.nf-row {
    padding: 0 4% 48px;
}

/* ── Movie Card ── */
.nf-card {
    position: relative;
    border-radius: 6px;
    overflow: hidden;
    background: #1f1f1f;
    transition: transform 0.25s ease, box-shadow 0.25s ease, z-index 0s;
    cursor: pointer;
}
.nf-card:hover {
    transform: scale(1.08);
    box-shadow: 0 20px 60px rgba(0,0,0,0.8);
    z-index: 10;
}
.nf-card img {
    width: 100%;
    display: block;
    aspect-ratio: 2/3;
    object-fit: cover;
}
.nf-card-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.6) 60%, transparent 100%);
    padding: 32px 10px 10px;
    opacity: 0;
    transition: opacity 0.25s ease;
}
.nf-card:hover .nf-card-overlay { opacity: 1; }
.nf-card-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #fff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 4px;
}
.nf-card-meta {
    font-size: 0.72rem;
    color: #aaa;
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
}
.nf-card-rating { color: #46d369; font-weight: 700; }
.nf-genre-pill {
    background: rgba(255,255,255,0.15);
    border-radius: 3px;
    padding: 1px 6px;
    font-size: 0.68rem;
    color: #ccc;
}

/* ── No Poster ── */
.nf-no-poster {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    gap: 8px;
}
.nf-no-poster-label {
    font-size: 0.65rem;
    color: #555;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Card Info Below ── */
.nf-card-info {
    padding: 8px 4px 16px;
}
.nf-card-info-title {
    font-size: 0.82rem;
    font-weight: 600;
    color: #e5e5e5;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 4px;
}
.nf-card-info-meta {
    font-size: 0.72rem;
    color: #777;
    display: flex;
    gap: 8px;
    align-items: center;
}
.nf-card-info-rating { color: #46d369; font-weight: 600; }

/* ── Empty State ── */
.nf-empty {
    padding: 80px 4%;
    text-align: center;
    color: #555;
}
.nf-empty-icon { font-size: 4rem; margin-bottom: 16px; }
.nf-empty-title { font-size: 1.4rem; font-weight: 700; color: #777; margin-bottom: 8px; }
.nf-empty-sub { font-size: 0.9rem; color: #555; }

/* ── Footer ── */
.nf-footer {
    padding: 40px 4%;
    border-top: 1px solid #222;
    color: #555;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
}
.nf-footer span { color: #e50914; }

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] > div > div {
    background-color: #2a2a2a !important;
    border: 1px solid #444 !important;
    border-radius: 4px !important;
    color: #e5e5e5 !important;
    font-size: 0.95rem !important;
}
div[data-testid="stSelectbox"] label {
    color: #aaa !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
div.stButton > button {
    background: #e50914 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    transition: background 0.15s ease !important;
    width: 100% !important;
}
div.stButton > button:hover { background: #f40612 !important; }
div.stButton > button:active { background: #b20710 !important; }
div[data-testid="stImage"] img {
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── Load Data ──
meta_data  = load_data()
poster_map = load_poster_map()

# ── Nav ──
st.markdown("""
<div class="nf-nav">
    <div class="nf-logo">CineMatch</div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──
st.markdown("""
<div class="nf-hero">
    <div class="nf-hero-content">
        <div class="nf-hero-eyebrow">Powered by Machine Learning</div>
        <div class="nf-hero-title">Find Your<br><span>Next Favourite</span><br>Movie</div>
        <div class="nf-hero-desc">Pick any movie and instantly discover similar titles — matched by theme, genre, and story using AI clustering.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Search Row ──
st.markdown('<div class="nf-search-row">', unsafe_allow_html=True)
col_search, col_count, col_btn = st.columns([4, 1, 1])
with col_search:
    movie_list     = sorted(meta_data["title"].dropna().unique())
    selected_movie = st.selectbox("Search a movie", movie_list)
with col_count:
    n_recommendations = st.selectbox("Results", [5, 10, 15, 20], index=1)
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    get_recs = st.button("▶  Find Similar", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Results ──
if get_recs:
    with st.spinner(""):
        recommendations = recommend_cluster(selected_movie, n=n_recommendations)

    if recommendations.empty:
        st.markdown("""
        <div class="nf-empty">
            <div class="nf-empty-icon">🎞️</div>
            <div class="nf-empty-title">No matches found</div>
            <div class="nf-empty-sub">Try a different title</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="nf-section-label">Because you picked &nbsp;<span>{selected_movie}</span></div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="nf-row">', unsafe_allow_html=True)
        cols = st.columns(5)

        for i, (_, row) in enumerate(recommendations.iterrows()):
            with cols[i % 5]:
                # Poster
                poster = ""
                if poster_map is not None:
                    match = poster_map[poster_map["title"] == row["title"]]
                    if not match.empty:
                        poster = str(match.iloc[0]["poster_path"]).strip()

                if poster and poster not in ("", "nan", "null", "None") and poster.startswith("/"):
                    st.markdown('<div class="nf-card">', unsafe_allow_html=True)
                    st.image("https://image.tmdb.org/t/p/w300" + poster, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="nf-card">
                        <div class="nf-no-poster">
                            🎬
                            <span class="nf-no-poster-label">No Poster</span>
                        </div>
                    </div>""", unsafe_allow_html=True)

                # Year
                year = "N/A"
                if pd.notna(row.get("release_date")):
                    year = str(row["release_date"])[:4]

                # Rating
                try:
                    rating = f"{float(row.get('vote_average', 0)):.1f}"
                except (ValueError, TypeError):
                    rating = "N/A"

                # Genres
                genres = row.get("genres", [])
                if isinstance(genres, list):
                    genre_str = " · ".join(genres[:2])
                else:
                    genre_str = str(genres)

                st.markdown(f"""
                <div class="nf-card-info">
                    <div class="nf-card-info-title" title="{row['title']}">{row['title']}</div>
                    <div class="nf-card-info-meta">
                        <span class="nf-card-info-rating">★ {rating}</span>
                        <span>{year}</span>
                        <span style="color:#555">{genre_str}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="nf-empty">
        <div class="nf-empty-icon">🍿</div>
        <div class="nf-empty-title">What will you watch next?</div>
        <div class="nf-empty-sub">Search a movie above and click Find Similar</div>
    </div>""", unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="nf-footer">
    <span>CineMatch</span> &nbsp;·&nbsp; Powered by TF-IDF · PCA · DBSCAN · Streamlit
</div>""", unsafe_allow_html=True)