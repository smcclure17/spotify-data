from enum import Enum
from typing import Dict
from functools import total_ordering
import spotipy
import json

# TODO(sean): use the spotipy secrets manager instead of this
secrets = json.load(open("secrets.json"))["secrets"]
TOKEN = spotipy.util.prompt_for_user_token(
    username=secrets["username"],
    scope=secrets["scope"],
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    redirect_uri=secrets["redirect_uri"],
)


class SpotifyVariables(str, Enum):
    GENRES = ("genres",)
    TIMESTAMP = ("endTime",)
    DURATION_PLAYED = ("msPlayed",)
    TRACK_NAME = ("trackName",)
    ARTIST_NAME = ("artistName",)
    TRACK_ID = ("track_id",)
    ARTIST_ID = "artist_id"


@total_ordering
class Genre(str, Enum):
    HIP_HOP = ("hip-hop/rap",)
    K_POP = ("k-pop",)
    HOUSE_EDM = ("house/edm",)
    RNB = ("r&b",)
    POP = ("pop",)
    ROCK_ALTERNATIVE = ("rock/alternative",)
    AFRO_LATIN = ("afro/latin",)
    MISC = ("miscellaneous",)

    # must define an ordering operation (__eq__ is handled by Enum automatically)
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value  #  pylint: disable=comparison-with-callable
        return NotImplemented


