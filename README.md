# CineMatch Movie Recommender

CineMatch is a FastAPI movie recommendation web app built from the TMDB 5000 movie dataset. A user selects a movie, the backend finds similar movies using a precomputed similarity matrix, and the frontend displays polished recommendation cards with posters, release years, ratings, and overviews.

## Features

- Search/select a movie from the local movie list.
- Recommend similar movies using precomputed vector similarity.
- Display each recommendation as a poster card.
- Fetch posters without relying on TMDB image hosting.
- Use a built-in placeholder poster if no external poster is available.
- Run as a simple FastAPI app with Jinja2 templates.

## Project Structure

```text
movie recomender/
|-- Backend/
|   |-- main.py
|   |-- movie_list.json
|   |-- vectors.csv
|   |-- similarity.pkl
|   |-- data/
|   |   |-- tmdb_5000_movies.csv
|   |   `-- tmdb_5000_credits.csv
|   |-- services/
|   |   |-- recommender.py
|   |   `-- posterfetch.py
|   `-- templates/
|       |-- index.html
|       `-- recommend.html
|-- requirements.txt
|-- .env
`-- README.md
```

## How Recommendation Works

The recommendation system is content-based. That means it recommends movies that have similar metadata and text features to the movie selected by the user.

The original dataset contains information such as:

- Movie title
- Genres
- Keywords
- Overview
- Cast
- Crew/director
- Production information
- Release date
- Rating

During model preparation, important text fields were combined into a single `tag` column. Those tags were converted into numerical vectors, and then a similarity matrix was calculated. The similarity matrix is saved as:

```text
Backend/similarity.pkl
```

When a user searches for a movie:

1. `main.py` receives the selected movie from the HTML form.
2. `Recommend(movie)` in `services/recommender.py` finds that movie in `vectors.csv`.
3. The app gets the selected movie index.
4. It reads similarity scores for that movie from `similarity.pkl`.
5. It sorts movies by highest similarity score.
6. It returns the top recommended movies.
7. For each movie, it adds year, rating, overview, and poster URL.
8. `recommend.html` displays everything in movie cards.

## Important Data Files

### `vectors.csv`

This file contains the movie id, title, and processed tag text used by the recommender. It is used instead of `vectors.pkl` so the app does not break when different pandas versions are installed.

### `movie_list.json`

This file contains all movie titles used by the search box on the homepage. It is used instead of `movie_list.pkl` for better compatibility.

### `similarity.pkl`

This file stores the precomputed similarity matrix. It is large, but it makes recommendations fast because the app does not need to recalculate similarity on every request.

### `tmdb_5000_movies.csv`

This dataset is used to show extra details such as movie overview, release year, and rating.

## Poster Fetching

TMDB poster/image hosting may be blocked in some regions, so this project does not depend on TMDB for poster images.

Poster lookup happens in `Backend/services/posterfetch.py`:

1. Try OMDb, if an `OMDB_API_KEY` is available.
2. Try Wikipedia/Wikimedia PageImages using movie title and release year.
3. Use a built-in SVG placeholder poster if no poster is found.

OMDb is optional. To enable it, add this to `.env`:

```env
OMDB_API_KEY=your_omdb_key_here
```

The app works without this key because Wikipedia and the local placeholder are used as fallbacks.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the App

From the `Backend` folder:

```powershell
cd Backend
python -m uvicorn main:app --reload
```

Open the app:

```text
http://127.0.0.1:8000/
```


## Main Files

### `Backend/main.py`

Creates the FastAPI app, loads the movie title list, renders the homepage, and handles recommendation form submissions.

### `Backend/services/recommender.py`

Loads the vector data, similarity matrix, and movie details. It finds the selected movie, sorts similar movies, builds recommendation cards, and fetches posters in parallel.

### `Backend/services/posterfetch.py`

Handles poster lookup using OMDb, Wikipedia/Wikimedia, and a local placeholder fallback.

### `Backend/templates/index.html`

The homepage UI. It contains the movie search form and datalist suggestions.

### `Backend/templates/recommend.html`

The recommendation result UI. It displays movie cards with posters, years, ratings, titles, and overviews.

## Common Problems

### Posters are missing

Poster fetching depends on external services. If OMDb/Wikipedia cannot find a poster or the network blocks the request, the app shows a built-in placeholder poster so the UI still works.

For better poster results, add an OMDb API key in `.env`:

```env
OMDB_API_KEY=your_omdb_key_here
```

## Tech Stack

- Python
- FastAPI
- Jinja2
- pandas
- scikit-learn
- requests
- TMDB 5000 dataset
- OMDb and Wikipedia/Wikimedia for poster lookup

## Notes

The recommendation model and similarity matrix are already prepared. If you change the dataset or feature engineering logic, you must regenerate `vectors.csv`, `movie_list.json`, and `similarity.pkl`.
