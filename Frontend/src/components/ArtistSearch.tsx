import { useState } from "react";
import { useSigma } from "@react-sigma/core";
import type { Artist } from "../types";
import { getGenreColor } from "../utils/genreColors";

interface Props {
  artists: Artist[];
  onSelectArtist: (artist: Artist) => void;
}

export default function ArtistSearch({ artists, onSelectArtist }: Props) {
  const [search, setSearch] = useState("");
  useSigma();

  const results = search.trim()
    ? artists.filter(a =>
        a.name.toLowerCase().includes(search.toLowerCase())
      ).slice(0, 8)
    : [];

  const handleSelect = (artist: Artist) => {
    onSelectArtist(artist);
    setSearch("");
  };

  return (
    <div className="artist-search" style={{
      position: "absolute",
      top: 24,
      right: 24,
      width: 240,
      zIndex: 100,
    }}>
      <input
        value={search}
        onChange={e => setSearch(e.target.value)}
        placeholder="Search artists..."
        style={{
          width: "100%",
          background: "#0f172a",
          border: "1px solid #1e293b",
          borderRadius: results.length > 0 ? "8px 8px 0 0" : "8px",
          padding: "8px 12px",
          color: "#f1f5f9",
          fontSize: 12,
          fontFamily: "monospace",
          outline: "none",
          boxSizing: "border-box",
        }}
      />
      {results.length > 0 && (
        <div style={{
          background: "#0f172a",
          border: "1px solid #1e293b",
          borderTop: "none",
          borderRadius: "0 0 8px 8px",
          overflow: "hidden",
        }}>
          {results.map(artist => (
            <button
              key={artist.id}
              onClick={() => handleSelect(artist)}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                gap: 8,
                background: "transparent",
                border: "none",
                borderTop: "1px solid #1e293b",
                padding: "8px 12px",
                cursor: "pointer",
                textAlign: "left",
              }}
              onMouseEnter={e => e.currentTarget.style.background = "#1e293b"}
              onMouseLeave={e => e.currentTarget.style.background = "transparent"}
            >
              <div style={{
                width: 8,
                height: 8,
                borderRadius: "50%",
                background: getGenreColor(artist.genres),
                flexShrink: 0,
              }} />
              <span style={{ color: "#94a3b8", fontSize: 12, fontFamily: "monospace" }}>
                {artist.name}
              </span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}