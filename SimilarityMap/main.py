import psycopg2
import numpy as np
import pandas as pd
import umap
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="db",
    port=5432
)

def build_matrix(conn):
    cur = conn.cursor()

    # fetch all artists
    cur.execute("SELECT id, name FROM artists")
    artists = cur.fetchall()
    artist_ids = [a[0] for a in artists]
    artist_names = [a[1] for a in artists]
    id_to_idx = {id: i for i, id in enumerate(artist_ids)}

    # build empty matrix
    n = len(artists)
    matrix = np.zeros((n, n))

    # fill in similarity scores
    cur.execute("SELECT artist_1_id, artist_2_id, similarity_score FROM similarities")
    for artist_id, similar_id, score in cur.fetchall():
        i = id_to_idx.get(artist_id)
        j = id_to_idx.get(similar_id)
        if i is not None and j is not None:
            matrix[i][j] = score
            matrix[j][i] = score  # make it symmetric

    # diagonal is 1 (every artist is identical to itself)
    np.fill_diagonal(matrix, 1.0)

    return matrix, artist_ids, artist_names

def run_umap(matrix):
    reducer = umap.UMAP(
        n_components=2,       # 2D output for the map
        metric="precomputed", # we're passing a distance matrix
        n_neighbors=15,       # how local vs global the layout is
        min_dist=0.1,         # how tightly clustered points are
        random_state=42       # reproducible results
    )
    # UMAP expects a distance matrix, not similarity — invert it
    distance_matrix = 1 - matrix
    return reducer.fit_transform(distance_matrix)

def save_coordinates(conn, artist_ids, coords):
    cur = conn.cursor()
    cur.execute("""
        ALTER TABLE artists 
        ADD COLUMN IF NOT EXISTS x FLOAT,
        ADD COLUMN IF NOT EXISTS y FLOAT
    """)
    for artist_id, (x, y) in zip(artist_ids, coords):
        cur.execute("""
            UPDATE artists SET x = %s, y = %s WHERE id = %s
        """, (float(x), float(y), artist_id))
    conn.commit()
    print(f"Saved coordinates for {len(artist_ids)} artists")

# run it
matrix, artist_ids, artist_names = build_matrix(conn)
print(f"Built {len(artist_names)}x{len(artist_names)} matrix")

coords = run_umap(matrix)
save_coordinates(conn, artist_ids, coords)