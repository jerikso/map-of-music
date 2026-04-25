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

@app.get("/api/map")
def get_map():
    conn = get_conn()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, x, y, listeners, genres
            FROM artists
            WHERE x IS NOT NULL
        """)
        rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "x": row[2],
            "y": row[3],
            "listeners": row[4],
            "genres": row[5],
        }
        for row in rows
    ]