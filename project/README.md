# 🎬 CineMatch — Movie Recommendation System

A content-based movie recommendation web app built with Python and Streamlit. Select any movie and instantly get similar recommendations powered by unsupervised machine learning.

![Python](https://img.shields.io/badge/Python-3.13-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red) ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange) ![TMDB](https://img.shields.io/badge/TMDB-API-green)

---

## 📌 Features

- 🔍 Search from 45,000+ movies
- 🎯 Cluster-based recommendations (TF-IDF + PCA + DBSCAN)
- 🖼️ Movie posters fetched from TMDB API
- ⭐ Rating, release year, and genre tags on every card
- 🎛️ Choose 5, 10, 15, or 20 recommendations
- ⚡ Fast loading with cached data (`@st.cache_data`)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.13 | Core language |
| Streamlit | Web UI framework |
| Pandas | Data loading & processing |
| Scikit-learn | TF-IDF, PCA, DBSCAN |
| TMDB API | Movie poster images |
| Requests | HTTP calls to TMDB |
| Pickle | Fast serialised data storage |

---

## 📁 Project Structure

```
project/
│
├── app.py                  # Main Streamlit application
├── meta_data.pkl           # Processed movie data with cluster labels
├── movies_metadata.csv     # Raw TMDB dataset (45,000+ movies)
├── poster_map.pkl          # Auto-generated poster cache (created on first run)
└── README.md               # This file
```

---

## ⚙️ How It Works

```
movies_metadata.csv
        ↓
   TF-IDF Vectorization    →  Text (overview + genres + keywords) to numbers
        ↓
   PCA                     →  Reduce dimensions, remove noise
        ↓
   DBSCAN Clustering       →  Group similar movies into clusters
        ↓
   meta_data.pkl           →  Saved with cluster labels
        ↓
   Streamlit App           →  User picks movie → fetch same cluster → show results
```

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone 
cd demo
```

### 2. Install dependencies
```bash
pip install streamlit pandas scikit-learn requests
```

### 3. Get a free TMDB API key
1. Go to [themoviedb.org](https://www.themoviedb.org) → Sign Up
2. Profile → Settings → API → Create → Developer
3. Copy your **API Key (v3)**

### 4. Add your API key in `app.py`
```python
# Line 6 in app.py
TMDB_API_KEY = "your_api_key_here"
```

### 5. Run the app
```bash
streamlit run app.py
```

Open browser at **http://localhost:8501**

> **Note:** On first run, the app will fetch posters for all movies from TMDB and save them to `poster_map.pkl`. This is a one-time process — subsequent runs will load instantly from cache.

---

## 📸 Screenshot

> App displays movie recommendations in a 5-column card grid with posters, ratings, years, and genre tags.

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| Posters not showing | Delete `poster_map.pkl` and restart the app |
| `KeyError: poster_path` | Make sure `movies_metadata.csv` is in the same folder as `app.py` |
| `KeyError: cluster` | Ensure `meta_data.pkl` was generated with DBSCAN cluster labels |
| API warning on screen | Add your TMDB API key on line 6 of `app.py` |
| Slow first load | Normal — posters are being fetched from TMDB (one-time only) |

---

## 🤖 ML Approach

**TF-IDF** converts each movie's text (overview, genres, keywords) into a numerical vector — words unique to a movie get higher weight.

**PCA** compresses the high-dimensional TF-IDF vectors into fewer dimensions, removing noise and speeding up clustering.

**DBSCAN** groups movies that are close together in feature space into clusters. Movies in the same cluster share similar themes and content — these become the recommendations.

---

## 📄 License

This project uses the [TMDB API](https://www.themoviedb.org/documentation/api) for poster images.  
Dataset: [TMDB Movies Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

---

*Powered by TF-IDF · PCA · DBSCAN · Built with Streamlit*
