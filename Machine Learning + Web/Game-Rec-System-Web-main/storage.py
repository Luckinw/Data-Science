import requests
import pandas as pd
from sqlalchemy import create_engine


def names_list():
    engine = create_engine('sqlite:///game_data.db')
    query = "SELECT name FROM games"
    df = pd.read_sql_query(query, engine)
    names = df['name'].tolist()
    return names


def get_steam_game_link(game_name,):
    # for req in range(num)
    base_url = "https://store.steampowered.com/api/storesearch"
    params = {
        "term": game_name,
        "l": "english",
        "cc": "us"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["total"] > 0:
        game = data["items"][0]
        game_id = game["id"]
        game_link = f"https://store.steampowered.com/app/{game_id}"
        return game_link

    return 'This Game is not published on steam'

