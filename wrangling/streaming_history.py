import logging
import multiprocessing
from typing import Dict, List
import pandas as pd
import json
from dataclasses import dataclass, field
from pathlib import Path
import requests
from utils import TOKEN

# use functools cache properties as the Track attributes are costly
import functools

SPOTIFY_DATA_ROOT = Path(__file__).parents[1] / "data"
DATA_CACHE = SPOTIFY_DATA_ROOT / "cache"
QUERY_BASE_URL = "https://api.spotify.com/v1/"
# how many objects to create in parallel
CONCURRENCY = 16


@dataclass
class SpotifyParser:
    """class to hold an instance of spotify listening history"""

    file_prefix: str = "StreamingHistory"
    num_files: int = 4

    @functools.cached_property
    def raw_listening_history(self) -> List[Dict]:

        streaming_files = []
        for file_num in range(0, self.num_files):
            with open(
                SPOTIFY_DATA_ROOT / f"{self.file_prefix}{file_num}.json",
                encoding="utf-8",
            ) as data_file:
                file_chunk = json.loads(data_file.read())
                streaming_files.extend(file_chunk)
                print(f"reading {len(file_chunk)} records from file {file_num}")

        return streaming_files
    
    @staticmethod
    def _create_track(track: Dict):
        try:
            return Track(**track)
        except IndexError:
            logging.warning(f"cannot fetch track data for {track}")
            return None    

    @functools.cached_property
    def listening_history(self) -> pd.DataFrame:
        # if file is cached, don't recalculate values
        # TODO(sean): create a nicer caching system than manually reading and writing (cache module?)
        if not self._is_cached():
            pool = multiprocessing.Pool(processes=CONCURRENCY)
            records = pool.map(self._create_track, self.raw_listening_history[:10])

            data = pd.DataFrame.from_records(
                [record.__dict__ for record in records]
            ).assign(
                endTime=lambda row: pd.to_datetime(row["endTime"]),
            )

            # cache and return dataframe
            data.to_csv(DATA_CACHE / (self.file_prefix + ".csv"), index=False)
            return data
        else:
            return pd.read_csv(DATA_CACHE / (self.file_prefix + ".csv"))

    def _is_cached(self):
        cached_file = Path(DATA_CACHE / (self.file_prefix + ".csv"))
        return cached_file.is_file()


@dataclass()
class Track:
    """holds characteristics of a track from the Spotify web API"""

    trackName: str
    artistName: str
    endTime: str = None
    msPlayed: int = None
    artist_id: str = field(init=False)
    track_id: str = field(init=False)
    genres: List[str] = field(init=False)

    def __post_init__(self):
        self.artist_id = self._get_artist_id()
        self.track_id = self._get_track_id()
        self.genres = self._get_genres()

    def _get_artist_id(self) -> str:
        res = requests.get(
            url=QUERY_BASE_URL + "search",
            headers={"Authorization": f"Bearer " + TOKEN},
            params={("q", self.artistName), ("type", "artist")},
        )
        # assume the top result is the one we want -- put the faith of God in spotify's search alg
        try:
            return res.json()["artists"]["items"][0]["id"]
        except:
            return None

    def _get_track_id(self) -> str:
        try:
            res = requests.get(
                url=QUERY_BASE_URL + "search",
                headers={"Authorization": f"Bearer " + TOKEN},
                params={("q", self.trackName), ("type", "track")},
            )
            results = res.json()["tracks"]["items"]
            # find top song result for song with the matching artist id
            # TODO(sean): this is pretty slow... find ways to speed up (is artist matching really necessary?)
            return [
                track
                for track in results
                if self.artist_id in [artist["id"] for artist in track["artists"]]
            ][0]["id"]
        except:
            return None

    def _get_genres(self) -> list:
        try:
            return requests.get(
                url=QUERY_BASE_URL + f"artists/{self.artist_id}",
                headers={"Authorization": f"Bearer " + TOKEN},
            ).json()["genres"]
        except:
            return None
