import pandas as pd
from typing import List, Dict


def get_rid_of_skips(data: List[Dict]) -> List[Dict]:
    return [song for song in data if song.get("msPlayed") >= 30000]


def get_rid_of_2020(data: List[Dict]) -> List[Dict]:
    return [song for song in data if int(song["endTime"].split("-")[0]) > 2020]


def get_most_listened(data: List[Dict], key_to_parse: str) -> Dict:
    total = [item[key_to_parse] for item in data]
    unique = set(total)
    occurences = {song: total.count(song) for song in unique}
    return {k: v for k, v in sorted(occurences.items(), key=lambda item: item[1], reverse=True)}


def create_summary_dataframe(data: Dict[str, int], variable: str) -> None:
    if variable not in ("track", "artist"):
        raise ValueError(
            f"{variable} is not a valid variable option. Please specify either 'track' or 'artist'"
        )
    return pd.DataFrame({f"{variable}_name": data.keys(), "listens": data.values()})


def print_top(data: Dict[str, int], n: int):
    for index, (k, v) in enumerate(data.items()):
        if index == n:
            return
        print(f"{k}: {v}")
