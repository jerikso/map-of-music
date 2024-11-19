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
        album = json["album"]["name"]
        artist = json["artists"][0]["name"]
        name = json["name"]
        release_date = json["album"]["release_date"]
        popularity = json["popularity"]
        id = json["id"]
        return cls(id, name, artist, album, release_date, popularity)
        
    def __str__(self):
        return f"{self.name} by {self.artist} from the album {self.album} released on {self.release_date} with a popularity of {self.popularity}"
        
class AccessToken:
    def __init__(self, access_token, expires_in):
        self.access_token = access_token
        self.expires_in = expires_in

    def __str__(self):
        return f"Access Token: {self.access_token}, Expires In: {self.expires_in}"

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

    def search(self, q, types):
        # Make a request to the Spotify API to search for a track
        endpoint = "search"
        params = {
            "q": q,
            "type": types
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
    
    def search_tracks(self, q):
        response_data = self.search(q, ItemType.TRACK)
        tracks = response_data["tracks"]["items"]
        list_of_tracks = [Track.fromjson(track) for track in tracks]
        for track in list_of_tracks:
            track.set_audio_features(self.get_audio_features(track.id))
        return list_of_tracks