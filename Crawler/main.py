import heapq
import os
from time import sleep
from dotenv import load_dotenv
import requests
import psycopg2

DEPTH = 2
NUM_SIMILAR_ARTISTS = 20

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

    def get_most_popular_artists(self, amount):
        params = {
            'method': 'chart.gettopartists',
            'api_key': self.api_key,
            'format': 'json',
            'limit': amount
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'artists' in data and 'artist' in data['artists']:
                return [artist['name'] for artist in data['artists']['artist']]
        return []

    def get_artist_info(self, artist_name: str) -> dict:
        params = {
            "method": "artist.getinfo",
            "artist": artist_name,
            "api_key": self.api_key,
            "format": "json",
        }
        retries = 3
        for attempt in range(retries):
            try:
                response = requests.get(self.base_url, params=params)
                
                if response.status_code == 429:
                    wait = 5 * (attempt + 1)
                    print(f"Rate limited, waiting {wait}s before retry...")
                    sleep(wait)
                    continue

                if response.status_code != 200 or not response.text:
                    print(f"Failed to get info for {artist_name}: status {response.status_code}")
                    return {"listeners": 0, "playcount": 0, "genres": []}

                data = response.json().get("artist", {})
                stats = data.get("stats", {})
                tags = data.get("tags", {}).get("tag", [])
                return {
                    "listeners": int(stats.get("listeners", 0)),
                    "playcount": int(stats.get("playcount", 0)),
                    "genres": [tag["name"] for tag in tags],
                }

            except Exception as e:
                print(f"Error getting info for {artist_name} (attempt {attempt + 1}): {e}")
                sleep(2)

        print(f"Giving up on {artist_name} after {retries} attempts")
        return {"listeners": 0, "playcount": 0, "genres": []}

class PostgreDriver():
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="db",
            port=5432
        )

    def create_artists_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS artists (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL,
                    listeners BIGINT,
                    playcount BIGINT,
                    genres TEXT[]
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

    def initialize_schema(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                ALTER TABLE artists ALTER COLUMN listeners TYPE BIGINT;
                ALTER TABLE artists ALTER COLUMN playcount TYPE BIGINT;
            """)
        self.conn.commit()

    def insert_artist(self, name, listeners=None, playcount=None, genres=None):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO artists (name, listeners, playcount, genres)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE
                    SET listeners = COALESCE(EXCLUDED.listeners, artists.listeners),
                        playcount = COALESCE(EXCLUDED.playcount, artists.playcount),
                        genres = COALESCE(EXCLUDED.genres, artists.genres)
                RETURNING id;
            ''', (name, listeners, playcount, genres))
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

    def get_visited_artists(self) -> set:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT name FROM artists WHERE listeners IS NOT NULL")
            return {row[0] for row in cursor.fetchall()}
    

    def close(self):
        self.conn.close()

def crawl_artists_popularity_first(seeds, depth, lastfm_driver, postgres_driver):
    postgres_driver.create_artists_table()
    postgres_driver.create_similarities_table()
    postgres_driver.initialize_schema()

    # load already visited artists from DB
    visited = postgres_driver.get_visited_artists()
    print(f"Resuming from {len(visited)} already crawled artists")

    heap = []
    for seed in seeds:
        if seed not in visited:
            info = lastfm_driver.get_artist_info(seed)
            heapq.heappush(heap, (-info["listeners"], 0, seed, info))

    while heap:
        neg_listeners, current_depth, artist_name, info = heapq.heappop(heap)

        if artist_name in visited or current_depth > depth:
            continue

        visited.add(artist_name)

        print(f"[{len(visited)}] Crawling: {artist_name} ({-neg_listeners:,} listeners) at depth {current_depth}")

        artist_id = postgres_driver.insert_artist(
            artist_name,
            listeners=info["listeners"],
            playcount=info["playcount"],
            genres=info["genres"],
        )

        similar_artists = lastfm_driver.get_similar_artists(artist_name)
        print(f"  Found {len(similar_artists)} similar artists")

        for similarity in similar_artists:
            if similarity.artist_2 not in visited:
                # fetch info immediately so we can prioritize by popularity
                similar_info = lastfm_driver.get_artist_info(similarity.artist_2)
                similar_artist_id = postgres_driver.insert_artist(
                    similarity.artist_2,
                    listeners=similar_info["listeners"],
                    playcount=similar_info["playcount"],
                    genres=similar_info["genres"],
                )
                if artist_id and similar_artist_id:
                    postgres_driver.insert_similarity(artist_id, similar_artist_id, similarity.similarity_score)
                heapq.heappush(heap, (-similar_info["listeners"], current_depth + 1, similarity.artist_2, similar_info))
            
        sleep(0.2)

    postgres_driver.close()

if __name__ == "__main__":
    lastfm_driver = LastFMDriver()
    postgres_driver = PostgreDriver()

    # global popular artists
    popular_artists = lastfm_driver.get_most_popular_artists(50)

    # genre-specific seeds to ensure diversity
    genre_seeds = [
        # prog metal
        "Opeth", "Tool", "Porcupine Tree", "Dream Theater", "Meshuggah",
        # jazz
        "Miles Davis", "John Coltrane", "Bill Evans",
        # classical
        "Bach", "Beethoven", "Mozart",
        # electronic
        "Aphex Twin", "Burial", "Boards of Canada",
        # hip-hop
        "Kendrick Lamar", "MF DOOM", "Earl Sweatshirt",
        # folk
        "Nick Drake", "Elliott Smith", "Iron & Wine",
        # metal
        "Gojira", "Mastodon", "Baroness",
        # french rap
        "Nekfeu", "Damso", "Lomepal",
        # swedish
        "Robyn", "Avicii", "Håkan Hellström",
    ]

    all_seeds = list(set(popular_artists + genre_seeds))
    print(f"Crawling {len(all_seeds)} seeds")
    crawl_artists_popularity_first(all_seeds, DEPTH, lastfm_driver, postgres_driver)