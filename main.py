import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENTS_ID = "YOUR SPOTIFY CLIENT ID"
SPOTIFY_CLIENT_SECRET = "YOUR SPOTIFY CLIENT SECRET"

user_date = input("Which Year do you want to travel to? Type the date in the format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{user_date}/"

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

all_songs = soup.select("div.o-chart-results-list-row-container ul li ul li h3#title-of-a-story")

song_names = [sub.getText().strip() for sub in all_songs]

# with open("music.txt", mode="w") as file:
#     for sub in song_names:
#         file.write(f"{sub}\n")



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENTS_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = user_date.split("-")[0]
for sub in song_names:
    result = sp.search(q=f"track:{sub} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{sub} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)



