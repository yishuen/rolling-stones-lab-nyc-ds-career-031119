import csv
import json
import re
import spotipy
import spotipy.oauth2 as oauth2

def readCSV(file_name):
    with open(file_name) as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]
        return data

top500AlbumData = readCSV('data.csv')

credentials = oauth2.SpotifyClientCredentials(
        client_id="12d4e8c7a8934e60ab3ab3e645a19a6b",
        client_secret="99c6e9ce677440a89558bd5fc52c4a3b")

token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

def find_album_id(album_name, artist_name, x):
    album = spotify.search(q='album:' + album_name, type='album')['albums']['items'][0]
    spotify_artist_name = album['artists'][0]['name']
    id = album['id']
    return id

def createListOfAlbumTracks(albumData):
    all_track_data = []
    x = 0
    for album in albumData:
        album_id = find_album_id(album['album'], album['artist'], x)
        x += 1
        tracks = [track['name'] for track in spotify.album_tracks(album_id)['items']]
        all_track_data.append({'artist': album['artist'], 'album':album['album'], 'tracks': tracks})
    return all_track_data

album_track_data = createListOfAlbumTracks(top500AlbumData)

def writeToCSV(list_of_dicts):
    with open('track_data.csv', 'w') as csvfile:
        fieldnames = ['artist', 'album', 'tracks']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in list_of_dicts:
            writer.writerow(row)

def writeToJSON(list_of_dicts):
    with open('track_data.json', 'w') as jsonFile:
        json.dump(list_of_dicts, jsonFile)
        print("Wrote JSON to file!")

# writeToCSV(album_track_data)
writeToJSON(album_track_data)
