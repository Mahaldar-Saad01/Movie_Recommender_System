from functools import lru_cache
import os
from urllib.parse import quote

from dotenv import load_dotenv
import requests

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")
USER_AGENT = "MovieRecommender/1.0 (local development)"
PLACEHOLDER_IMAGE = "data:image/svg+xml;utf8," + quote(
    """<svg xmlns="http://www.w3.org/2000/svg" width="780" height="1170" viewBox="0 0 780 1170">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#111827"/><stop offset="1" stop-color="#0f172a"/></linearGradient></defs>
<rect width="780" height="1170" fill="url(#g)"/>
<rect x="70" y="80" width="640" height="1010" rx="28" fill="none" stroke="#334155" stroke-width="8"/>
<circle cx="390" cy="440" r="118" fill="#1f2937" stroke="#64748b" stroke-width="10"/>
<path d="M330 390v100l92-50z" fill="#f8fafc"/>
<text x="390" y="705" fill="#f8fafc" font-family="Arial, sans-serif" font-size="54" font-weight="700" text-anchor="middle">Poster</text>
<text x="390" y="770" fill="#94a3b8" font-family="Arial, sans-serif" font-size="34" text-anchor="middle">not found</text>
</svg>"""
)


def _get_json(url, params=None):
    try:
        response = requests.get(
            url,
            params=params,
            headers={"User-Agent": USER_AGENT},
            timeout=3,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {}


@lru_cache(maxsize=512)
def fetch_poster_from_omdb(title, year=None):
    if not OMDB_API_KEY or not title:
        return ""

    params = {"apikey": OMDB_API_KEY, "t": title, "type": "movie"}
    if year and year != "N/A":
        params["y"] = year

    data = _get_json("https://www.omdbapi.com/", params)
    poster = data.get("Poster", "")
    if not poster or poster == "N/A":
        return ""
    return poster


@lru_cache(maxsize=512)
def fetch_poster_from_wikipedia(title, year=None):
    if not title:
        return ""

    searches = [
        f"{title} {year} film" if year and year != "N/A" else "",
        f"{title} film",
        title,
    ]

    for search in [item for item in searches if item]:
        wiki_data = _get_json(
            "https://en.wikipedia.org/w/api.php",
            {
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrsearch": search,
                "gsrlimit": 5,
                "prop": "pageimages",
                "pithumbsize": 780,
                "pilicense": "any",
            },
        )
        pages = wiki_data.get("query", {}).get("pages", {})
        for page in sorted(pages.values(), key=lambda item: item.get("index", 99)):
            thumbnail = page.get("thumbnail", {})
            source = thumbnail.get("source")
            if source:
                return source

    return ""


def fetch_poster(title, year=None):
    return (
        fetch_poster_from_omdb(title, year)
        or fetch_poster_from_wikipedia(title, year)
        or PLACEHOLDER_IMAGE
    )
