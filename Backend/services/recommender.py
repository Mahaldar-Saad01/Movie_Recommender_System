import pickle
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

from services.posterfetch import fetch_poster

BASE_DIR = Path(__file__).resolve().parent.parent

vector_path = BASE_DIR / "vectors.csv"
similarity_path = BASE_DIR / "similarity.pkl"
movies_path = BASE_DIR / "data" / "tmdb_5000_movies.csv"

vectors = pd.read_csv(vector_path)
similarity = pickle.load(open(similarity_path, "rb"))
movies = pd.read_csv(movies_path)
movies_by_id = movies.set_index("id")


def _movie_details(row):
    movie_id = int(row["id"])
    details = movies_by_id.loc[movie_id] if movie_id in movies_by_id.index else {}
    release_date = str(details.get("release_date", "")) if hasattr(details, "get") else ""
    year = release_date[:4] if release_date and release_date != "nan" else "N/A"
    return movie_id, details, year


def _movie_card(row, poster):
    movie_id, details, year = _movie_details(row)
    rating = details.get("vote_average", "") if hasattr(details, "get") else ""
    overview = details.get("overview", "") if hasattr(details, "get") else ""

    return {
        "id": movie_id,
        "title": row["title"],
        "year": year,
        "rating": round(float(rating), 1) if rating != "" and not pd.isna(rating) else "N/A",
        "overview": overview if isinstance(overview, str) and overview else "No overview available.",
        "poster": poster,
    }


def Recommend(movie):
    matches = vectors[vectors["title"] == movie]
    if matches.empty:
        return []

    index = matches.index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1],
    )

    rows = [vectors.iloc[i[0]] for i in distances[1:7]]
    with ThreadPoolExecutor(max_workers=6) as executor:
        posters = list(
            executor.map(
                lambda row: fetch_poster(row["title"], _movie_details(row)[2]),
                rows,
            )
        )

    return [_movie_card(row, poster) for row, poster in zip(rows, posters)]
