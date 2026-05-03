import { useState, useEffect } from "react";
import type { Artist, Similarity } from "../types";

export function useMapData() {
  const [artists, setArtists] = useState<Artist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [similarities, setSimilarities] = useState<Similarity[]>([]);

  useEffect(() => {
    fetch("/api/map")
      .then((res) => res.json())
      .then((data) => {
        setArtists(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
  fetch("/api/similarities")
    .then(res => res.json())
    .then(setSimilarities)
    .catch(console.error);
}, []);

  return { artists, similarities, loading, error };
}