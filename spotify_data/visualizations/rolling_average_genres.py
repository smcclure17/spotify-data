from spotify_data.datasets.rolling_average import calculate_rolling_average
from spotify_data.wrangling.streaming_history import SpotifyParser
from spotify_data.utils import SpotifyVariables
import pandas as pd

pd.options.plotting.backend = "plotly"

dataset = calculate_rolling_average(SpotifyParser().listening_history, window=7)

# forward fill here to fill gaps in the line graphs
# not entirely sure why there are gaps --
# TODO(sean): check to make sure the rolling avg function is actually working as expected
dataset_wide = dataset.pivot_table(
    columns=SpotifyVariables.GENRES,
    index=[SpotifyVariables.TIMESTAMP],
    values="percentage",
).ffill()
dataset_wide.plot(labels=dict(value="percentage of total listening")).show()
