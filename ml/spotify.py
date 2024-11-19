from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access variables using os.getenv
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

print(spotify_client_id, spotify_client_secret)
