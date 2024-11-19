# Start from the base Anaconda image
FROM continuumio/anaconda3:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy only the environment file first
COPY environment.yml /app/

# Install dependencies (this step will only re-run if environment.yml changes)
RUN conda env create -f environment.yml

# Now, copy the rest of the application code
COPY . /app/

# Set the shell to use conda environment
SHELL ["conda", "run", "-n", "map-of-music-ml", "/bin/bash", "-c"]

# Set the default command to run the app inside the conda environment
CMD ["conda", "run", "-n", "map-of-music-ml", "python", "spotify.py"]
