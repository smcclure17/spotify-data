import pandas as pd
from pretty_html_table import build_table
from typing import List, Dict
from spotify_data.wrangling.streaming_history import SpotifyParser
from pathlib import Path

DATA_OUTPUTS = Path(__file__).parents[2] / "data" / "outputs"


def run_summary():
    all_my_data = get_rid_of_skips(SpotifyParser().raw_listening_history)

    list_songs = get_most_listened(all_my_data, key_to_parse="trackName")
    export_to_table(list_songs, variable="track")
    list_artists = get_most_listened(all_my_data, "artistName")
    export_to_table(list_artists, "artist")


def get_rid_of_skips(data: List[Dict]) -> List[Dict]:
    return [song for song in data if song.get("msPlayed") >= 30000]


def get_rid_of_2020(data: List[Dict]) -> List[Dict]:
    return [song for song in data if int(song["endTime"].split("-")[0]) > 2020]


def get_most_listened(data: List[Dict], key_to_parse: str) -> Dict:
    total = [item[key_to_parse] for item in data]
    unique = set(total)
    occurences = {song: total.count(song) for song in unique}
    return {k: v for k, v in sorted(occurences.items(), key=lambda item: item[1], reverse=True)}


def export_to_table(data: Dict[str, int], variable: str) -> None:
    if variable not in ("track", "artist"):
        raise ValueError(
            f"{variable} is not a valid variable option. Please specify either 'track' or 'artist'"
        )

    output = pd.DataFrame({f"{variable}_name": data.keys(), "listens": data.values()})
    with open(DATA_OUTPUTS / f"top_{variable}s.html", "w") as fh:
        fh.write(build_table(output.head(100), "blue_light"))


def print_top(data: Dict[str, int], n: int):
    for index, (k, v) in enumerate(data.items()):
        if index == n:
            return
        print(f"{k}: {v}")
