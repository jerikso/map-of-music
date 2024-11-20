from dotenv import load_dotenv
import os
import requests

# Load environment variables from the .env file
load_dotenv()

# Access variables using os.getenv
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_BASE_URL = "https://api.spotify.com/v1"

class AudioFeatures:
    def __init__(self, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature):
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo
        self.duration_ms = duration_ms
        self.time_signature = time_signature
    
    @classmethod
    def fromjson(cls, json):
        return AudioFeatures(
            json["danceability"],
            json["energy"],
            json["key"],
            json["loudness"],
            json["mode"],
            json["speechiness"],
            json["acousticness"],
            json["instrumentalness"],
            json["liveness"],
            json["valence"],
            json["tempo"],
            json["duration_ms"],
            json["time_signature"]
        )
        
    def __repr__(self) -> str:
        return self.__str__()
        
    def __str__(self):
        return f"[Danceability: {self.danceability}, Energy: {self.energy}, Key: {self.key}, Loudness: {self.loudness}, Mode: {self.mode}, Speechiness: {self.speechiness}, Acousticness: {self.acousticness}, Instrumentalness: {self.instrumentalness}, Liveness: {self.liveness}, Valence: {self.valence}, Tempo: {self.tempo}, Duration: {self.duration_ms}, Time Signature: {self.time_signature}]"

class Artist:
    def __init__(self, id, name, genres, popularity):
        self.id = id
        self.name = name
        self.genres = genres
        self.popularity = popularity
        self.audio_features = None
        self.tracks = []
        
    @classmethod
    def fromjson(cls, json):
        id = json["id"]
        name = json["name"]
        genres = json["genres"]
        popularity = json["popularity"]
        return cls(id, name, genres, popularity)
    
    def set_audio_features(self, audio_features):
        self.audio_features = audio_features
    
    def set_tracks(self, tracks):
        self.tracks = tracks
        
    def __str__(self):
        return f"{self.name} is a {', '.join(self.genres)} artist with a popularity of {self.popularity}"
    
class Track:
    def __init__(self, id, name, artist, album, release_date, popularity):
        self.id = id
        self.name = name
        self.artist = artist
        self.album = album
        self.release_date = release_date
        self.popularity = popularity
        self.audio_features = None
        
    def set_audio_features(self, audio_features):
        self.audio_features = audio_features
    
    @classmethod
    def fromjson(cls, json):
        artist = json["artists"][0]["name"]
        name = json["name"]
        popularity = json["popularity"]
        id = json["id"]
        release_date = json["album"]["release_date"]
        album = json["album"]["name"]
        return cls(id, name, artist, album, release_date, popularity)
        
    def __str__(self):
        return f"{self.name} by {self.artist} from the album {self.album} released on {self.release_date} with a popularity of {self.popularity}"
        
class AccessToken:
    def __init__(self, access_token, expires_in):
        self.access_token = access_token
        self.expires_in = expires_in

    def __str__(self):
        return f"Access Token: {self.access_token}, Expires In: {self.expires_in}"

class Album:
    def __init__(self, id, name, artist, release_date, total_tracks):
        self.id = id
        self.name = name
        self.artist = artist
        self.release_date = release_date
        self.total_tracks = total_tracks
        
    @classmethod
    def fromjson(cls, json):
        id = json["id"]
        name = json["name"]
        artist = json["artists"][0]["name"]
        release_date = json["release_date"]
        total_tracks = json["total_tracks"]
        return cls(id, name, artist, release_date, total_tracks)
        
    def __str__(self):
        return f"{self.name} by {self.artist} released on {self.release_date} with a total of {self.total_tracks} tracks"
    
class ItemType:
    ALBUM = "album"
    ARTIST = "artist"
    TRACK = "track"

