import argparse
import os

import networkx as nx
import numpy as np
import psycopg2
import umap
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="db",
    port=5432,
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
    matrix = np.zeros((n, n), dtype=float)

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
        n_components=2,
        metric="precomputed",
        n_neighbors=15,
        min_dist=0.1,
        random_state=42,
    )
    distance_matrix = 1 - matrix
    return reducer.fit_transform(distance_matrix)


def run_networkx_layout(matrix, iterations=500, scale=1.0):
    n = matrix.shape[0]
    if n == 0:
        return np.empty((0, 2), dtype=float)

    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            weight = float(matrix[i, j])
            if weight != 0.0:
                G.add_edge(i, j, weight=weight)

    pos = nx.spring_layout(
        G,
        dim=2,
        iterations=iterations,
        seed=42,
        weight="weight",
        scale=scale,
    )

    coords = np.vstack([pos[i] for i in range(n)])
    coords -= coords.min(axis=0)
    size = coords.max(axis=0)
    coords /= np.where(size == 0, 1.0, size)

    return coords


def save_coordinates(conn, artist_ids, coords):
    cur = conn.cursor()
    cur.execute(
        """
        ALTER TABLE artists
        ADD COLUMN IF NOT EXISTS x FLOAT,
        ADD COLUMN IF NOT EXISTS y FLOAT
        """
    )
    for artist_id, (x, y) in zip(artist_ids, coords):
        cur.execute(
            """
            UPDATE artists SET x = %s, y = %s WHERE id = %s
            """,
            (float(x), float(y), artist_id),
        )
    conn.commit()
    print(f"Saved coordinates for {len(artist_ids)} artists")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build artist coordinate layout from similarity scores")
    parser.add_argument(
        "--method",
        choices=["umap", "networkx", "force"],
        default="umap",
        help="Layout algorithm to use for coordinates",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=500,
        help="Number of spring-layout iterations when using --method networkx or --method force",
    )
    args = parser.parse_args()

    matrix, artist_ids, artist_names = build_matrix(conn)
    print(f"Built {len(artist_names)}x{len(artist_names)} matrix")

    if args.method in ("networkx", "force"):
        coords = run_networkx_layout(matrix, iterations=args.iterations)
    else:
        coords = run_umap(matrix)

    save_coordinates(conn, artist_ids, coords)
