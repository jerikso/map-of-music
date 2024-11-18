# map-of-music

map-of-music is a web application that helps users discover and explore similarities between songs, artists, and genres using an interactive graph. It leverages the **Spotify API** for data, **machine learning** for similarity computation, and **Neo4j** for graph-based storage and traversal.

## **Features**
- **Music Discovery**: Find similar songs and artists based on Spotify's audio features and machine learning analysis.
- **Graph Visualization**: Explore music relationships using an interactive graph.
- **Scalable Architecture**: Decoupled backend, ML processing, and graph storage for performance and scalability.
- **Modern Stack**: Built with **Vue.js**, **FastAPI**, and **Neo4j**.

## **Tech Stack**
- **Frontend**: Vue.js (Interactive UI)
- **Backend**: FastAPI (API layer)
- **Database**: Neo4j (Graph database for relationships)
- **Machine Learning**: Python, sklearn (Similarity and clustering algorithms)
- **Deployment**: Dockerized services

## **How It Works**
1. **Data Fetching**:  
   - The backend retrieves music data (songs, artists, features) from the Spotify API.

2. **ML Processing**:  
   - A separate ML service computes song/artist similarities and updates the graph in Neo4j.

3. **Graph Storage**:  
   - Nodes: Represent songs, artists, or genres.  
   - Edges: Represent similarities or other relationships (e.g., collaborations).

4. **Visualization**:  
   - The frontend queries the backend for graph data and renders it for users to explore.