class SpotifyClient:
    def __init__(self):
        self.access_token = self.get_access_token()

    def make_request(self, endpoint, params=None):
        # Make a request to the Spotify API
        
        response = requests.get(
            f"{SPOTIFY_BASE_URL}/{endpoint}",
            headers={
                "Authorization": f"Bearer {self.access_token.access_token}"
            },
            params=params
        )
        if response.status_code != 200:
            raise Exception(f"Failed to make request to {SPOTIFY_BASE_URL}/{endpoint} with status code {response.status_code}")
        return response.json()
        
    def get_access_token(self):
        # Make a request to the Spotify API to get an access token
        endpoint = "https://accounts.spotify.com/api/token"
        response = requests.post(
            endpoint,
            data={
                "grant_type": "client_credentials"
            },
            auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
        )
        response_data = response.json()

        access_token = response_data["access_token"]
        expires_in = response_data["expires_in"]

        return AccessToken(access_token, expires_in)

    def search(self, q, types, limit=20, offset=0):
        # Make a request to the Spotify API to search for a track
        endpoint = "search"
        params = {
            "q": q,
            "type": types,
            "limit": limit,
            "offset": offset
        }
        response_data = self.make_request(endpoint, params)
        return response_data

    def get_track(self, track_id):
        # Make a request to the Spotify API to get a track by its ID
        endpoint = f"tracks/{track_id}"
        response_data = self.make_request(endpoint)
        return Track.fromjson(response_data)

    def get_audio_features(self, track_id):
        endpoint = f"audio-features/{track_id}"
        response_data = self.make_request(endpoint)
        return AudioFeatures.fromjson(response_data)
    
    def get_multiple_audio_features(self, track_ids):
        endpoint = "audio-features"
        params = {
            "ids": ",".join(track_ids)
        }
        response_data = self.make_request(endpoint, params)
        return [AudioFeatures.fromjson(audio_features) for audio_features in response_data["audio_features"]]
    
    def search_tracks(self, q):
        response_data = self.search(q, ItemType.TRACK)
        tracks = response_data["tracks"]["items"]
        list_of_tracks = [Track.fromjson(track) for track in tracks]
        
        return list_of_tracks
        # fetch audio features in batches of 100
    
    def get_artists_in_genre(self, genre, limit=50):
        # if there are more than 50 artists in the genre, we can't get all of them, get in batches of 50
        
        for i in range(0, limit, 50):
            print(f"Fetching artists in the genre {genre} from {i} to {i+50}")
            q = f'genre:"{genre}"'
            # if fetching last batch, limit to the remaining artists
            if i + 50 <= limit:
                search_limit = 50
            else:
                search_limit = limit - i
                
            response_data = self.search(q, ItemType.ARTIST, limit=search_limit, offset=i)
            artists = response_data["artists"]["items"]
            print(f"Found {len(artists)} artists in the genre {genre}")
            return [Artist.fromjson(artist) for artist in artists]
        
        q = f'genre:"{genre}"'
        response_data = self.search(q, ItemType.ARTIST, limit=limit)
        print(response_data)
        artists = response_data["artists"]["items"]
        print(f"Found {len(artists)} artists in the genre {genre}")
        return [Artist.fromjson(artist) for artist in artists]
    
    def get_albums_by_artist(self, artist_id):
        endpoint = f"artists/{artist_id}/albums"
        response_data = self.make_request(endpoint)
        albums = response_data["items"]
        return [Album.fromjson(album) for album in albums]
    
    def get_tracks_in_album(self, album_id):
        endpoint = f"albums/{album_id}/tracks"
        response_data = self.make_request(endpoint)
        tracks = response_data["items"]
        track_ids = [track["id"] for track in tracks]
        return self.get_multiple_tracks(track_ids)
    
    def get_multiple_tracks(self, track_ids):
        endpoint = "tracks"
        params = {
            "ids": ",".join(track_ids)
        }
        response_data = self.make_request(endpoint, params)
        return [Track.fromjson(track) for track in response_data["tracks"]]
    
    def get_audio_features_for_tracks(self, tracks):
        track_ids = [track.id for track in tracks]
        
        for i in range(0, len(track_ids), 100):
            print(f"Fetching audio features for tracks {i} to {i+100}")
            batch_ids = track_ids[i:i+100]
            audio_features = self.get_multiple_audio_features(batch_ids)
            for i, track in enumerate(tracks[i:i+100]):
                track.set_audio_features(audio_features[i])
        
        return tracks
    
    def get_tracks_by_artist(self, artist_id):
        # get albums and then get tracks from each album
        albums = self.get_albums_by_artist(artist_id)
        tracks = []
        for album in albums:
            album_tracks = self.get_tracks_in_album(album.id)
            tracks.extend(album_tracks)
        return tracks

    def aggregate_audio_features(self, tracks):
        aggregate_features = {
            "danceability": 0,
            "energy": 0,
            "key": 0,
            "loudness": 0,
            "mode": 0,
            "speechiness": 0,
            "acousticness": 0,
            "instrumentalness": 0,
            "liveness": 0,
            "valence": 0,
            "tempo": 0,
            "duration_ms": 0,
            "time_signature": 0
        }
        
        for track in tracks:
            audio_features = track.audio_features
            aggregate_features["danceability"] += audio_features.danceability
            aggregate_features["energy"] += audio_features.energy
            aggregate_features["key"] += audio_features.key
            aggregate_features["loudness"] += audio_features.loudness
            aggregate_features["mode"] += audio_features.mode
            aggregate_features["speechiness"] += audio_features.speechiness
            aggregate_features["acousticness"] += audio_features.acousticness
            aggregate_features["instrumentalness"] += audio_features.instrumentalness
            aggregate_features["liveness"] += audio_features.liveness
            aggregate_features["valence"] += audio_features.valence
            aggregate_features["tempo"] += audio_features.tempo
            aggregate_features["duration_ms"] += audio_features.duration_ms
            aggregate_features["time_signature"] += audio_features.time_signature
        
        num_tracks = len(tracks)
        for key in aggregate_features:
            aggregate_features[key] /= num_tracks
        
        return AudioFeatures(
            aggregate_features["danceability"],
            aggregate_features["energy"],
            aggregate_features["key"],
            aggregate_features["loudness"],
            aggregate_features["mode"],
            aggregate_features["speechiness"],
            aggregate_features["acousticness"],
            aggregate_features["instrumentalness"],
            aggregate_features["liveness"],
            aggregate_features["valence"],
            aggregate_features["tempo"],
            aggregate_features["duration_ms"],
            aggregate_features["time_signature"]
        )
        
    def get_artist_and_tracks_by_genre(self, genre, artist_limit=50):
        artists = self.get_artists_in_genre(genre, artist_limit)

        for artist in artists:
            artist_tracks = self.get_tracks_by_artist(artist.id)
            self.get_audio_features_for_tracks(artist_tracks)
            # aggregate audio features for the artist
            audio_features = self.aggregate_audio_features(artist_tracks)
            artist.set_audio_features(audio_features)
            artist.set_tracks(artist_tracks)
            
        return artists
    