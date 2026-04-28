import type { Artist } from "../types";
import { getGenreColor } from "../utils/genreColors";

interface Props {
  artist: Artist;
  onClose: () => void;
  onGenreClick: (genre: string) => void;
}

export default function ArtistPopup({ artist, onClose, onGenreClick }: Props) {
  const format = (n: number) =>
    n >= 1_000_000 ? `${(n / 1_000_000).toFixed(1)}M` :
    n >= 1_000 ? `${(n / 1_000).toFixed(0)}K` : `${n}`;

  return (
    <div className="artist-popup" style={{
      position: "fixed",
      bottom: 24,
      right: 24,
      background: "#0f172a",
      border: "1px solid #1e293b",
      borderRadius: 16,
      padding: "20px 24px",
      zIndex: 100,
      width: 280,
      boxShadow: "0 25px 50px rgba(0,0,0,0.5)",
    }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
        <h2 style={{
          margin: 0,
          color: "#f1f5f9",
          fontSize: 18,
          fontFamily: "monospace",
          fontWeight: 700,
        }}>
          {artist.name}
        </h2>
        <button
          onClick={onClose}
          style={{
            background: "none",
            border: "none",
            color: "#475569",
            cursor: "pointer",
            fontSize: 18,
            padding: 0,
            lineHeight: 1,
          }}
        >
          ✕
        </button>
      </div>

      {/* Listeners */}
      {artist.listeners != null && artist.listeners > 0 && (
        <div style={{ marginBottom: 16 }}>
          <p style={{ margin: "0 0 4px", color: "#475569", fontSize: 11, fontFamily: "monospace", textTransform: "uppercase", letterSpacing: "0.1em" }}>
            Monthly Listeners
          </p>
          <p style={{ margin: 0, color: "#38bdf8", fontSize: 20, fontFamily: "monospace", fontWeight: 700 }}>
            {format(artist.listeners)}
          </p>
        </div>
      )}

      {/* Genres */}
      {artist.genres && artist.genres.length > 0 && (
        <div>
          <p style={{ margin: "0 0 8px", color: "#475569", fontSize: 11, fontFamily: "monospace", textTransform: "uppercase", letterSpacing: "0.1em" }}>
            Genres
          </p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {artist.genres.slice(0, 6).map(genre => (
              <button
                key={genre}
                onClick={() => onGenreClick(genre.toLowerCase())}
                style={{
                  padding: "3px 10px",
                  borderRadius: 999,
                  fontSize: 11,
                  fontFamily: "monospace",
                  background: `${getGenreColor([genre])}22`,
                  color: getGenreColor([genre]),
                  border: `1px solid ${getGenreColor([genre])}44`,
                  cursor: "pointer",
                }}
              >
                {genre}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}