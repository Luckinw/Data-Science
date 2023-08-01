import sqlite3
import pickle
import pandas as pd
from storage import get_steam_game_link

conn = sqlite3.connect('game_data.db')
query = "SELECT appid,header_image FROM games"
df = pd.read_sql_query(query, conn)

games = pickle.load(open("./recommendation/game_data.pkl", 'rb'))
similarity = pickle.load(open("./recommendation/similarity.pkl", 'rb'))

def recommend(game, num):
    recommended_list = []
    if game in games['name'].values:
        index = games[games['name'] == game].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        if num >= len(distance):
            for i in distance[1:len(distance)-1]:
                game = games.iloc[i[0]][['name', 'appid']]
                link = get_steam_game_link(game['name'])
                appid = game['appid']
                header_image = df.loc[df['appid'] == appid, 'header_image'].iloc[0]
                recommended_list.append((game['name'], link, header_image))
               
        elif num < len(distance):
            for i in distance[1:num+1]:
                game = games.iloc[i[0]][['name', 'appid']]
                link = get_steam_game_link(game['name'])
                appid = game['appid']
                header_image = df.loc[df['appid'] == appid, 'header_image'].iloc[0]
                recommended_list.append((game['name'], link, header_image))
               
        else:
            return 'Game is not in the database'
    return recommended_list

conn.close()
