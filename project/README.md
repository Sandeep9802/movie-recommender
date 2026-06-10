# 🎬 CineMatch — Movie Recommendation System

> Discover your next favourite movie — powered by Machine Learning

![Python](https://img.shields.io/badge/Python-3.13-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red) ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange)

---

## What is CineMatch?

CineMatch is a content-based movie recommendation system. Pick any movie from 45,000+ titles and instantly get similar recommendations — matched by theme, genre, and story using AI clustering. Movie posters, ratings, release years, and genre tags are shown for every result in a Netflix-style UI.

---

## How It Works

```
movies_metadata.csv
      ↓
TF-IDF Vectorization   →  Convert movie text (overview + genres + keywords) to numbers
      ↓
PCA                    →  Reduce dimensions, remove noise
      ↓
DBSCAN Clustering      →  Group similar movies into clusters
      ↓
meta_data.pkl          →  Saved with cluster labels
      ↓
Streamlit App          →  Pick movie → find cluster → show recommendations
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.13 | Core language |
| Streamlit | Web UI framework |
| Pandas | Data loading & processing |
| Scikit-learn | TF-IDF, PCA, DBSCAN |
| Pickle | Fast serialised data storage |

---

## Project Structure

```
project/
│
├── app.py                 # Main Streamlit application
├── meta_data.pkl          # Processed movie data with cluster labels
├── movies_metadata.csv    # Raw TMDB dataset (45,000+ movies)
├── poster_map.pkl         # Movie poster paths cache
├── movies.ipynb           # ML pipeline notebook
└── README.md              # This file
```

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Sandeep9802/demo.git
cd demo
```

### 2. Install dependencies
```bash
pip install streamlit pandas scikit-learn
```

### 3. Run the app
```bash
streamlit run app.py
```

Open browser at **http://localhost:8501**

---

## Features

- 🔍 Search from 45,000+ movie titles
- 🎯 Cluster-based recommendations — semantically similar movies
- 🖼️ Movie posters loaded from TMDB CDN
- ⭐ Rating, release year, and genre tags on every card
- 🎛️ Choose 5, 10, 15, or 20 recommendations
- ⚡ Fast loading with `@st.cache_data`
- 🎬 Netflix-style dark UI with hover effects

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Posters not showing | Make sure `poster_map.pkl` is in the project folder |
| `KeyError: cluster` | Ensure `meta_data.pkl` was generated with DBSCAN cluster labels |
| App not loading | Run `pip install streamlit pandas scikit-learn` |

---

*Powered by TF-IDF · PCA · DBSCAN · Built with Streamlit*