import { GENRE_COLORS } from "../utils/genreColors";
import { useState } from "react";

interface Props {
  max: number;
  activeGenres: Set<string>;
  onListenersChange: (value: number) => void;
  onToggleGenre: (genre: string) => void;
}

export default function SidePanel({ max, activeGenres, onListenersChange, onToggleGenre }: Props) {
  const [value, setValue] = useState(0);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value);
    setValue(val);
    onListenersChange(val);
  };

  const format = (n: number) =>
    n >= 1_000_000 ? `${(n / 1_000_000).toFixed(1)}M` :
    n >= 1_000 ? `${(n / 1_000).toFixed(0)}K` : `${n}`;

  return (
    <div style={{
      position: "fixed",
      top: 24,
      left: 24,
      background: "#0f172a",
      border: "1px solid #1e293b",
      borderRadius: 12,
      padding: "16px",
      zIndex: 100,
      width: 220,
      display: "flex",
      flexDirection: "column",
      gap: 16,
    }}>

      {/* Popularity slider */}
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
          <span style={{ color: "#475569", fontSize: 11, fontFamily: "monospace", textTransform: "uppercase", letterSpacing: "0.1em" }}>
            Min Listeners
          </span>
          <span style={{ color: "#f1f5f9", fontSize: 11, fontFamily: "monospace" }}>
            {format(value)}
          </span>
        </div>
        <input
          type="range"
          min={0}
          max={max}
          step={10000}
          value={value}
          onChange={handleChange}
          style={{ width: "100%", accentColor: "#38bdf8" }}
        />
      </div>

      {/* Divider */}
      <div style={{ borderTop: "1px solid #1e293b" }} />

      {/* Genre legend */}
      <div>
        <p style={{
          color: "#475569",
          fontSize: 11,
          fontFamily: "monospace",
          textTransform: "uppercase",
          letterSpacing: "0.1em",
          margin: "0 0 10px",
        }}>
          Genres
        </p>
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          {Object.entries(GENRE_COLORS).map(([genre, color]) => {
            const active = activeGenres.has(genre);
            return (
              <button
                key={genre}
                onClick={() => onToggleGenre(genre)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  background: active ? `${color}22` : "transparent",
                  border: `1px solid ${active ? color : "transparent"}`,
                  borderRadius: 6,
                  padding: "4px 8px",
                  cursor: "pointer",
                  textAlign: "left",
                  transition: "all 0.15s",
                }}
              >
                <div style={{
                  width: 10,
                  height: 10,
                  borderRadius: "50%",
                  background: color,
                  flexShrink: 0,
                  opacity: active || activeGenres.size === 0 ? 1 : 0.3,
                }} />
                <span style={{
                  color: active || activeGenres.size === 0 ? "#94a3b8" : "#475569",
                  fontSize: 12,
                  fontFamily: "monospace",
                  textTransform: "capitalize",
                }}>
                  {genre}
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}