GENRE_MAP: Dict[str, Genre] = {
    "album rock": Genre.ROCK_ALTERNATIVE,
    "australian rock": Genre.ROCK_ALTERNATIVE,
    "canadian rock": Genre.ROCK_ALTERNATIVE,
    "christian alternative rock": Genre.ROCK_ALTERNATIVE,
    "modern rock": Genre.ROCK_ALTERNATIVE,
    "modern alternative rock": Genre.ROCK_ALTERNATIVE,
    "garage rock": Genre.ROCK_ALTERNATIVE,
    "alternative rock": Genre.ROCK_ALTERNATIVE,
    "electro house": Genre.HOUSE_EDM,
    "house": Genre.HOUSE_EDM,
    "brostep": Genre.HOUSE_EDM,
    "bass house": Genre.HOUSE_EDM,
    "edmonton indie": Genre.HOUSE_EDM,
    "dubstep": Genre.HOUSE_EDM,
    "edm": Genre.HOUSE_EDM,
    "dutch edm": Genre.HOUSE_EDM,
    "deep house": Genre.HOUSE_EDM,
    "folk-pop": Genre.K_POP,
    "k-indie": Genre.K_POP,
    "k-rap": Genre.HIP_HOP,
    "korean ost": Genre.K_POP,
    "korean r&b": Genre.RNB,
    "k-pop boy group": Genre.K_POP,
    "k-pop girl group": Genre.K_POP,
    "k-pop": Genre.K_POP,
    "korean dream pop": Genre.POP,
    "art pop": Genre.POP,
    "australian pop": Genre.POP,
    "hip pop": Genre.POP,
    "pop r&b": Genre.RNB,
    "indie pop rap": Genre.HIP_HOP,
    "dance pop": Genre.POP,
    "modern dream pop": Genre.POP,
    "social media pop": Genre.POP,
    "german pop": Genre.POP,
    "canadian pop": Genre.POP,
    "colombian pop": Genre.POP,
    "chill pop": Genre.POP,
    "electropop": Genre.POP,
    "classic city pop": Genre.POP,
    "la pop": Genre.POP,
    "nyc pop": Genre.POP,
    "pop rap": Genre.HIP_HOP,
    "pop": Genre.POP,
    "desi pop": Genre.POP,
    "moldovan pop": Genre.POP,
    "bedroom pop": Genre.POP,
    "barbadian pop": Genre.POP,
    "chamber pop": Genre.POP,
    "latin pop": Genre.POP,
    "chinese idol pop": Genre.POP,
    "indie pop": Genre.POP,
    "dutch pop": Genre.POP,
    "modern indie pop": Genre.POP,
    "afropop": Genre.POP,
    "indie poptimism": Genre.POP,
    "french indie pop": Genre.POP,
    "pop punk": Genre.POP,
    "alternative r&b": Genre.RNB,
    "neo mellow": Genre.RNB,
    "canadian contemporary r&b": Genre.RNB,
    "chill r&b": Genre.RNB,
    "r&b en espanol": Genre.RNB,
    "indie hip hop": Genre.HIP_HOP,
    "melodic rap": Genre.HIP_HOP,
    "dfw rap": Genre.HIP_HOP,
    "atl hip hop": Genre.HIP_HOP,
    "atl trap": Genre.HIP_HOP,
    "country rap": Genre.HIP_HOP,
    "jazz rap": Genre.HIP_HOP,
    "ohio hip hop": Genre.HIP_HOP,
    "indonesian hip hop": Genre.HIP_HOP,
    "hip hop": Genre.HIP_HOP,
    "detroit trap": Genre.HIP_HOP,
    "lgbtq+ hip hop": Genre.HIP_HOP,
    "conscious hip hop": Genre.HIP_HOP,
    "canadian hip hop": Genre.HIP_HOP,
    "emo rap": Genre.HIP_HOP,
    "philly rap": Genre.HIP_HOP,
    "bass trap": Genre.HIP_HOP,
    "aesthetic rap": Genre.HIP_HOP,
    "east coast hip hop": Genre.HIP_HOP,
    "chicago rap": Genre.HIP_HOP,
    "hardcore hip hop": Genre.HIP_HOP,
    "asian american hip hop": Genre.HIP_HOP,
    "australian hip hop": Genre.HIP_HOP,
    "brooklyn drill": Genre.HIP_HOP,
    "dark trap": Genre.HIP_HOP,
    "north carolina hip hop": Genre.HIP_HOP,
    "uk hip hop": Genre.HIP_HOP,
    "nottingham hip hop": Genre.HIP_HOP,
    "trap soul": Genre.HIP_HOP,
    "cali rap": Genre.HIP_HOP,
    "kentucky hip hop": Genre.HIP_HOP,
    "florida rap": Genre.HIP_HOP,
    "meme rap": Genre.HIP_HOP,
    "canadian old school hip hop": Genre.HIP_HOP,
    "ghanaian hip hop": Genre.HIP_HOP,
    "alternative hip hop": Genre.HIP_HOP,
    "nyc rap": Genre.HIP_HOP,
    "hawaiian hip hop": Genre.HIP_HOP,
    "new york drill": Genre.HIP_HOP,
    "trap": Genre.HIP_HOP,
    "rap": Genre.HIP_HOP,
    "dutch hip hop": Genre.HIP_HOP,
    "boston hip hop": Genre.HIP_HOP,
    "chicago drill": Genre.HIP_HOP,
    "houston rap": Genre.HIP_HOP,
    "bronx hip hop": Genre.HIP_HOP,
    "new jersey rap": Genre.HIP_HOP,
    "baton rouge rap": Genre.HIP_HOP,
    "miami hip hop": Genre.HIP_HOP,
    "detroit hip hop": Genre.HIP_HOP,
    "dmv rap": Genre.HIP_HOP,
    "philly drill": Genre.HIP_HOP,
    "alabama rap": Genre.HIP_HOP,
    "arkansas hip hop": Genre.HIP_HOP,
    "underground hip hop": Genre.HIP_HOP,
    "deep underground hip hop": Genre.HIP_HOP,
    "new jersey underground rap": Genre.HIP_HOP,
    "dirty south rap": Genre.HIP_HOP,
    "gangster rap": Genre.HIP_HOP,
    "chinese hip hop": Genre.HIP_HOP,
    "viral rap": Genre.HIP_HOP,
    "memphis hip hop": Genre.HIP_HOP,
}
