from typing import Dict
from pretty_html_table import build_table
from pathlib import Path

from spotify_data.datasets import spotify_summaries as summary
from spotify_data.wrangling.streaming_history import SpotifyParser

DATA_OUTPUTS = Path(__file__).parents[2] / "data" / "outputs"


def export_summary_tables() -> None:
    """build html tables of users most listened songs and artists"""
    all_my_data = summary.get_rid_of_skips(SpotifyParser().raw_listening_history)

    list_songs = summary.get_most_listened(all_my_data, key_to_parse="trackName")
    create_export_table(list_songs, variable="track")

    list_artists = summary.get_most_listened(all_my_data, key_to_parse="artistName")
    create_export_table(list_artists, variable="artist")


def create_export_table(data: Dict[str, int], variable: str) -> None:
    output = summary.create_summary_dataframe(data, variable=variable)
    with open(DATA_OUTPUTS / f"top_{variable}s.html", "w") as fh:
        fh.write(build_table(output.head(100), "blue_light"))
