import streamlit as st
import pandas as pd
import requests

# --------------------------------------------------
TMDB_API_KEY = "1549fc9cc5d49235a8ad3b14c4a3e1cc"
# --------------------------------------------------

st.set_page_config(
    page_title="CineMatch – Movie Recommender",
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

def fetch_and_save_posters(meta):
    rows     = []
    progress = st.progress(0, text="Posters fetch ho rahe hain... pehli baar thoda time lagega")
    total    = len(meta)
    for i, (_, row) in enumerate(meta.iterrows()):
        poster = ""
        try:
            r = requests.get(f"https://api.themoviedb.org/3/movie/{int(row['id'])}?api_key={TMDB_API_KEY}", timeout=5).json()
            poster = r.get("poster_path", "") or ""
        except Exception:
            pass
        rows.append({"title": row["title"], "poster_path": poster})
        if i % 100 == 0:
            progress.progress(min(i / total, 1.0), text=f"Fetching posters... {i}/{total}")
    progress.empty()
    df = pd.DataFrame(rows)
    df.to_pickle("poster_map.pkl")
    return df

def recommend_cluster(movie_title, n=10):
    idx     = meta_data[meta_data["title"] == movie_title].index[0]
    cluster = meta_data.loc[idx, "cluster"]
    return meta_data[
        (meta_data["cluster"] == cluster) & (meta_data.index != idx)
    ][["title", "genres", "vote_average", "release_date", "id"]].head(n)

st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.hero {
    text-align:center; padding:3rem 2rem 2.5rem;
    background:#0f0f0f; border-radius:20px;
    margin-bottom:2rem; border:1px solid #222;
}
.hero h1 { font-size:2.8rem; font-weight:800; letter-spacing:-1px; color:#fff; margin:0 0 0.4rem; }
.hero .accent { color:#e50914; }
.hero p { color:#aaa; font-size:1.05rem; margin:0; }
.section-title {
    font-size:1.3rem; font-weight:700; color:#fff;
    margin:1.5rem 0 1rem; padding-bottom:0.5rem;
    border-bottom:2px solid #e50914; display:inline-block;
}
.movie-card {
    background:#141414; border:1px solid #222; border-radius:14px;
    overflow:hidden; transition:transform 0.2s ease,border-color 0.2s ease; height:100%;
}
.movie-card:hover { transform:translateY(-4px); border-color:#e50914; }
.card-body { padding:0.75rem 0.9rem 1rem; }
.card-title {
    font-size:0.95rem; font-weight:700; color:#f0f0f0;
    margin:0 0 0.3rem; line-height:1.3;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.card-meta { display:flex; align-items:center; gap:10px; font-size:0.8rem; color:#888; margin-bottom:0.5rem; }
.card-rating { color:#f5c518; font-weight:600; }
.card-year   { color:#777; }
.genre-tag {
    display:inline-block; background:#1e1e1e; border:1px solid #333;
    color:#bbb; font-size:0.72rem; padding:2px 8px;
    border-radius:20px; margin:2px 3px 2px 0; white-space:nowrap;
}
.no-poster {
    background:#1a1a1a; height:260px;
    display:flex; align-items:center; justify-content:center; font-size:2.5rem;
}
.empty-state { text-align:center; padding:3rem 2rem; color:#555; font-size:1rem; }
.empty-state .icon { font-size:3rem; margin-bottom:0.8rem; }
.footer { text-align:center; color:#444; font-size:0.78rem; padding:2rem 0 0.5rem; letter-spacing:0.05em; }
.footer span { color:#666; }
div[data-testid="stSelectbox"] label { font-weight:600; color:#aaa; font-size:0.85rem; letter-spacing:0.06em; text-transform:uppercase; }
div[data-testid="stSelectbox"] > div > div { background-color:#141414 !important; border:1px solid #333 !important; border-radius:10px !important; color:#f0f0f0 !important; }
div.stButton > button { background:#e50914; color:white; border:none; border-radius:10px; padding:0.65rem 1.5rem; font-weight:700; font-size:1rem; transition:background 0.2s ease,transform 0.1s ease; }
div.stButton > button:hover { background:#ff1a24; transform:translateY(-1px); }
div.stButton > button:active { transform:scale(0.98); }
</style>
""", unsafe_allow_html=True)

meta_data  = load_data()
poster_map = None

if TMDB_API_KEY == "1apni":
    st.warning("TMDB API key daalo — app.py line 6 pe. Free key lo: https://www.themoviedb.org/settings/api", icon="🔑")
else:
    poster_map = load_poster_map()
    if poster_map is None:
        with st.spinner("Pehli baar posters fetch ho rahe hain..."):
            poster_map = fetch_and_save_posters(meta_data)

st.markdown("""
<div class="hero">
    <h1>🎬 <span class="accent">Cine</span>Match</h1>
    <p>Discover movies that match your taste — powered by smart clustering</p>
</div>
""", unsafe_allow_html=True)

col_search, col_count = st.columns([3, 1])
with col_search:
    movie_list     = sorted(meta_data["title"].dropna().unique())
    selected_movie = st.selectbox("🔍 Pick a movie you love", movie_list)
with col_count:
    n_recommendations = st.selectbox("Show", [5, 10, 15, 20], index=1)

st.markdown("<br>", unsafe_allow_html=True)
get_recs = st.button("Find similar movies →", use_container_width=True)

if get_recs:
    with st.spinner("Finding the best matches..."):
        recommendations = recommend_cluster(selected_movie, n=n_recommendations)

    if recommendations.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🎞️</div>
            <p>No similar movies found.<br>Try a different title!</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="section-title">Movies similar to &nbsp;<em>{selected_movie}</em></div>', unsafe_allow_html=True)
        cols = st.columns(5)
        for i, (_, row) in enumerate(recommendations.iterrows()):
            with cols[i % 5]:
                poster = ""
                if poster_map is not None:
                    match = poster_map[poster_map["title"] == row["title"]]
                    if not match.empty:
                        poster = str(match.iloc[0]["poster_path"]).strip()
                if poster and poster not in ("", "nan", "null", "None") and poster.startswith("/"):
                    st.image("https://image.tmdb.org/t/p/w300" + poster, use_container_width=True)
                else:
                    st.markdown('<div class="no-poster">🎬</div>', unsafe_allow_html=True)

                year = "N/A"
                if pd.notna(row.get("release_date")):
                    year = str(row["release_date"])[:4]
                try:
                    rating_display = f"⭐ {float(row.get('vote_average', 0)):.1f}"
                except (ValueError, TypeError):
                    rating_display = "⭐ N/A"

                genres = row.get("genres", [])
                if isinstance(genres, list):
                    genre_tags = "".join(f'<span class="genre-tag">{g}</span>' for g in genres[:3])
                else:
                    genre_tags = f'<span class="genre-tag">{genres}</span>'

                st.markdown(f"""
                <div class="movie-card">
                    <div class="card-body">
                        <div class="card-title" title="{row['title']}">{row['title']}</div>
                        <div class="card-meta">
                            <span class="card-rating">{rating_display}</span>
                            <span class="card-year">📅 {year}</span>
                        </div>
                        <div>{genre_tags}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">🍿</div>
        <p>Select a movie above and click <strong>Find similar movies</strong> to get personalised recommendations.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Powered by <span>TF-IDF · PCA · DBSCAN</span> · Built with Streamlit
</div>""", unsafe_allow_html=True)