# Make requests to Last FM, search artist name and get similar artists

import os
from dotenv import load_dotenv

import requests

import psycopg2

SEEDS = [
    "Radiohead",
    "Opeth",
    "Muse",
    "Porcupine Tree",
    "Steven Wilson",
    "Sleep Token",
    "Bad Omens",
    "Yasin",
    "Coldplay",
    "Luidji",
    "Thirty Seconds to Mars",
    "Katatonia",
    "Fleetwood Mac",
    "Phil Collins",
]

NUM_SIMILAR_ARTISTS = 5

DEPTH = 2

class Similarity:
    def __init__(self, artist_1, artist_2, similarity_score):
        self.artist_1 = artist_1
        self.artist_2 = artist_2
        self.similarity_score = similarity_score
        
class LastFMDriver():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('LASTFM_API_KEY')
        self.base_url = 'http://ws.audioscrobbler.com/2.0/'

    def get_similar_artists(self, artist_name, limit=NUM_SIMILAR_ARTISTS):
        params = {
            'method': 'artist.getsimilar',
            'artist': artist_name,
            'api_key': self.api_key,
            'format': 'json',
            'limit': limit
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'similarartists' in data and 'artist' in data['similarartists']:
                similar_artists = []
                for artist in data['similarartists']['artist']:
                    name = artist['name']
                    similarity_score = float(artist['match'])
                    similar_artists.append(Similarity(artist_name, name, similarity_score))
                return similar_artists
        return []

class PostgreDriver():
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="localhost",
            port=5432
        )

    def create_artists_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS artists (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL
                );
            ''')
            self.conn.commit()
    
    def create_similarities_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS similarities (
                    id SERIAL PRIMARY KEY,
                    artist_1_id INTEGER NOT NULL,
                    artist_2_id INTEGER NOT NULL,
                    similarity_score FLOAT NOT NULL,
                    UNIQUE (artist_1_id, artist_2_id),
                    FOREIGN KEY (artist_1_id) REFERENCES artists(id),
                    FOREIGN KEY (artist_2_id) REFERENCES artists(id)
                );
            ''')
            self.conn.commit()
    
    def insert_artist(self, name):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO artists (name) VALUES (%s)
                ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                RETURNING id;
            ''', (name,))
            result = cursor.fetchone()
            self.conn.commit()
            return result[0] if result else None
    
    def insert_similarity(self, artist_1_id, artist_2_id, similarity_score):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO similarities (artist_1_id, artist_2_id, similarity_score)
                VALUES (%s, %s, %s)
                ON CONFLICT (artist_1_id, artist_2_id) DO NOTHING;
            ''', (artist_1_id, artist_2_id, similarity_score))
            self.conn.commit()
    
    def close(self):
        self.conn.close()
        
def crawl_artists(seeds, depth):
    lastfm_driver = LastFMDriver()
    postgres_driver = PostgreDriver()
    
    postgres_driver.create_artists_table()
    postgres_driver.create_similarities_table()
    
    visited = set()
    queue = [(seed, 0) for seed in seeds]
    
    while queue:
        artist_name, current_depth = queue.pop(0)
        
        print(f"Crawling: {artist_name} at depth {current_depth}")
        
        if artist_name in visited or current_depth > depth:
            continue
        
        visited.add(artist_name)
        
        artist_id = postgres_driver.insert_artist(artist_name)
        
        similar_artists = lastfm_driver.get_similar_artists(artist_name)
        
        print(f"Found {len(similar_artists)} similar artists for {artist_name}")
        
        for similarity in similar_artists:
            similar_artist_id = postgres_driver.insert_artist(similarity.artist_2)
            if artist_id and similar_artist_id:
                postgres_driver.insert_similarity(artist_id, similar_artist_id, similarity.similarity_score)
            queue.append((similarity.artist_2, current_depth + 1))
    
    postgres_driver.close()
if __name__ == "__main__":
    crawl_artists(SEEDS, DEPTH)
    
    