from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="db",
        port=5432
    )

@app.get("/map")
def get_map():
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, x, y, listeners, genres FROM artists WHERE x IS NOT NULL")
            rows = cursor.fetchall()
        return [{"id": r[0], "name": r[1], "x": r[2], "y": r[3], "listeners": r[4], "genres": r[5]} for r in rows]
    finally:
        conn.close() # This ensures the connection is freed up even if an error occurs

@app.get("/similarities")
def get_similarities():
    conn = get_conn()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT artist_1_id, artist_2_id, similarity_score
            FROM similarities
        """)
        rows = cursor.fetchall()
    conn.close()

    return [
        {
            "artist1Id": row[0],
            "artist2Id": row[1],
            "score": row[2],
        }
        for row in rows
    ]