import similarity
import spotify

if __name__ == "__main__":
    client = spotify.SpotifyClient()
    tracks = client.search_tracks("Porcupine Tree")
    similarity.create_similarity_dataset_from_search(tracks, similarity.cosine_similarity)
    print("done")