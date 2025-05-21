import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAWG_API_KEY")
URL = "https://api.rawg.io/api/games"

def fetch_games(page=1, page_size=40):
    params = {
        "key": API_KEY,
        "page": page,
        "page_size": page_size,
        "platforms": 1
    }
    response = requests.get(URL, params=params)
    response.raise_for_status()
    return response.json()

def extract_data(pages=3):
    all_games = []
    for page in range(1, pages + 1):
        data = fetch_games(page)
        for game in data["results"]:
            all_games.append({
                "nombre": game["name"],
                "fecha_publicacion": game["released"],
                "rating": game["rating"],
                "ratings_count": game["ratings_count"],
                "generos": [g["name"] for g in game["genres"]],
                "tags": [t["name"] for t in game["tags"] if t.get("language") in ["eng", "spa"]],
                "metacritic": game.get("metacritic"),
                "plataformas": [p["platform"]["name"] for p in game["platforms"]],
                "usuarios_interesados": game["added"],
            })
    return pd.DataFrame(all_games)

if __name__ == "__main__":
    df = extract_data(pages=10)
    df.to_csv("data/steam_sample.csv", index=False)
    print("Datos guardados en steam_sample.csv")