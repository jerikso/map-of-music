import { useState, useEffect } from "react";
import type { Artist } from "../types";

export function useMapData() {
  const [artists, setArtists] = useState<Artist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

  return { artists, loading, error };
}