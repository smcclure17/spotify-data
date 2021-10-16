import pandas as pd
from pretty_html_table import build_table
from typing import List, Dict
from spotify_data.wrangling.streaming_history import SpotifyParser
from pathlib import Path

SPOTIFY_DATA_ROOT = Path(__file__).parents[2] / "data" / "outputs"


def run_summary():
    all_my_data = get_rid_of_skips(SpotifyParser().raw_listening_history)

    # songs
    list_songs = get_most_listened_songs(all_my_data)
    songs = pd.DataFrame({"track_name": list_songs.keys(), "listens": list_songs.values()})
    songs["track_name"] = songs["track_name"].apply(
        lambda x: str(x.encode("ascii", "ignore").decode())
    )
    with open(SPOTIFY_DATA_ROOT / "top_songs.html", "w") as fh:
        fh.write(build_table(songs.head(100), "blue_light"))

    # artists
    list_artists = get_most_listened_artist(all_my_data)
    artists = pd.DataFrame({"artist_name": list_artists.keys(), "listens": list_artists.values()})
    artists["artist_name"] = artists["artist_name"].apply(
        lambda x: str(x.encode("ascii", "ignore").decode())
    )
    with open(SPOTIFY_DATA_ROOT / "top_artists.html", "w") as fh:
        fh.write(build_table(artists.head(100), "blue_light"))


def get_rid_of_skips(data: List[Dict]) -> List[Dict]:
    return [song for song in data if song.get("msPlayed") >= 30000]


def get_rid_of_2020(data: List[Dict]) -> List[Dict]:
    return [song for song in data if int(song["endTime"].split("-")[0]) > 2020]


def get_most_listened_songs(data) -> Dict:
    total_songs = [item["trackName"] for item in data]
    unique_songs = list(set(total_songs))
    occurences = {song: total_songs.count(song) for song in unique_songs}
    return {k: v for k, v in sorted(occurences.items(), key=lambda item: item[1], reverse=True)}


def get_most_listened_artist(data) -> Dict:
    total_artists = [item["artistName"] for item in data]
    unique_artists = list(set(total_artists))
    occurences = {song: total_artists.count(song) for song in unique_artists}
    return {k: v for k, v in sorted(occurences.items(), key=lambda item: item[1], reverse=True)}
