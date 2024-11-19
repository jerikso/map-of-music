import numpy as np

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
    