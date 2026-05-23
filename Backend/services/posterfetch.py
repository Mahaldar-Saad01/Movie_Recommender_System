from dotenv import load_dotenv
import os
load_dotenv()
import requests
import json

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

url = f"https://api.themoviedb.org/3/movie/5/images?api_key={API_KEY}"

try:
    response = requests.get(url, timeout=10)

    print("Status:", response.status_code)
    print("URL:", response.url)

    try:
        print(json.dumps(response.json(), indent=4))
    except:
        print(response.text)

except Exception as e:
    print("ERROR:", e)


# def fetch_poster(movie_id):
#     API_KEY = os.getenv("API_KEY")
#     url=https://api.themoviedb.org/3/movie/{movie_id}/images?api_key=API_KEY
