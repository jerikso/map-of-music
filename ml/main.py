import similarity
import spotify
import databaseHandler
import pandas as pd
import numpy as np

def create_similarity_dataset_from_search(tracks, similarity_metric):
    # Get a list of tracks
    feature_vectors = [feature_vector_from_track(track) for track in tracks]
    # Calculate the similarity between each pair of tracks
    similarities = similarity.calculate_similarities(similarity_metric, feature_vectors)
    
    # create one pandas dataframe for tracks, and one for similarities
    track_data = pd.DataFrame([[track.id, track.name, track.artist, track.album, track.release_date, track.popularity] for track in tracks], columns=["id", "name", "artist", "album", "release_date", "popularity"])
    similarity_data = pd.DataFrame([[track1, track2, similarity] for (track1, track2), similarity in similarities.items()], columns=["track1", "track2", "similarity"])
    
    # change the index to track id
    track_data.set_index("id", inplace=True)
    similarity_data["track1"] = similarity_data["track1"].apply(lambda x: tracks[x].id)
    similarity_data["track2"] = similarity_data["track2"].apply(lambda x: tracks[x].id)
    
    return track_data, similarity_data

def feature_vector_from_track(track):
    # Create a feature vector from a track
    feature_vector = np.array([
        track.audio_features.danceability,
        track.audio_features.energy,
        track.audio_features.key,
        track.audio_features.loudness,
        track.audio_features.mode,
        track.audio_features.speechiness,
        track.audio_features.acousticness,
        track.audio_features.instrumentalness,
        track.audio_features.liveness,
        track.audio_features.valence,
        track.audio_features.tempo,
        track.audio_features.duration_ms
    ])
    return feature_vector


def track_to_dict(track):
    # Flatten the track's attributes into a dictionary
    properties = {
        "id": track.id,
        "name": track.name,
        "artist": track.artist,
        "album": track.album,
        "release_date": track.release_date,
        "popularity": track.popularity,
        # Flatten the audio_features map into individual properties
        "danceability": track.audio_features.danceability,
        "energy": track.audio_features.energy,
        "key": track.audio_features.key,
        "loudness": track.audio_features.loudness,
        "mode": track.audio_features.mode,
        "speechiness": track.audio_features.speechiness,
        "acousticness": track.audio_features.acousticness,
        "instrumentalness": track.audio_features.instrumentalness,
        "liveness": track.audio_features.liveness,
        "valence": track.audio_features.valence,
        "tempo": track.audio_features.tempo,
        "duration_ms": track.audio_features.duration_ms,
        "time_signature": track.audio_features.time_signature
    }

    # Verify that all values are primitive types (and not nested)
    for key, value in properties.items():
        if isinstance(value, dict):  # If any value is a dictionary, it's not allowed
            raise ValueError(f"Property '{key}' contains a nested map, which is not allowed in Neo4j.")
    
    return properties
        
# Usage:
if __name__ == "__main__":
    client = spotify.SpotifyClient()
    tracks = client.search_tracks("Porcupine Tree")
    track_data, similarity_data = create_similarity_dataset_from_search(tracks, similarity.cosine_similarity)
    
    # write the data to the database
    driver = databaseHandler.get_driver()
    for track in tracks:
        properties = track_to_dict(track)
        databaseHandler.create_node(driver, "Track", properties)
        
    for index, row in similarity_data.iterrows():
        databaseHandler.create_relationship(driver, row["track1"], row["track2"], "COSINE", {"similarity": row["similarity"]})