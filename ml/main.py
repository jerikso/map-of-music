import similarity
import spotify
import databaseHandler
import pandas as pd
import numpy as np
from tqdm import tqdm

def create_similarity_dataset_from_artists(artists, similarity_metric):
    # Get a list of tracks
    feature_vectors = [feature_vector_from_audio_features(artist.audio_features) for artist in artists]
    
    # Normalize the feature vectors
    feature_vectors = np.array(feature_vectors)
    mean = np.mean(feature_vectors, axis=0)
    std = np.std(feature_vectors, axis=0)
    feature_vectors = (feature_vectors - mean) / std
    
    # Calculate the similarity between each pair of tracks
    similarities = similarity.calculate_similarities(similarity_metric, feature_vectors)
    
    print(similarities)
    # create one pandas dataframe for tracks, and one for similarities
    artist_data = pd.DataFrame([[artist.id, artist.name, artist.popularity, artist.genres] for artist in artists], columns=["id", "name", "popularity", "genres"])
    similarity_data = pd.DataFrame([[artist1, artist2, similarity] for (artist1, artist2), similarity in similarities.items()], columns=["artist1", "artist2", "similarity"])
    
    # change the index to track id
    artist_data.set_index("id", inplace=True)
    similarity_data["artist1"] = similarity_data["artist1"].apply(lambda x: artists[x].id)
    similarity_data["artist2"] = similarity_data["artist2"].apply(lambda x: artists[x].id)
    
    print(similarity_data)
    
    return artist_data, similarity_data

def feature_vector_from_audio_features(audio_features):
    # Create a feature vector from a track
    feature_vector = np.array([
        audio_features.danceability,
        audio_features.energy,
        audio_features.key,
        audio_features.loudness,
        audio_features.mode,
        audio_features.speechiness,
        audio_features.acousticness,
        audio_features.instrumentalness,
        audio_features.liveness,
        audio_features.valence,
        audio_features.tempo,
        audio_features.duration_ms
    ])
    return feature_vector


def artist_to_dict(artist):
    # Convert an artist object to a dictionary
    properties = {
        "id": artist.id,
        "name": artist.name,
        "popularity": artist.popularity,
        "genres": artist.genres,
        "audio_features_danceability": artist.audio_features.danceability,
        "audio_features_energy": artist.audio_features.energy,
        "audio_features_key": artist.audio_features.key,
        "audio_features_loudness": artist.audio_features.loudness,
        "audio_features_mode": artist.audio_features.mode,
        "audio_features_speechiness": artist.audio_features.speechiness,
        "audio_features_acousticness": artist.audio_features.acousticness,
        "audio_features_instrumentalness": artist.audio_features.instrumentalness,
        "audio_features_liveness": artist.audio_features.liveness,
        "audio_features_valence": artist.audio_features.valence,
        "audio_features_tempo": artist.audio_features.tempo,
        "audio_features_duration_ms": artist.audio_features.duration_ms
    }

    # Verify that all values are primitive types (and not nested)
    for key, value in properties.items():
        if isinstance(value, dict):  # If any value is a dictionary, it's not allowed
            raise ValueError(f"Property '{key}' contains a nested map, which is not allowed in Neo4j.")
    
    return properties

def write_artist_to_database(driver, artist):
    # Write an artist to the database
    properties = artist_to_dict(artist)
    
    artist_properties = {k: v for k, v in properties.items() if k != "genres"}
    databaseHandler.create_node(driver, "Artist", artist_properties)
    # for each genre, create a node, connect it to the artist
    for genre in artist.genres:
        databaseHandler.create_node(driver, "Genre", {"name": genre, "id": genre})
        databaseHandler.create_relationship(driver, artist.id, genre, "HAS_GENRE", {})

        
if __name__ == "__main__":
    client = spotify.SpotifyClient()
    artists = client.get_artist_and_tracks_by_genre("prog metal", 30)
    artist_data, similarity_data = create_similarity_dataset_from_artists(artists, similarity.cosine_similarity)
    
    
    # write the data to the database
    driver = databaseHandler.get_driver()
    
    print("Writing artists...")
    for artist in tqdm(artists):
        write_artist_to_database(driver, artist)
    print("done.")
    
    print("Writing similarities...")
    for index, row in tqdm(similarity_data.iterrows()):
        databaseHandler.create_relationship(driver, row["artist1"], row["artist2"], "COSINE", {"similarity": row["similarity"]})
    print("done.")