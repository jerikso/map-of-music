# map-of-music

map-of-music is a web application that helps users discover and explore similarities between music artists using an interactive map. It leverages the **Last.fm API** for data, **UMAP** for dimensionality reduction, and **PostgreSQL** for storage.

## Features
- **Music Discovery**: Find similar artists based on Last.fm similarity scores.
- **Interactive Map**: Explore artist relationships on a 2D map where similar artists appear closer together.
- **Search**: Search for any artist and fly to their position on the map.
- **Scalable Architecture**: Decoupled crawler, ML service, API, and frontend running as separate Docker services.
- **Modern Stack**: Built with **React + TypeScript**, **FastAPI**, and **PostgreSQL**.

## **Tech Stack**
* **Frontend**: React + TypeScript (Interactive map UI)
* **Backend**: FastAPI (API layer between Frontend and Database)
* **Database**: PostgreSQL (Artist and similarity data)
* **Machine Learning**: Python, UMAP (Dimensionality reduction for map coordinates)
* **Data Collection**: Python, Last.fm API (Artist crawling and similarity scores)
* **Deployment**: Docker + Docker Compose

## How It Works

1. **Data Collection**
   - The crawler fetches artist data and similarity scores from the Last.fm API, storing them in PostgreSQL.

2. **ML Processing**
   - A separate service builds a similarity matrix from the crawled data and runs UMAP to compute 2D coordinates for each artist.

3. **Data Storage**
   - Artists and their similarity scores are stored in PostgreSQL.
   - Each artist gets an x/y coordinate representing their position on the map.

4. **Visualization**
   - The frontend fetches artist data from the FastAPI backend and renders an interactive map using Sigma.js, where similar artists appear closer together.

## Running the services

### Database, API and crawlers
Requires Docker. From the root directory:

```bash
sudo docker compose up -d db        # start the database
sudo docker compose up --build crawler      # crawl artist data from Last.fm
sudo docker compose up --build similaritymap  # compute UMAP coordinates
sudo docker compose up --build api          # start the API
```

### Frontend
Requires Node.js. From the `Frontend/` directory:

```bash
npm install   # first time only
npm run dev   # starts at http://localhost:5173
```

The API must be running before starting the frontend.