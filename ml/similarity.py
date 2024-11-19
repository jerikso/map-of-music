# import spotify.py

import spotify
import numpy as np
import pandas as pd

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

def cosine_similarity(v1, v2):
    # Calculate the cosine similarity between two tracks
    similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return similarity

def calculate_similarities(similarity_metric, feature_vectors):
    # Calculate the similarity between each pair of tracks in the list
    similarities = {}
    for i, track1 in enumerate(feature_vectors):
        for j, track2 in enumerate(feature_vectors[i+1:], start=i+1):
            if i != j:
                similarity = similarity_metric(track1, track2)
                similarities[(i, j)] = similarity
                similarities[(j, i)] = similarity
    return similarities

def create_similarity_dataset_from_search(tracks, similarity_metric):
    # Get a list of tracks
    feature_vectors = [feature_vector_from_track(track) for track in tracks]
    # Calculate the similarity between each pair of tracks
    similarities = calculate_similarities(similarity_metric, feature_vectors)
    
    # create one pandas dataframe for tracks, and one for similarities
    track_data = pd.DataFrame([[track.id, track.name, track.artist, track.album, track.release_date, track.popularity] for track in tracks], columns=["id", "name", "artist", "album", "release_date", "popularity"])
    similarity_data = pd.DataFrame([[track1, track2, similarity] for (track1, track2), similarity in similarities.items()], columns=["track1", "track2", "similarity"])
    
    # change the index to track id
    track_data.set_index("id", inplace=True)
    similarity_data["track1"] = similarity_data["track1"].apply(lambda x: tracks[x].id)
    similarity_data["track2"] = similarity_data["track2"].apply(lambda x: tracks[x].id)
    
    # save the dataframes to csv files
    track_data.to_csv("tracks.csv", index=False)
    similarity_data.to_csv("similarities.csv", index=False)
    