import { useState, useMemo } from "react";

import { useMapData } from "./hooks/useMapData";
import type { Artist } from "./types";

import MapCanvas from "./components/MapCanvas";
import SidePanel from "./components/SidePanel";
import ArtistPopup from "./components/ArtistPopup";


export default function App() {
  const { artists, similarities, loading, error } = useMapData();
  const [selected, setSelected] = useState<Artist | null>(null);
  const [minListeners, setMinListeners] = useState(0);
  const [activeGenres, setActiveGenres] = useState<Set<string>>(new Set());


  const handleSelectArtist = (artist: Artist) => {
    setSelected(null);
    setTimeout(() => setSelected(artist), 0);
  };

  const maxListeners = useMemo(
    () => Math.max(...artists.map(a => a.listeners ?? 0)),
    [artists]
  );

  const filteredArtists = useMemo(
    () => artists.filter(a => {
      const meetsListeners = (a.listeners ?? 0) >= minListeners;
      const meetsGenre = activeGenres.size === 0 || 
        a.genres?.some(g => activeGenres.has(g.toLowerCase()));
      return meetsListeners && meetsGenre;
    }),
    [artists, minListeners, activeGenres]
  );

  const availableGenres = useMemo(() => {
    const genres = new Set<string>();
    artists.forEach(a => a.genres?.forEach(g => genres.add(g.toLowerCase())));
    return Array.from(genres).sort();
  }, [artists]);

  const toggleGenre = (genre: string) => {
    setActiveGenres(prev => {
      const next = new Set(prev);
      if (next.has(genre)) next.delete(genre);
      else next.add(genre);
      return next;
    });
  };

  const removeGenre = (genre: string) => {
    setActiveGenres(prev => {
      const next = new Set(prev);
      next.delete(genre);
      return next;
    });
  };

  if (loading) return <div style={{ color: "white", padding: 24 }}>Loading...</div>;
  if (error) return <div style={{ color: "white", padding: 24 }}>Error: {error}</div>;

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <MapCanvas
        artists={filteredArtists}
        similarities={similarities}
        selectedArtist={selected}
        onSelectArtist={handleSelectArtist}
      />
      <SidePanel
        max={maxListeners}
        activeGenres={activeGenres}
        availableGenres={availableGenres}
        onListenersChange={setMinListeners}
        onToggleGenre={toggleGenre}
        onRemoveGenre={removeGenre}
      />
      {selected && (
        <ArtistPopup
          artist={selected}
          onClose={() => setSelected(null)}
          onGenreClick={toggleGenre}
        />
      )}
    </div>
  );
}