import json
import pandas as pd
from pretty_html_table import build_table

files_with_data = [
    'MyData/StreamingHistory0.json',
    'MyData/StreamingHistory1.json',
    'MyData/StreamingHistory2.json',
    'MyData/StreamingHistory3.json'
    ]

files_with_data = [
    'MyData/sean0.json',
    'MyData/sean1.json',
    'MyData/sean2.json',
    'MyData/sean3.json',
]


def get_data():
    all_data = []
    for file_path in files_with_data:
        with open(file_path, 'r', encoding="utf8") as fh:
            data = fh.read()
        all_data += json.loads(data)
    return all_data


def get_rid_of_skips(data):
    return [song for song in data if song.get('msPlayed') >= 30000]


def get_rid_of_2020(data):
    return [song for song in data if int(song['endTime'].split('-')[0]) > 2020]


def get_most_listened_songs(data):
    total_songs = [item['trackName'] for item in data]
    unique_songs = list(set(total_songs))
    occurences = {song: total_songs.count(song) for song in unique_songs}
    return {k: v for k, v in sorted(occurences.items(), key=lambda item: item[1], reverse=True)}


def print_top(data, n):
    for index, (k, v) in enumerate(data.items()):
        if index == n:
            return
        print(f'{k}: {v}')


def get_most_listened_artist(data):
    total_artists = [item['artistName'] for item in data]
    unique_artists = list(set(total_artists))
    occurences = {song: total_artists.count(song) for song in unique_artists}
    return {k: v for k, v in sorted(occurences.items(), key=lambda item: item[1], reverse=True)}


def main():
    all_my_data = get_data()
    all_my_data = get_rid_of_skips(all_my_data)
    #all_my_data = get_rid_of_2020(all_my_data)

    # songs
    list_songs = get_most_listened_songs(all_my_data)
    songs = pd.DataFrame({"track_name": list_songs.keys(), "listens": list_songs.values()})
    songs['track_name'] = songs['track_name'].apply(lambda x: str(x.encode('ascii', 'ignore').decode()))
    with open('top_songs.html', 'w') as fh:
        fh.write(build_table(songs.head(100), 'blue_light'))



    # artists
    list_artists = get_most_listened_artist(all_my_data)
    artists = pd.DataFrame({"artist_name": list_artists.keys(), "listens": list_artists.values()})
    artists['artist_name'] = artists['artist_name'].apply(lambda x: str(x.encode('ascii', 'ignore').decode()))
    with open('top_artists.html', 'w') as fh:
        fh.write(build_table(artists.head(100), 'blue_light'))


main()
