from spotify_data.wrangling.streaming_history import SpotifyParser
from spotify_data.utils import GENRE_MAP, Genre, SpotifyVariables

import pandas as pd
from pathlib import Path

DATA_OUTPUT = Path(__file__).parents[2] / "data" / "outputs"


def calculate_genre_percentages(dataset: SpotifyParser.listening_history, cutoff: int = 20):
    """find the percentage of total songs listened to for each genre by day

    dataset: pd.Dataframe output of the SpotifyParser class
    cutoff: how many seconds the song must have been played to count as a listen
    """

    # move this to class dec
    dataset.dropna()
    dataset[SpotifyVariables.GENRES] = (
        dataset[SpotifyVariables.GENRES].str.strip("[]").str.split(",")
    )
    dataset = (
        dataset.dropna()
        .assign(
            genres=lambda row: row[SpotifyVariables.GENRES].apply(lambda x: x[0]),
            endTime=lambda row: pd.to_datetime(row[SpotifyVariables.TIMESTAMP]).dt.date,
        )
        .query(f"{SpotifyVariables.DURATION_PLAYED} > {cutoff*1000}")
        .loc[:, [SpotifyVariables.TIMESTAMP, SpotifyVariables.GENRES]]
        .set_index(SpotifyVariables.TIMESTAMP)
    )
    dataset[SpotifyVariables.GENRES] = (
        dataset[SpotifyVariables.GENRES].str.replace("'", "").map(GENRE_MAP)
    )

    genres = (
        dataset.groupby([SpotifyVariables.TIMESTAMP, SpotifyVariables.GENRES])
        .size()
        .reset_index()
        .set_index(SpotifyVariables.TIMESTAMP)
        .rename(columns={0: "count"})
    )
    totals = pd.DataFrame(dataset.groupby(SpotifyVariables.TIMESTAMP).size()).rename(
        columns={0: "total"}
    )
    dataset = totals.join(genres)
    dataset["percentage"] = dataset["count"] / dataset["total"]
    return dataset


def calculate_rolling_average(dataset: SpotifyParser.listening_history, window: int = 30):
    dataset = calculate_genre_percentages(dataset)
    frames = []
    # TODO(sean): rolling with groupby returned NANs, so slice and parse each genre separately
    # find out why groupby returned all nulls
    for genre in Genre:
        genre_data = dataset[dataset[SpotifyVariables.GENRES] == genre]
        frames.append(
            genre_data.set_index(SpotifyVariables.GENRES, append=True)
            .rolling(window=window, min_periods=1)
            .mean()
        )
    return pd.concat(frames).ffill()


# TODO(sean): either get some sort of API set up to serve files or create an exporter class
def serve_dataset(file_format="str"):
    data = calculate_genre_percentages(SpotifyParser().listening_history).reset_index()
    if file_format == "csv":
        data.to_csv(DATA_OUTPUT / "rolling_average.csv", index=False)
    elif file_format == "json":
        raise NotImplementedError()
        # TODO(sean) implement this...
